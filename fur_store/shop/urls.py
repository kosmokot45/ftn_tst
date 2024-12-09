from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import ProductsViewSet, ProductViewSet, CategoryViewSet, CartViewSet, OrderViewSet

router = DefaultRouter()
router.register(r"products", ProductsViewSet, basename="products")
router.register(r"product", ProductViewSet, basename="product")
router.register(r"categories", CategoryViewSet, basename="categories")
router.register(r"cart", CartViewSet, basename="cart")
router.register(r"order", OrderViewSet, basename="order")

urlpatterns = [
    path("", include(router.urls)),
]
