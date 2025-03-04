import datetime

from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.db.models import Q

from book.models import Books, Borrowed, Reviews, Authors, Genres
from client import forms
from client.forms import SelectBookForm
from client.models import FavGenres, FavAuthors
from client.utils import available_books

# --------------------------------------------------------------------------------------------------------------
# Create your views here.
def index(request):
    if request.user.is_authenticated:
        return redirect('client/profile/')
    else:
        return render(request, 'index.html')

def about(request):
    if request.user.is_authenticated:
        user_group = request.user.groups.first().name
    else:
        user_group = 'anonymous'
    return render(request, 'about.html', {'user_group': user_group})

@login_required(login_url='/')
def profile(request):
    if request.method == 'GET':
        my_books = Borrowed.objects.filter(user=request.user, status="reader").all()
        prev_books = Borrowed.objects.filter(user=request.user, status="returned").all()
        fav_authors = FavAuthors.objects.filter(user=request.user)
        fav_genres = FavGenres.objects.filter(user=request.user)
        user_group = request.user.groups.first().name
        return render(request, 'profile.html',{'user':request.user, 'my_books':my_books,
                                        'prev_books':prev_books, 'fav_authors':fav_authors, 'fav_genres':fav_genres,
                                               'user_group':user_group})
    else:
        return render(request, 'profile.html')

@login_required(login_url='/')
def edit_profile(request):
    if request.method == 'GET':
        init_data = {'first_name': request.user.first_name, 'last_name': request.user.last_name,
                     'email': request.user.email,}
        edit_profile_form = forms.UpdateProfileForm(initial=init_data)
        return render(request, 'edit_profile.html', {'edit_profile_form': edit_profile_form})
    else:
        edit_profile_form = forms.UpdateProfileForm(request.POST)
        if edit_profile_form.is_valid():
            updated_profile = User.objects.get(pk=request.user.id)
            updated_profile.first_name = edit_profile_form.cleaned_data['first_name']
            updated_profile.last_name = edit_profile_form.cleaned_data['last_name']
            updated_profile.email = edit_profile_form.cleaned_data['email']
            updated_profile.save()
        return redirect('/client/profile/')

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
        user_group = request.user.groups.first().name
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
            return render(request, 'books.html', context={'form': form, 'books': books_to_borrow,
                                                          'title': title, 'user_group': user_group})
        else:
            the_book = Books.objects.get(id=book_id)
            return render(request, 'borrow_book.html', context={'book': the_book, 'user_group': user_group})
    else:
        borrowed_book = Borrowed()
        borrowed_book.user = User.objects.get(pk=request.user.id)
        borrowed_book.book = Books.objects.get(id=book_id)
        borrowed_book.from_date = datetime.date.today()
        borrowed_book.to_date = request.POST.get('to_date')
        borrowed_book.status = "reader"
        borrowed_book.confirmed = False
        borrowed_book.save()
        return redirect('/client/profile')

@login_required(login_url="/")
def return_books(request): # повернути книгу
    if request.method == 'GET':
        my_books = Borrowed.objects.filter(user=request.user, status="reader").all()
        return render(request, 'return_book.html', context={'books': my_books})

@login_required(login_url='/')
def return_the_book(request, book_id):
    if request.method == 'GET':
        the_book = Borrowed.objects.filter(book_id=book_id, user=request.user, status="reader").first()
        the_book.status = "returned"
        the_book.save()
        msg = "Ви успішно повернули книгу: <b>" + the_book.book.title + "</b>"
        msg += "<br><br>Але бібліотекар ще має підтвердити, що все гаразд із книгою :)"
        return HttpResponse(msg)

@login_required(login_url="/")
def suggest_book(request): # отримати рекомендацію, що почитати ще
    if request.method == 'GET':
        user_borrowed_books = Borrowed.objects.filter(user=request.user).values_list('book_id', flat=True)
        user_fav_authors = FavAuthors.objects.filter(user=request.user).values_list('author_id', flat=True)
        user_fav_genres = FavGenres.objects.filter(user=request.user).values_list('genre_id', flat=True)
        # Books: haven't read yet + favourites authors or genres
        book_filter = ~Q(id__in=user_borrowed_books)  # Виключаємо вже взяті книги
        if fav_authors or fav_genres:
            book_filter &= Q(author_id__in=user_fav_authors) | Q(
                genre_id__in=user_fav_genres)

        top_books = Books.objects.filter(book_filter).order_by('-rating')[:5]
        return render(request, "suggestion.html", {'books': top_books})

    else: pass

def book_rating(request, book_id=None):
    if request.user.is_authenticated:
        user_group = request.user.groups.first().name
    else:
        user_group = 'anonymous'
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

            title = 'Тут показані усі книги у нашій бібліотеці'
            return render(request, 'books.html', context={'form': form, 'books': books, 'title': title,
                                                          'user_group': user_group})
        else:
            the_book = Books.objects.get(id=book_id)
            reviews = Reviews.objects.filter(book=the_book).all()
            return render(request, 'about_book.html', context={'book': the_book, 'reviews': reviews,
                                                               'user_group': user_group})

    else:
        pass

@login_required(login_url="/")
def fav_authors(request):
    user = request.user
    all_authors = Authors.objects.all()
    fav_authors = Authors.objects.filter(favauthors__user=user)

    if request.method == "POST":
        selected_authors = request.POST.getlist("fav_authors")
        FavAuthors.objects.filter(user=user).delete()
        for author_id in selected_authors:
            author = Authors.objects.get(id=author_id)
            FavAuthors.objects.create(user=user, author=author)
        return redirect("/client/profile/")

    return render(request, "fav_authors.html", {"authors": all_authors, "fav_authors": fav_authors})

@login_required(login_url="/")
def fav_genres(request):
    user = request.user
    all_genres = Genres.objects.all()
    fav_genres = Genres.objects.filter(favgenres__user=user)

    if request.method == "POST":
        selected_genres = request.POST.getlist("fav_genres")
        FavGenres.objects.filter(user=user).delete()
        for genre_id in selected_genres:
            genre = Genres.objects.get(id=genre_id)
            FavGenres.objects.create(user=user, genre=genre)
        return redirect("/client/profile/")

    return render(request, "fav_genres.html", {"genres": all_genres, "fav_genres": fav_genres})
