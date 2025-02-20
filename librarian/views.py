import datetime
from functools import wraps

from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from book import models
from book.models import Books, Borrowed
from librarian import forms
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
def add_book(request): # додати нову книгу. може лише "бібліотекар"
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
            borrowed_qty = Borrowed.objects.filter(book_id=book, closed=False).count()
            book.borrowed_qty = borrowed_qty
            book.available_qty = book.quantity - borrowed_qty

        return render(request, "inventory.html", {'books': books, 'inv_date': inv_date})
    else:
        pass

@login_required(login_url="/")
def send_reminder(request): # надіслати нагадування користувачам
    if request.method == 'GET':
        reminder_date = datetime.date.today() + datetime.timedelta(days=3)
        users_to_notify = Borrowed.objects.filter(to_date__lt=reminder_date).all()
        return render(request, "send_reminder.html", {'books': users_to_notify})
    else:
        users_to_notify = request.POST
        send_reminders_to_users(request, users_to_notify)
    return HttpResponse("Send Reminder Page")

def send_reminders_to_users(request, users_to_notify):
    for user in users_to_notify:
        user.message_status = True
    return render(request, "send_reminder_status.html", {'users': users_to_notify})

@login_required(login_url="/")
def confirm_return(request):
    if request.method == 'GET':
        books_to_return = Borrowed.objects.filter(closed=False).filter(ready_to_return=True).all()
        return render(request, "confirm_return.html", {'books': books_to_return})
    else:
        pass