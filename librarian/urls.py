from django.urls import path

from . import views

urlpatterns = [
    path('add_book/', views.add_book, name='add_book_page'),
    path('inventory/', views.inventory, name='inventory_page'),
    path('send_reminder/', views.send_reminder, name='send_reminder_page'),
    path('confirm_return/', views.confirm_return, name='confirm_return_page'),

]
