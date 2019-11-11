from django.contrib import messages, auth
from django.contrib.auth.models import User
from django.shortcuts import redirect
from django.shortcuts import render


def register(request):
    if request.method == 'POST':
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        username = request.POST['username']
        email = request.POST['email']
        password1 = request.POST['password']
        password2 = request.POST['password2']

        if password1 != password2:
            messages.error(request, 'Passwords do not match')
            return redirect('register')
        if User.objects.filter(username=username).exists():
            messages.error(request, f"Username {username} is already taken")
            return redirect('register')
        if User.objects.filter(email=email).exists():
            messages.error(request, f"Email {email} already exists")
            return redirect('register')
        user = User.objects.create_user(username=username, email=email, password=password1, first_name=first_name,
                                        last_name=last_name)
        user.save()
        auth.login(request, user)
        messages.success(request, f"You are logged in as {username}")
        return redirect('index')
    else:
        return render(request, 'accounts/register.html')


def login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = auth.authenticate(username=username, password=password)
        if user is not None:
            auth.login(request, user)
            messages.success(request, 'You are not logged in')
            return redirect('dashboard')
        else:
            messages.error(request, 'Invalid credentials')
            return redirect('login')
    else:
        return render(request, 'accounts/login.html')


def logout(request):
    return redirect('index')


def dashboard(request):
    return render(request, 'accounts/dashboard.html')
