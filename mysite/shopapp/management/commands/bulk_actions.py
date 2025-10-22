from collections.abc import Sequence
from django.contrib.auth.models import User
from django.core.management import BaseCommand
from shopapp.models import Product


class Command(BaseCommand):
    def handle(self, *args, **options):
        self.stdout.write("Start demo bulk")
        # info = [
        #     ('Smart 1', 199),
        #     ('Smart 2', 299),
        #     ('Smart 3', 399),
        # ]
        # products = [
        #     Product(name=name, price=price)
        #     for name, price in info
        # ]
        # result = Product.objects.bulk_create(products)
        #
        # for i in result:
        #     print(i)

        self.stdout.write(f"Done")
