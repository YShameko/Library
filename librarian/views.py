from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.

def add_book(request): # додати нову книгу. може лише "бібліотекар"
    return HttpResponse("Hello! Add Book Page")

def inventory(request): # перевірити залишки по книгах - які є в бібліотеці, які "на руках"
    return HttpResponse("Inventory Page")

def send_reminder(request): # надіслати нагадування користувачам
    return HttpResponse("Send Reminder Page")
