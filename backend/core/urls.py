from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import StoreViewSet, GasTypeViewSet, WithdrawalViewSet, UserViewSet, StockViewSet, StockMovementViewSet

router = DefaultRouter()
router.register(r'stores', StoreViewSet)
router.register(r'gastypes', GasTypeViewSet)
router.register(r'withdrawals', WithdrawalViewSet)
router.register(r'users', UserViewSet)
router.register(r'stocks', StockViewSet)
router.register(r'stock-movements', StockMovementViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
