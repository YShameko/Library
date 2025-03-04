from django.urls import path

from . import views

urlpatterns = [
    path('profile/', views.profile, name='profile_page'),
    path('profile/fav_authors/', views.fav_authors, name='fav_authors'),
    path('profile/fav_genres/', views.fav_genres, name='fav_genres'),
    path('profile/edit/', views.edit_profile, name='edit_profile'),
    path('review_book/', views.review_book, name='review_book_page'),
    path('review_book/<book_id>', views.review_book, name='review_book_page'),
    path('borrow_book/', views.borrow_book, name='borrow_book_page'),
    path('borrow_book/<book_id>', views.borrow_book, name='borrow_book_page'),
    path('return_books/', views.return_books, name='return_book_page'),
    path('return_the_book/<book_id>', views.return_the_book, name='return_book_page'),
    path('suggest_book/', views.suggest_book, name='suggest_book_page'),
    path('book_rating/', views.book_rating, name='book_rating_page'),
    path('book_rating/<book_id>', views.book_rating, name='about_book_page'),
]
