from django.test import TestCase
from django.contrib.auth.models import User
from .models import Category, Product, Cart, CartItem


class ShopTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="testuser", password="testpass")
        self.category = Category.objects.create(name="Шубы")
        self.product = Product.objects.create(
            name="Меховая шуба",
            description="Теплая и стильная шуба.",
            price=299.99,
            category=self.category,
            characteristics={"цвет": "черный", "размер": "M"},
        )
        self.cart = Cart.objects.create(user=self.user)

    def test_add_product_to_cart(self):
        cart_item = CartItem.objects.create(cart=self.cart, product=self.product, quantity=1)
        self.assertEqual(cart_item.cart, self.cart)
        self.assertEqual(cart_item.product, self.product)
        self.assertEqual(cart_item.quantity, 1)

    def test_order_creation(self):
        cart_item = CartItem.objects.create(cart=self.cart, product=self.product, quantity=1)
        order = Order.objects.create(user=self.user, total_price=self.product.price)
        OrderItem.objects.create(order=order, product=self.product, quantity=1)
        self.assertEqual(order.user, self.user)
        self.assertEqual(order.total_price, self.product.price)
