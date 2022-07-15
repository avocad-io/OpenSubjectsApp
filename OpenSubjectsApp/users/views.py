import re
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.forms import UserCreationForm


def login_user(request):
    next_url = request.GET.get('next')
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            if next_url:
                return redirect(next_url)
            else:
               return redirect('/')
        else:
            messages.success(request, "LOGIN ERROR")
            return render(request, 'users/login.html')  
    else:
        return render(request, 'users/login.html')

def logout_user(request):
    logout(request)
    messages.success(request, "You were logged out")
    return redirect('/')

def register_user(request):
    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data['username']
            password = form.cleaned_data['password1']
            user = authenticate(request, username=username, password=password)
            messages.success(request, "Registration successful!")
            return redirect('login_user')
    else:
        form = UserCreationForm()
    return render(request, 'users/register_user.html', {'form': form})