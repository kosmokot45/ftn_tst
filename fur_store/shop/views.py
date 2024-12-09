from drf_spectacular.utils import extend_schema, OpenApiParameter
from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from .models import Cart, Category, Order, Product
from .serializers import (
    CartSerializer,
    CategoryIDSerializer,
    CategorySerializer,
    OrderSerializer,
    ProductSerializer,
    ProductsSerializer,
)


class ProductsViewSet(viewsets.ViewSet):

    @extend_schema(
        request=CategoryIDSerializer,
        responses={200: ProductsSerializer(many=True)},
    )
    def create(self, request):
        category_id = request.data.get("category_id")
        queryset = Product.objects.all()
        if category_id:
            queryset = queryset.filter(category_id=category_id)
        serializer = ProductsSerializer(queryset, many=True)
        return Response(serializer.data)


# class ProductViewSet(viewsets.ReadOnlyModelViewSet):
#     queryset = Product.objects.all()
#     serializer_class = ProductSerializer

#     def retrieve(self, request, pk=None):
#         product = self.get_object()
#         serializer = self.get_serializer(product)
#         return Response(serializer.data)

# def get_queryset(self):
#     queryset = super().get_queryset()
#     # Фильтрация и сортировка по цене
#     min_price = self.request.query_params.get("min_price")
#     max_price = self.request.query_params.get("max_price")
#     if min_price:
#         queryset = queryset.filter(price__gte=min_price)
#     if max_price:
#         queryset = queryset.filter(price__lte=max_price)
#     return queryset


class ProductViewSet(viewsets.ViewSet):

    @extend_schema(
        responses={200: ProductSerializer},
        parameters=[
            OpenApiParameter(
                name="min_price",
                required=False,
                type=float,
                description="Минимальная цена для фильтрации",
            ),
            OpenApiParameter(
                name="max_price",
                required=False,
                type=float,
                description="Максимальная цена для фильтрации",
            ),
        ],
    )
    def retrieve(self, request, pk=None):
        try:
            product = Product.objects.get(pk=pk)
        except Product.DoesNotExist:
            return Response({"detail": "Товар не найден"}, status=status.HTTP_404_NOT_FOUND)

        min_price = request.query_params.get("min_price")
        max_price = request.query_params.get("max_price")

        if min_price is not None:
            if product.price < float(min_price):
                return Response({"detail": "Цена продукта ниже чем указанная"}, status=status.HTTP_400_BAD_REQUEST)

        if max_price is not None:
            if product.price > float(max_price):
                return Response({"detail": "Цена продукта выше чем указанная"}, status=status.HTTP_400_BAD_REQUEST)

        serializer = ProductSerializer(product)
        return Response(serializer.data)


class CategoryViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer


class CartViewSet(viewsets.ModelViewSet):
    serializer_class = CartSerializer

    def get_queryset(self):
        user = self.request.user
        return Cart.objects.filter(user=user)

    def list(self, request):
        # Получаем корзину текущего пользователя
        cart = self.get_queryset().first()
        if cart:
            serializer = self.get_serializer(cart)
            return Response(serializer.data)
        return Response({"detail": "Cart not found."}, status=status.HTTP_404_NOT_FOUND)

    def create(self, request):
        # Создаем новую корзину для пользователя, если ее нет
        cart, created = Cart.objects.get_or_create(user=request.user)
        serializer = self.get_serializer(cart)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def update(self, request, pk=None):
        # # Обновление корзины (например, можно добавить логику для обновления)
        # return Response({"detail": "Method not allowed."}, status=status.HTTP_405_METHOD_NOT_ALLOWED)
        cart = self.get_queryset().first()
        if not cart:
            return Response({"detail": "Cart not found."}, status=status.HTTP_404_NOT_FOUND)

        product_id = request.data.get("product_id")
        quantity = request.data.get("quantity")

        if quantity is None:
            return Response({"detail": "Quantity is required."}, status=status.HTTP_400_BAD_REQUEST)

        try:
            cart_item = CartItem.objects.get(cart=cart, product_id=product_id)
            cart_item.quantity = quantity
            cart_item.save()
            return Response({"detail": "Cart item updated."}, status=status.HTTP_200_OK)
        except CartItem.DoesNotExist:
            return Response({"detail": "Cart item not found."}, status=status.HTTP_404_NOT_FOUND)

    def destroy(self, request, pk=None):
        cart = self.get_queryset().first()
        if not cart:
            return Response({"detail": "Cart not found."}, status=status.HTTP_404_NOT_FOUND)

        cart.cartitem_set.all().delete()  # Удаляем все элементы из корзины
        return Response({"detail": "Cart cleared."}, status=status.HTTP_204_NO_CONTENT)

    @action(detail=False, methods=["post"])
    def add_product(self, request):
        cart = self.get_queryset().first()
        if not cart:
            return Response({"detail": "Cart not found."}, status=status.HTTP_404_NOT_FOUND)

        product_id = request.data.get("product_id")
        quantity = request.data.get("quantity", 1)

        try:
            product = Product.objects.get(id=product_id)
        except Product.DoesNotExist:
            return Response({"detail": "Product not found."}, status=status.HTTP_404_NOT_FOUND)

        cart_item, created = CartItem.objects.get_or_create(cart=cart, product=product)
        cart_item.quantity += quantity
        cart_item.save()
        return Response(status=status.HTTP_201_CREATED)

    @action(detail=False, methods=["delete"])
    def remove_product(self, request):
        cart = self.get_queryset().first()
        if not cart:
            return Response({"detail": "Cart not found."}, status=status.HTTP_404_NOT_FOUND)

        product_id = request.data.get("product_id")
        try:
            cart_item = CartItem.objects.get(cart=cart, product_id=product_id)
            cart_item.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        except CartItem.DoesNotExist:
            return Response({"detail": "Cart item not found."}, status=status.HTTP_404_NOT_FOUND)

    @extend_schema(exclude=True)
    def partial_update(self, request, *args, **kwargs):
        return Response({"detail": "PATCH method is not allowed."}, status=status.HTTP_405_METHOD_NOT_ALLOWED)


class OrderViewSet(viewsets.ViewSet):
    serializer_class = OrderSerializer

    def create(self, request):
        user = request.user
        try:
            cart = Cart.objects.get(user=user)
        except Cart.DoesNotExist:
            return Response({"detail": "Cart not found."}, status=status.HTTP_404_NOT_FOUND)

        order = Order.objects.create(user=user)
        for item in cart.cartitem_set.all():
            OrderItem.objects.create(order=order, product=item.product, quantity=item.quantity)
        cart.cartitem_set.all().delete()  # Очистка корзины
        return Response(OrderSerializer(order).data, status=status.HTTP_201_CREATED)
