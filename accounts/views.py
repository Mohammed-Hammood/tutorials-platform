from django.shortcuts import render, redirect
from django.contrib.auth import logout, login, authenticate
from .forms import NewUserForm
from django.contrib import messages
from django.contrib.auth import get_user_model 
from django.contrib.auth.forms import AuthenticationForm


def login_view(request):
    if request.method == "POST":
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                messages.info(request, f"You are now logged in as {username}.")
                return redirect("accounts:profile")
            else:
                messages.error(request, "Invalid username or password.")
        messages.error(request, "Invalid username or password.")
    context = {
        "form": AuthenticationForm()
    }
    return render(request, "accounts/login.html", context)


def register_view(request):
    if request.method == "POST":
        form = NewUserForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, "Registration successful.")
            return redirect("products:home")
        messages.error(
            request, "Unsuccessful registration. Invalid information.")
    form = NewUserForm()
    return render(request=request, template_name="accounts/register.html", context={"form": form})


def logout_view(request):
    logout(request)
    return redirect("accounts:login")


def profile_view(request, username:str):
    User = get_user_model()
    try:
        user = User.objects.get(username=username)
    except User.DoesNotExist:
        return render(request, 'not-found.html')
    context = {
        "user": user
    }
    return render(request, "accounts/profile.html", context)