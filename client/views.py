from django.http import HttpResponse
from django.shortcuts import render

# Create your views here.
def index(request):
    return render(request, 'index.html')

def about(request):
    return render(request, 'about.html')

def profile(request):
    return HttpResponse('Profile Page')

def register(request):
    return HttpResponse('Register Page')

def login(request):
    return HttpResponse('Login Page')

def logout(request):
    return HttpResponse('Logout Page')

def review_book(request): # написати рецензію на книгу
    return HttpResponse('Review Book Page')

def borrow_book(request): # взяти книгу в бібліотеці
    return HttpResponse('Borrow Book Page')

def return_book(request): # повернути книгу
    return HttpResponse('Return Book Page')

def suggest_book(request): # отримати рекомендацію, що почитати ще
    return HttpResponse('Suggest Book Page')

def book_rating(request):
    return HttpResponse('Book Rating Page')