from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from accounts.models import User

def login_view(request):
    if request.method == "POST":
        email = request.POST.get("email")
        password = request.POST.get("password")
        user = authenticate(request, email=email, password=password)
        if user:
            login(request, user)
            return redirect('storage-dashboard')
        return render(request, 'accounts/login.html', {"error": "Invalid credentials"})
    return render(request, 'accounts/login.html')

def register_view(request):
    if request.method == "POST":
        email = request.POST.get("email")
        password = request.POST.get("password")
        re_password = request.POST.get("re_password")
        if password != re_password:
            return render(request, 'accounts/register.html', {"error": "Passwords do not match"})
        if User.objects.filter(email=email).exists():
            return render(request, 'accounts/register.html', {"error": "Email already registered"})
        user = User.objects.create_user(email=email, password=password)
        login(request, user)
        return redirect('storage-dashboard')
    return render(request, 'accounts/register.html')

def logout_view(request):
    logout(request)
    return redirect('login')
