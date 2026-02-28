from django.db import transaction
from rest_framework import viewsets, permissions, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.pagination import LimitOffsetPagination
from .models import CustomUser, Store, GasType, Withdrawal, Stock, StockMovement
from .serializers import (
    CustomUserSerializer, StoreSerializer, GasTypeSerializer, 
    WithdrawalSerializer, StockSerializer, StockMovementSerializer
)

class IsMasterOrReadOnly(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.user.role == 'MASTER':
            return True
        return request.method in permissions.SAFE_METHODS

class IsEncarregadoOrMaster(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.user.role in ['MASTER', 'ENCARREGADO']:
            return True
        return request.method in permissions.SAFE_METHODS

class CanCreateWithdrawal(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.user.role in ['MASTER', 'ENCARREGADO', 'OPERADOR']:
            return True
        return request.method in permissions.SAFE_METHODS

class StoreViewSet(viewsets.ModelViewSet):
    queryset = Store.objects.all()
    serializer_class = StoreSerializer
    permission_classes = [permissions.IsAuthenticated, IsMasterOrReadOnly]

class GasTypeViewSet(viewsets.ModelViewSet):
    queryset = GasType.objects.all()
    serializer_class = GasTypeSerializer
    permission_classes = [permissions.IsAuthenticated, IsMasterOrReadOnly]

class WithdrawalViewSet(viewsets.ModelViewSet):
    queryset = Withdrawal.objects.all().order_by('-created_at')
    serializer_class = WithdrawalSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        queryset = Withdrawal.objects.all().order_by('-created_at')
        store_id = self.request.query_params.get('store', None)
        if store_id is not None:
            queryset = queryset.filter(store__id=store_id)
        return queryset

    def get_permissions(self):
        if self.action == 'create':
            return [permissions.IsAuthenticated(), CanCreateWithdrawal()]
        elif self.action in ['update', 'partial_update', 'destroy']:
            return [permissions.IsAuthenticated(), IsEncarregadoOrMaster()]
        return [permissions.IsAuthenticated()]

    @transaction.atomic
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        store = serializer.validated_data['store']
        gas_type = serializer.validated_data['gas_type']
        quantity = serializer.validated_data['quantity']
        
        try:
            # select_for_update locka a linha no banco até a transação acabar
            stock = Stock.objects.select_for_update().get(store=store, gas_type=gas_type)
        except Stock.DoesNotExist:
            return Response({"error": "Estoque não configurado para este gás nesta loja."}, status=status.HTTP_400_BAD_REQUEST)
            
        if stock.quantity < quantity:
            return Response({"error": f"Saldo em estoque insuficiente. Saldo atual: {stock.quantity}"}, status=status.HTTP_400_BAD_REQUEST)
            
        # Deduzir
        stock.quantity -= quantity
        stock.save()
        
        # Salvar o Withdrawal
        self.perform_create(serializer)
        
        # Registrar o Movimento
        StockMovement.objects.create(
            stock=stock,
            quantity=-quantity,
            movement_type='SAIDA',
            created_by=request.user,
            description=f"Retirada PDV {serializer.validated_data.get('pdv')}"
        )
        
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)

    @action(detail=False, methods=['get'], permission_classes=[permissions.IsAuthenticated])
    def history(self, request):
        if request.user.role not in ['MASTER', 'ENCARREGADO']:
            return Response({"error": "Acesso negado"}, status=403)
            
        history = Withdrawal.history.all().order_by('-history_date')
        
        paginator = LimitOffsetPagination()
        paginated_history = paginator.paginate_queryset(history, request)
        
        data = [{
            'history_id': h.history_id,
            'history_date': h.history_date,
            'history_type': h.history_type,
            'history_user': h.history_user.username if h.history_user else None,
            'quantity': h.quantity,
            'gas_type': h.gas_type.name if h.gas_type else None,
            'store': h.store.name if h.store else None,
            'pdv': h.pdv,
            'operator': h.operator,
            'retriever_name': h.retriever_name
        } for h in paginated_history]
        
        return paginator.get_paginated_response(data)

class UserViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = CustomUser.objects.all()
    serializer_class = CustomUserSerializer
    permission_classes = [permissions.IsAuthenticated]

    @action(detail=False, methods=['get'])
    def me(self, request):
        serializer = self.get_serializer(request.user)
        return Response(serializer.data)

class StockViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Stock.objects.all()
    serializer_class = StockSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        queryset = Stock.objects.all()
        store_id = self.request.query_params.get('store', None)
        if store_id is not None:
            queryset = queryset.filter(store__id=store_id)
        return queryset

class StockMovementViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = StockMovement.objects.all().order_by('-created_at')
    serializer_class = StockMovementSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        queryset = StockMovement.objects.all().order_by('-created_at')
        stock_id = self.request.query_params.get('stock', None)
        store_id = self.request.query_params.get('store', None)
        if stock_id:
            queryset = queryset.filter(stock__id=stock_id)
        if store_id:
            queryset = queryset.filter(stock__store__id=store_id)
        return queryset
