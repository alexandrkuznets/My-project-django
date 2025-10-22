from http.client import responses
from string import ascii_letters

from django.conf import settings
from django.contrib.auth.models import User, Permission
from django.test import TestCase
from shopapp.utils import add_two_number
from django.urls import reverse
from random import choices
from .models import Product, Order


class AddTwoNumberTestCase(TestCase):
    def test_add_two_numbers(self):
        result = add_two_number(2, 3)
        self.assertEqual(result, 5)

# class ProductCreateViewTestCase(TestCase):
#
#     def setUp(self) -> None:
#         self.product_name = "".join(choices(ascii_letters, k=10))
#         Product.objects.filter(name=self.product_name).delete()
#
#     def test_create_view(self):
#         self.client.login(username='admin', password='123456')
#         response = self.client.post(
#             reverse("blogapp:product_form"),
#             {
#                 "name": self.product_name,
#                 "price": "123.45",
#                 "description": "A good table",
#                 "discount": "10",
#             }
#         )
#         self.assertRedirects(response, reverse("blogapp:products_list"))
#         self.assertTrue(
#             Product.objects.filter(name=self.product_name).exists()
#         )
#
# class ProductDetailsViewTestCase(TestCase):
#
#     @classmethod
#     def setUpClass(cls):
#         cls.product = Product.objects.create(name="Best Product")
#
#     @classmethod
#     def tearDownClass(cls):
#         cls.product.delete()
#
#     def test_get_product(self):
#         response = self.client.get(
#             reverse("blogapp:product_details", kwargs={"pk": self.product.pk})
#         )
#         self.assertEqual(response.status_code, 200)
#
#     def test_get_product_and_check_content(self):
#         response = self.client.get(
#             reverse("blogapp:product_details", kwargs={"pk": self.product.pk})
#         )
#         self.assertContains(response.status_code, self.product.name)
#
#
# class ProductListViewTestCase(TestCase):
#     fixtures = [
#         'users-fixture.json',
#         'products-fixture.json',
#     ]
#
#     def test_products(self):
#         response = self.client.get(reverse('blogapp:products_list'))
#
#         self.assertQuerySetEqual(
#             qs=Product.objects.filter(archived=False).all(),
#             value=(p.pk for p in response.context["products"]),
#             transform=lambda p: p.pk,
#         )
#
#         self.assertTemplateUsed(response, 'blogapp/article_list.html')
#
# class OrdersListViewTestCase(TestCase):
#
#     @classmethod
#     def setUpClass(cls):
#         cls.user = User.objects.create_user(username='Bob', password='qwerty')
#
#     @classmethod
#     def tearDownClass(cls):
#         cls.user.delete()
#
#     def setUp(self):
#         self.client.force_login(self.user)
#
#     def test_orders_view(self):
#         response = self.client.get(reverse("blogapp:orders_list"))
#         self.assertContains(response, "Orders")
#
#     def test_orders_view_not_authenticated(self):
#         self.client.logout()
#         response = self.client.get(reverse("blogapp:orders_list"))
#         self.assertEqual(response.status_code, 302)
#         self.assertIn(str(settings.LOGIN_URL), response.url)


class ProductsExportViewTestCase(TestCase):
    fixtures = [
        'products-fixture.json',
    ]

    def test_get_products_view(self):
        response = self.client.get(
            reverse("blogapp:products-export"),
        )
        self.assertEqual(response.status_code, 200)
        products = Product.objects.order_by("pk").all()
        expected_data = [
            {
                "pk": product.pk,
                "name": product.name,
                "price": str(product.price),
                "archived": product.archived,
            }
            for product in products
        ]
        products_data = response.json()
        self.assertEqual(
            products_data["products"],
            expected_data,
        )

class OrderDetailViewTestCase(TestCase):

    @classmethod
    def setUpClass(cls):
        cls.user = User.objects.create_user(username='Bob', password='qwerty')
        permission = Permission.objects.get(codename='view_order')
        cls.user.user_permissions.add(permission)

    @classmethod
    def tearDownClass(cls):
        cls.user.delete()

    def setUp(self):
        self.client.force_login(self.user)
        self.order = Order.objects.create(delivery_address="street", promocode="sale123", user=self.user)

    def tearDown(self):
        self.order.delete()


    def test_order_details(self):
        response = self.client.get(reverse("blogapp:order_details", kwargs={"pk": self.order.pk}))
        response_order = response.context["order"]
        self.assertContains(response, "Delivery address")
        self.assertContains(response, "Promocode")
        self.assertEqual(response_order.pk, self.order.pk)

class OrderExportTestCase(TestCase):
    fixtures = [
        'users-fixtures.json',
        'products-fixture.json',
        'orders-fixtures.json',
    ]
    @classmethod
    def setUpClass(cls):
        cls.user = User.objects.create_user(username='Bob', password='qwerty', is_staff=True)

    @classmethod
    def tearDownClass(cls):
        cls.user.delete()

    def setUp(self):
        self.client.force_login(self.user)


    def test_order_list(self):
        response = self.client.get(reverse("blogapp:orders-export"))
        self.assertEqual(response.status_code, 200)
        orders = Order.objects.order_by("pk").all()
        expected_data = [
            {
                "pk": order.pk,
                "delivery_address": order.delivery_address,
                "promocode": order.promocode,
                "user": order.user.pk,
                "products": order.products
            }
            for order in orders
        ]
        orders_data = response.json()
        self.assertEqual(
            orders_data["order"],
            expected_data,
        )
