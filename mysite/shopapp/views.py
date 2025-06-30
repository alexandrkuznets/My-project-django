from django.http import HttpResponse
from django.shortcuts import render
from timeit import default_timer
from  django.contrib.auth.models import Group
from .models import Product, Order


# Create your views here.

def shop_index(request):
    vacancies = [
        ("Manager", True),
        ("Director", True),
        ("Security", False),
        ("Consultant", False),
        ]
    products = [
        ("Laptop", 1999),
        ("Desktop", 2999),
        ("Smartphone", 999),
    ]
    context = {
        "time_running": default_timer(),
        "products": products,
        "vacancies": vacancies,
    }

    return render(request, "shopapp/shop-index.html", context=context)

def group_list(request):
    context = {
        "groups": Group.objects.prefetch_related('permissions').all(),
    }
    return render(request, "shopapp/groups-list.html", context=context)


def products_list(request: HttpResponse):
    context = {
        "products": Product.objects.all(),
    }
    return render(request, "shopapp/products-list.html", context=context)

def orders_list(request: HttpResponse):
    context = {
        "orders": Order.objects.select_related("user").prefetch_related('products').all(),
    }
    return render(request, "shopapp/orders-list.html", context=context)