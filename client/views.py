from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required

from client import forms

# Create your views here.
def index(request):
    return render(request, 'index.html')

def about(request):
    return render(request, 'about.html')

@login_required
def profile(request):
    return HttpResponse('Profile Page')

def register(request):
    if request.method == 'GET':
        register_form = forms.RegisterForm()
        return render(request, 'register.html', context={'register_form': register_form})
    else:
        register_form = forms.RegisterForm(request.POST)
        if register_form.is_valid():
            created_user = register_form.save()
            client_role = 'client'
            created_user.groups.add(client_role)
            created_user.save()
            message = "A new user: <b><i>" + register_form.cleaned_data['username'] + "</i></b> was successfully created!"
            message += "<br><br>Welcome!<br> Now you can <a href='/'>login</a> into your new account."
            return HttpResponse(message)
        else:
            return HttpResponse(register_form.errors)

def login_handler(request):
    user = User.objects.create_user()
    user.save()
    login_form = forms.LoginForm()
    if request.method == 'POST':
        login_form = forms.LoginForm(request.POST)
        if login_form.is_valid():
            username = login_form.cleaned_data['username']
            password = login_form.cleaned_data['password']
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return HttpResponse("You are now logged in")
        else:
            return redirect('/login/', messages.error(request, 'Invalid username or password.'))

    return HttpResponse('Login Page')

@login_required
def logout_handler(request):
    logout(request)
    return HttpResponse("You are logged out now")

@login_required
def review_book(request): # написати рецензію на книгу
    if request.method == 'GET':
        return render(request, 'review_book.html', context={})

@login_required
def borrow_book(request): # взяти книгу в бібліотеці
    if request.method == 'GET':
        return render(request, 'borrow_book.html', context={})
    else:
        pass

@login_required
def return_book(request): # повернути книгу
    return HttpResponse('Return Book Page')

def suggest_book(request): # отримати рекомендацію, що почитати ще
    return HttpResponse('Suggest Book Page')

@login_required
def book_rating(request):
    return HttpResponse('Book Rating Page')