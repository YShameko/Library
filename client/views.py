import datetime
import client.utils as utils

from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required

from book.models import Books, Borrowed, Reviews
from client import forms
from client.forms import SelectBookForm
from client.models import FavGenres, FavAuthors
from client.utils import available_books

# --------------------------------------------------------------------------------------------------------------
# Create your views here.
def index(request):
    return render(request, 'index.html')

def about(request):
    return render(request, 'about.html')

@login_required
def profile(request):
    if request.method == 'GET':
        my_books = Borrowed.objects.filter(user_id=request.user, closed=False, ready_to_return=False).all()
        fav_authors = FavAuthors.objects.filter(user_id=request.user)
        fav_genres = FavGenres.objects.filter(user_id=request.user)
        return render(request, 'profile.html',{'user':request.user, 'my_books':my_books,
                                               'fav_authors':fav_authors, 'fav_genres':fav_genres})
    else:
        return render(request, 'profile.html')

def register(request):
    if request.method == 'GET':
        register_form = forms.RegisterForm()
        return render(request, 'register.html', context={'register_form': register_form})
    else:
        register_form = forms.RegisterForm(request.POST)
        if register_form.is_valid():
            new_client = register_form.save()
            new_client.groups.add(register_form.cleaned_data['user_type'])
            new_client.save()
            message = "Вітання! Новий користувач: <b><i>" + register_form.cleaned_data['username'] + "</i></b> був доданий!"
            message += "<br><br>Тепер ти можеш <a href='/'>увійти</a> в свій новий акаунт."
            return HttpResponse(message)
        else:
            return HttpResponse(register_form.errors)

def login_handler(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('/client/profile/')
        else:
            return redirect('/', messages.error(request, 'Invalid username or password.'))

    return redirect('/client/profile/')

@login_required(login_url="/")
def logout_handler(request):
    logout(request)
    return redirect('/')

@login_required(login_url="/")
def review_book(request, book_id=None): # написати рецензію на книгу
    if request.method == 'GET':
        if book_id is None:
            form = SelectBookForm(request.GET or None)
            books = Books.objects.all()
            if form.is_valid():
                author = form.cleaned_data.get('author')
                genre = form.cleaned_data.get('genre')

                if author:
                    books = books.filter(author=author)
                if genre:
                    books = books.filter(genre=genre)

            title = 'Обери книгу, про яку хочеш написати відгук'
            return render(request, 'books.html', context={'form': form, 'books': books, 'title': title})
        else:
            the_book = Books.objects.get(id=book_id)
            return render(request, 'review_book.html', context={'book': the_book})
    else:
        my_review = Reviews()
        my_review.user = User.objects.get(pk=request.user.id)
        my_review.book = Books.objects.get(id=book_id)
        my_review.rating = float(request.POST.get('rating'))
        my_review.text = request.POST.get('text')
        my_review.date = datetime.date.today()
        my_review.save()
        # Also changing current rating for the book
        the_book = Books.objects.get(id=book_id)
        the_book.rating = (the_book.rating + float(request.POST.get('rating'))) / 2
        the_book.save()
        return HttpResponse('Дякуємо за відгук!')

@login_required(login_url="/")
def borrow_book(request, book_id=None): # взяти книгу в бібліотеці
    if request.method == 'GET':
        if book_id is None:
            form = SelectBookForm(request.GET or None)
            books = Books.objects.all()
            if form.is_valid():
                author = form.cleaned_data.get('author')
                genre = form.cleaned_data.get('genre')

                if author:
                    books = books.filter(author=author)
                if genre:
                    books = books.filter(genre=genre)

            title = 'Обери книгу, яку хочеш прочитати'
            # Remove from the list of books those which are not available now
            books_to_borrow = available_books(books)
            return render(request, 'books.html', context={'form': form, 'books': books_to_borrow, 'title': title})
        else:
            the_book = Books.objects.get(id=book_id)
            return render(request, 'borrow_book.html', context={'book': the_book})
    else:
        borrowed_book = Borrowed()
        borrowed_book.user = User.objects.get(pk=request.user.id)
        borrowed_book.book = Books.objects.get(id=book_id)
        borrowed_book.from_date = datetime.date.today()
        borrowed_book.to_date = request.POST.get('to_date')
        borrowed_book.closed = False
        borrowed_book.ready_to_return = False
        borrowed_book.save()
        return redirect('/client/profile')

@login_required(login_url="/")
def return_books(request): # повернути книгу
    if request.method == 'GET':
        my_books = Borrowed.objects.filter(user_id=request.user.id).filter(closed=False).all()
        return render(request, 'return_book.html', context={'books': my_books})

def return_the_book(request, book_id):
    if request.method == 'GET':
        the_book = Borrowed.objects.filter(book_id=book_id).filter(user_id=request.user.id).filter(closed=False).first()
        the_book.ready_to_return = True
        the_book.save()
        msg = "Ви успішно повернули книгу: <b>" + the_book.book.title + "</b>"
        msg += "<br><br>Але бібліотекар ще має підтвердити, що все гаразд із книгою :)"
        return HttpResponse(msg)

def suggest_book(request): # отримати рекомендацію, що почитати ще
    return render(request, "suggestion.html")

# @login_required(login_url="/")
def book_rating(request):
    if request.method == 'GET':
        form = SelectBookForm()
        books = Books.objects.all()
        if form.is_valid():
            author = form.cleaned_data.get('author')
            genre = form.cleaned_data.get('genre')
            if author:
                books = books.filter(author=author)
            if genre:
                books = books.filter(genre=genre)

        title = 'Тут показані усі книги у нашій бібліотеці'
        return render(request, 'books.html', context={'form': form, 'books': books, 'title': title})
    else:
        pass