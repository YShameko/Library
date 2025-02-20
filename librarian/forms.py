from django import forms
from book.models import Authors, Genres, Publishers, Books
import datetime


class AddBookForm(forms.ModelForm):
    class Meta:
        model = Books
        fields = ['title', 'author', 'genre', 'publisher', 'publish_year', 'reception_date', 'cover', 'rating',
                  'quantity']

    title = forms.CharField(label="Назва книги", max_length=250, widget=forms.TextInput(attrs={'class': 'form-control'}))

    author = forms.ModelChoiceField(
        queryset=Authors.objects.all(),
        label="Автор",
        empty_label="Оберіть автора",
        widget=forms.Select(attrs={'class': 'form-control'})
    )

    genre = forms.ModelChoiceField(
        queryset=Genres.objects.all(),
        label="Жанр",
        empty_label="Оберіть жанр",
        widget=forms.Select(attrs={'class': 'form-control'})
    )

    publisher = forms.ModelChoiceField(
        queryset=Publishers.objects.all(),
        label="Видавництво",
        empty_label="Оберіть видавництво",
        widget=forms.Select(attrs={'class': 'form-control'})
    )

    publish_year = forms.IntegerField(label="Рік видання", widget=forms.NumberInput(attrs={'class': 'form-control'}))

    reception_date = forms.DateField(
        label="Дата надходження",
        widget=forms.DateInput(attrs={'type': 'date', 'class': 'form-control'})
    )

    cover = forms.ImageField(label="Обкладинка", required=False)

    rating = forms.FloatField(
        label="Рейтинг",
        initial=5,
        widget=forms.NumberInput(attrs={'class': 'form-control'})
    )

    quantity = forms.IntegerField(
        label="Кількість",
        initial=1,
        widget=forms.NumberInput(attrs={'class': 'form-control'})
    )
