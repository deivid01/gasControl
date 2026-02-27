from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import StoreViewSet, GasTypeViewSet, WithdrawalViewSet, UserViewSet

router = DefaultRouter()
router.register(r'stores', StoreViewSet)
router.register(r'gastypes', GasTypeViewSet)
router.register(r'withdrawals', WithdrawalViewSet)
router.register(r'users', UserViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
