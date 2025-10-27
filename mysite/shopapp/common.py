from csv import DictReader
from io import TextIOWrapper
from django.contrib.auth.models import User
from shopapp.models import Product, Order


def save_csv_products(file, encoding):
    csv_file = TextIOWrapper(file, encoding=encoding)
    reader = DictReader(csv_file)
    products = [Product(**row) for row in reader]
    Product.objects.bulk_create(products)
    return products

def save_csv_orders(file, encoding):
    csv_file = TextIOWrapper(file, encoding=encoding)
    reader = DictReader(csv_file)
    orders = [Order(**row) for row in reader]
    admin = User.objects.filter(is_staff=True).first()
    for order in orders:
        order.user = admin
    Order.objects.bulk_create(orders)
    return orders
