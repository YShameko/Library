from django.urls import path

from . import views

urlpatterns = [
    path('add_book/', views.add_book, name='add_book_page'),
    path('inventory/', views.inventory, name='inventory_page'),
    path('send_reminder/', views.send_reminder, name='send_reminder_page'),
    path('confirmation/borrow/', views.borrow_confirm, name='confirm_borrow_page'),
    path('confirmation/return/', views.return_confirm, name='confirm_return_page'),
    path('add_author/', views.add_author, name='add_author'),
    path('add_genre/', views.add_genre, name='add_genre'),
    path('add_publisher/', views.add_publisher, name='add_publisher'),
]
