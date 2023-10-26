from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from .forms import RegisterForm, LoginForm
from .models import UserDetails
from django.contrib.auth.hashers import make_password


from django.shortcuts import render
from django.http import HttpResponse


def index(request):
    return render(request, 'FrontEnd/index.html')


def user_login(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            user = authenticate(request
                                , username=form.cleaned_data['username'], password=form.cleaned_data['password'])
            if user:
                login(request, user)
                return redirect('/')
            else:
                form.add_error(None, 'Invalid login credentials')
    else:
        form = LoginForm()
    return render(request, 'FrontEnd/login.html', {'form': form})


def user_signup(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST, request.FILES)
        if form.is_valid():
            user = form.save(commit=False)
            user.password = make_password(form.cleaned_data['password'])
            user.save()
            return redirect('/login/')
    else:
        form = RegisterForm()
    return render(request, 'FrontEnd/signup.html', {'form': form})


def user_logout(request):
    logout(request)
    return redirect('/login/')