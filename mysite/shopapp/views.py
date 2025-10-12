from django.contrib.messages import success
from django.http import HttpResponse, HttpRequest, HttpResponseRedirect
from django.shortcuts import render, redirect, reverse, get_object_or_404
from timeit import default_timer
from  django.contrib.auth.models import Group
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin, UserPassesTestMixin
from django.views import View
from django.views.generic import TemplateView, ListView, DetailView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy

from .forms import ProductForm, OrderForm, GroupForm
from .models import Product, Order


# Create your views here.

class ShopIndexView(View):
    def get(self, request: HttpRequest) -> HttpResponse:
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

class GroupsListView(View):
    def get(self, request: HttpRequest) -> HttpResponse:
        context = {
            "form": GroupForm(),
            "groups": Group.objects.prefetch_related('permissions').all(),
        }
        return render(request, "shopapp/groups-list.html", context=context)

    def post(self, request: HttpRequest):
        form = GroupForm(request.POST)
        if form.is_valid():
            form.save()

        return redirect(request.path)


class ProductDetailsView(DetailView):
    template_name = "shopapp/products-details.html"
    model = Product
    context_object_name = "product"


class ProductsListView(ListView):
    template_name = "shopapp/products-list.html"
    context_object_name = "products"
    queryset = Product.objects.filter(archived=False)


class ProductCreateView(PermissionRequiredMixin, CreateView):
    permission_required = "shopapp.add_product"

    # def test_func(self):
    #     return self.request.user.is_superuser

    def form_valid(self, form):
        form.instance.created_by = self.request.user
        return super().form_valid(form)

    model = Product
    fields = "name", "price", "description", "discount"
    success_url = reverse_lazy("shopapp:products_list")


class ProductUpdateView(PermissionRequiredMixin, UserPassesTestMixin, UpdateView):
    def test_func(self):
        return self.request.user == self.get_object().created_by or self.request.user.is_superuser

    permission_required = "shopapp.change_product"
    model = Product
    fields = "name", "price", "description", "discount"
    template_name_suffix = "_update_form"

    def get_success_url(self):
        return reverse("shopapp:product_details", kwargs={"pk": self.object.pk},)


class ProductDeleteView(DeleteView):
    model = Product
    success_url = reverse_lazy("shopapp:products_list")

    def form_valid(self, form):
        success_url = self.get_success_url()
        self.object.archived = True
        self.object.save()
        return HttpResponseRedirect(success_url)


class OrderCreateView(CreateView):
    model = Order
    fields = "delivery_address", "promocode", "user", "products"
    success_url = reverse_lazy("shopapp:orders_list")


class OrderListView(LoginRequiredMixin, ListView):
    queryset = (
        Order.objects.select_related("user").prefetch_related('products')
    )


class OrderDetailView(PermissionRequiredMixin, DetailView):
    permission_required = "view_order"
    queryset = (
        Order.objects.select_related("user").prefetch_related('products')
    )

class OrderUpdateView(UpdateView):
    model = Order
    fields = "delivery_address", "promocode", "user", "products"
    template_name_suffix = "_update_form"

    def get_success_url(self):
        return reverse("shopapp:order_details", kwargs={"pk": self.object.pk}, )

class OrderDeleteView(DeleteView):
    model = Order
    success_url = reverse_lazy("shopapp:orders_list")
