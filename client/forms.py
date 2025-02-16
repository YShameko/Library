from django import forms
from django.contrib.auth.models import User

from client.models import UserProfile


class LoginForm(forms.Form):
    username = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class':'form-control'}))

class RegisterForm(forms.ModelForm):
    class Meta:
        # to hide the password when user is typing it on the HTML-page
        password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control'}))
        username = forms.CharField(widget=forms.TextInput(), help_text='')
        model = User
        fields = ['username', 'password', 'email', 'first_name', 'last_name']
        # fields += ['home_address', 'gender', 'phone_numer', 'role']
        widgets = {
            'password': forms.PasswordInput(),
        }

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
