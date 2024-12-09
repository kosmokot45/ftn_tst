from rest_framework import serializers
from .models import Product, Category, Cart, Order, CartItem, OrderItem

# from .models import Cart, CartItem, Order, OrderItem, Product


class ProductsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ["id", "name", "description", "image", "price", "characteristics"]


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = "__all__"


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = "__all__"


# class CartSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Cart
#         fields = "__all__"


# class OrderSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Order
#         fields = "__all__"


class CategoryIDSerializer(serializers.Serializer):
    category_id = serializers.IntegerField(required=False)


#


class CartItemSerializer(serializers.ModelSerializer):
    product = ProductSerializer()

    class Meta:
        model = CartItem
        fields = ["product", "quantity"]


class CartSerializer(serializers.ModelSerializer):
    items = CartItemSerializer(source="cartitem_set", many=True)

    class Meta:
        model = Cart
        fields = ["items"]


class OrderItemSerializer(serializers.ModelSerializer):
    product = ProductSerializer()

    class Meta:
        model = OrderItem
        fields = ["product", "quantity"]


class OrderSerializer(serializers.ModelSerializer):
    items = OrderItemSerializer(source="orderitem_set", many=True)

    class Meta:
        model = Order
        fields = ["id", "user", "created_at", "items"]
