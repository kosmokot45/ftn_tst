from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import ProductViewSet, CategoryViewSet, CartViewSet, OrderViewSet

router = DefaultRouter()
router.register(r"products", ProductViewSet)
router.register(r"categories", CategoryViewSet)
router.register(r"cart", CartViewSet)
router.register(r"order", OrderViewSet)

urlpatterns = [
    path("", include(router.urls)),
]
