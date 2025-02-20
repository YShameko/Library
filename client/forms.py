from django import forms
from django.contrib.auth.models import User, Group

from book.models import Reviews
from client.models import UserProfile
from book.models import Authors, Genres, Books

class LoginForm(forms.Form):
    username = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class':'form-control'}))

class RegisterForm(forms.ModelForm):
    class Meta:
        username = forms.CharField(label="Твій username:", widget=forms.TextInput(attrs={'class': 'form-control'}))
        # to hide the password when user is typing it on the HTML-page
        password = forms.CharField(label="та пароль:", widget=forms.PasswordInput(attrs={'class': 'form-control'}))
        model = User
        fields = ['username', 'password', 'email', 'first_name', 'last_name', 'user_type']
        # fields += ['home_address', 'gender', 'phone_numer', 'role']
        widgets = { 'password': forms.PasswordInput(), }

    user_type = forms.ModelChoiceField(
        queryset=Group.objects.all(),
        label="Хто ти?",
        empty_label="обирай",
        widget=forms.Select(attrs={'class': 'form-control'})
        )

    def save(self, commit=True):
        user = super(RegisterForm, self).save(commit=False)
        user.set_password(self.cleaned_data['password'])
        if commit:
            user.save()
        return user

class UpdateProfileForm(forms.Form):
    first_name = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control'}))
    last_name = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control'}))
    email = forms.EmailField(widget=forms.TextInput(attrs={'class':'form-control'}))
    # password = forms.CharField(widget=forms.PasswordInput(attrs={'class':'form-control'}))

class SelectBookForm(forms.Form):
    author = forms.ModelChoiceField(queryset=Authors.objects.all(), label="Автор", required=False)
    genre = forms.ModelChoiceField(queryset=Genres.objects.all(), label="Жанр", required=False)
