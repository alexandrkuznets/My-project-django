from django.contrib.sitemaps import Sitemap
from .models import Product


class ShopSitemap(Sitemap):
    changefreq = "never"
    priority = 0.5

    def items(self):
        return Product.objects.order_by("-created_at")

