from django.contrib.auth.decorators import login_required, permission_required, user_passes_test
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.mixins import UserPassesTestMixin
from django.contrib.auth.views import LogoutView
from django.http import HttpRequest, HttpResponse, JsonResponse
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.urls import reverse, reverse_lazy
from django.views import View
from django.views.generic import TemplateView, CreateView, ListView, DetailView, UpdateView
from django.views.decorators.cache import cache_page
from .models import Profile
from .forms import ProfileForm
from django.utils.translation import gettext_lazy as _, ngettext
from random import random

class HelloView(View):
    welcome_message = _("welcome hello world")

    def get(self, request: HttpRequest) -> HttpResponse:
        items_str = request.GET.get("items") or 0
        items = int(items_str)
        products_line = ngettext(
            "one product",
            "{count} products",
            items,
        )
        products_line = products_line.format(count=items)
        return HttpResponse(
            f"<h1>{self.welcome_message}</h1>"
            f"\n<h2>{products_line}</h2>"
        )

class AboutMeView(TemplateView):
    template_name = "accounts/about-me.html"

    def get(self, request: HttpRequest) -> HttpResponse:
        profile = Profile.objects.get_or_create(user=request.user)
        form = ProfileForm
        context = {"form": form, "profile": profile}
        return render(request, self.template_name, context)

    def post(self, request: HttpRequest) -> HttpResponse:
        profile = Profile.objects.get_or_create(user=request.user)
        form = ProfileForm(request.POST, request.FILES, instance=profile[0])
        if form.is_valid():
            form.save()
            return redirect("accounts:about-me")
        context = {"form": form, "profile": profile}
        return render(request, self.template_name, context)

class ProfileListView(ListView):
    template_name = "accounts/profile_list.html"
    context_object_name = "users"
    queryset = Profile.objects.all()

class ProfileDetailsView(DetailView):
    template_name = "accounts/profile_details.html"
    context_object_name = "profile"
    queryset = Profile.objects.all()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        form = ProfileForm()
        context['current_user'] = self.request.user
        context['form'] = form
        return context

    def post(self, request: HttpRequest, *args, **kwargs) -> HttpResponse:
        profile = self.get_object()
        form = ProfileForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            form.save()
            return redirect("accounts:profile_details", pk=profile.pk)
        context = {"form": form, "profile": profile, "pk": profile.pk}
        return render(request, self.template_name, context)


class RegisterView(CreateView):
    form_class = UserCreationForm
    template_name = "accounts/register.html"
    success_url = reverse_lazy("accounts:about-me")

    def form_valid(self, form):
        response = super().form_valid(form)
        Profile.objects.create(user=self.object)
        username = form.cleaned_data.get("username")
        password = form.cleaned_data.get("password1")
        user = authenticate(self.request, username=username, password=password)
        login(request=self.request, user=user)

        return response

def login_view(request: HttpRequest):
    if request.method == "GET":
        if request.user.is_authenticated:
            return redirect('/admin/')
        return render(request, 'accounts/login.html')
    username = request.POST["username"]
    password = request.POST["password"]
    user = authenticate(request, username=username, password=password)
    if user is not None:
        login(request, user)
        return redirect('/admin')
    return render(request, 'accounts/login.html', {"error": "Invalid login credentials"})

def logout_view(request: HttpRequest):
    logout(request)
    return redirect(reverse('accounts:login'))

class MyLogoutViews(View):
    def get(self, request):
        logout(request)
        return redirect('accounts:login')
    # next_page = reverse_lazy("accounts:login")

@user_passes_test(lambda u: u.is_superuser)
def set_cookie_view(request: HttpRequest) -> HttpResponse:
    response = HttpResponse("Cookie set")
    response.set_cookie("fizz", "buzz", max_age=3600)
    return response

@cache_page(60 * 2)
def get_cookie_view(request: HttpRequest) -> HttpResponse:
    value = request.COOKIES.get("fizz", "default value")
    return HttpResponse(f"Cookie value: {value!r} + {random()}")

@permission_required("accounts:view_profile", raise_exception=True)
def set_session_view(request: HttpRequest) -> HttpResponse:
    request.session["foobar"] = "spameggs"
    return HttpResponse("Session set")

@login_required
def get_session_view(request: HttpRequest) -> HttpResponse:
    value = request.session.get("foobar", "default")
    return HttpResponse(f"Session value {value!r}")

class FooBarView(View):
     def get(self, request: HttpRequest) -> JsonResponse:
         return JsonResponse({"foo": "bar", "spam": "eggs"})