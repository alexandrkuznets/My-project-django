from collections.abc import Sequence
from django.contrib.auth.models import User
from django.core.management import BaseCommand
from shopapp.models import Product
from django.db.models import Avg, Max, Min, Count

class Command(BaseCommand):
    def handle(self, *args, **options):
        self.stdout.write("Start demo agg")

        result = Product.objects.aggregate(
            Avg("price"),
            Min("price"),
            Max("price"),
            Count("price"),
        )
        print(result)

        self.stdout.write(f"Done")
