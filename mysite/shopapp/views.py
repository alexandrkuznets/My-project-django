from django.http import HttpResponse
from django.shortcuts import render
from timeit import default_timer

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