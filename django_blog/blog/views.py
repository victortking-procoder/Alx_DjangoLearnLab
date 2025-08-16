from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django import forms

# Create your views here.

# Extend Django’s UserCreationForm to include email
class RegisterForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ["username", "email", "password1", "password2"]

def home_view(request):
    return render(request, "blog/base.html")


# Registration View
def register_view(request):
    if request.method == "POST":
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)  # Auto-login after registration
            return redirect("blog:profile")
    else:
        form = RegisterForm()
    return render(request, "blog/register.html", {"form": form})


# Login View
def login_view(request):
    if request.method == "POST":
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect("blog:profile")
    else:
        form = AuthenticationForm()
    return render(request, "blog/login.html", {"form": form})


# Logout View
def logout_view(request):
    logout(request)
    return redirect("blog:login")


# Profile View (requires login)
@login_required
def profile_view(request):
    if request.method == "POST":
        # allow user to update email
        email = request.POST.get("email")
        if email:
            request.user.email = email
            request.user.save()
    return render(request, "blog/profile.html")

