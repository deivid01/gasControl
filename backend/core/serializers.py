from rest_framework import serializers
from .models import CustomUser, Store, GasType, Withdrawal, Stock, StockMovement

class CustomUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['id', 'username', 'role', 'first_name', 'last_name']

class StoreSerializer(serializers.ModelSerializer):
    class Meta:
        model = Store
        fields = '__all__'

class GasTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = GasType
        fields = '__all__'

class WithdrawalSerializer(serializers.ModelSerializer):
    store_name = serializers.CharField(source='store.name', read_only=True)
    gas_type_name = serializers.CharField(source='gas_type.name', read_only=True)
    created_by_username = serializers.CharField(source='created_by.username', read_only=True)

    class Meta:
        model = Withdrawal
        fields = '__all__'
        read_only_fields = ['created_by']

class StockSerializer(serializers.ModelSerializer):
    store_name = serializers.CharField(source='store.name', read_only=True)
    gas_type_name = serializers.CharField(source='gas_type.name', read_only=True)

    class Meta:
        model = Stock
        fields = '__all__'

class StockMovementSerializer(serializers.ModelSerializer):
    stock_info = serializers.CharField(source='stock.__str__', read_only=True)
    created_by_username = serializers.CharField(source='created_by.username', read_only=True)
    movement_type_display = serializers.CharField(source='get_movement_type_display', read_only=True)

    class Meta:
        model = StockMovement
        fields = '__all__'
