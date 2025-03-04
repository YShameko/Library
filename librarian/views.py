import datetime
from functools import wraps

from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from book.models import Books, Borrowed
from librarian import forms
from librarian.utils import send_reminders_to_users
from .forms import AddAuthorForm, AddGenreForm, AddPublisherForm

# --------------------------------------------------------------------------------------------------------------
def is_librarian(func_, request):
    @wraps(func_)
    def wrapped(*args, **kwargs):
        if request.user.groups.get("name") == "librarian":
            return func_(*args, **kwargs)
        else:
            return redirect("/")
    return wrapped
# --------------------------------------------------------------------------------------------------------------
# Create your views here.

@login_required(login_url="/")
def add_book(request): # Додати нову книгу. може лише "бібліотекар"
    if request.method == 'GET':
        new_book = forms.AddBookForm()
        return render(request, "add_book.html", {'add_book_form': new_book})
    else:
        add_book_form = forms.AddBookForm(request.POST)
        if add_book_form.is_valid():
            new_book = Books(**add_book_form.cleaned_data)
            new_book.save()
            msg = "Нову книгу <b>" + new_book.title + "</b> додано в нашу бібліотеку!"
            msg += "<br>Додамо ще <a href='/librarian/add_book'>книгу</a>? "
            msg += "Чи перейдемо в <a href='/client/profile'>особистий кабінет</a>?"
            return HttpResponse(msg)

@login_required(login_url="/")
def inventory(request): # перевірити залишки по книгах - які є в бібліотеці, які "на руках"
    if request.method == 'GET':
        inv_date = datetime.date.today()
        books = Books.objects.all()

        for book in books:
            borrowed_qty = Borrowed.objects.filter(book_id=book, status="reader").count()
            book.borrowed_qty = borrowed_qty
            book.available_qty = book.quantity - borrowed_qty

        return render(request, "inventory.html", {'books': books, 'inv_date': inv_date})
    else:
        pass

@login_required(login_url="/")
def send_reminder(request): # надіслати нагадування користувачам
    if request.method == 'GET':
        reminder_date = datetime.date.today() + datetime.timedelta(days=3)
        books_to_remind = Borrowed.objects.filter(to_date__lt=reminder_date).all()
        return render(request, "send_reminder.html", {'books': books_to_remind})
    else:
        reminders_list = request.POST.getlist("send_reminder")
        msg_sent = send_reminders_to_users(request, reminders_list)
        return render(request, "send_reminder_status.html", {'messages': msg_sent})

@login_required(login_url="/")
def borrow_confirm(request):
    if request.method == 'GET':
        books_to_borrow = Borrowed.objects.filter(status="reader", confirmed=False).all()
        return render(request, "confirm_borrow.html", {'books': books_to_borrow})
    else:
        borrowed_books_ids = request.POST.getlist("confirmed")
        for book in borrowed_books_ids:
            book_to_confirm = Borrowed.objects.get(id=book)
            book_to_confirm.confirmed = True
            book_to_confirm.save()
        msg = "Видачу книг підтверджено!"
        user_group = request.user.groups.first().name
        return render(request, "msg_board.html", {'message': msg, 'user_group': user_group})

@login_required(login_url="/")
def return_confirm(request):
    if request.method == 'GET':
        books_to_return = Borrowed.objects.filter(status="returned", confirmed=False).all()
        return render(request, "confirm_return.html", {'books': books_to_return})
    else:
        returned_books_ids = request.POST.getlist("confirmed")
        for book in returned_books_ids:
            book_to_confirm = Borrowed.objects.get(id=book)
            book_to_confirm.confirmed = True
            book_to_confirm.save()
        msg = "Повернення книг підтверджено!"
        user_group = request.user.groups.first().name
        return render(request, "msg_board.html", {'message': msg, 'user_group': user_group})

def add_author(request):
    if request.method == "POST":
        form = AddAuthorForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('add_book')
    else:
        form = AddAuthorForm()
    return render(request, 'add_author.html', {'form': form})

def add_genre(request):
    if request.method == "POST":
        form = AddGenreForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('add_book')
    else:
        form = AddGenreForm()
    return render(request, 'add_genre.html', {'form': form})

def add_publisher(request):
    if request.method == "POST":
        form = AddPublisherForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('add_book')
    else:
        form = AddPublisherForm()
    return render(request, 'add_publisher.html', {'form': form})