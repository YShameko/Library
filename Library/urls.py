"""
URL configuration for Library project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include

import client
from client import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', client.views.index, name='home_page'),  # check again!
    path('about/', client.views.about, name='about_page'),  # check again!
    path('client/', include('client.urls')),

    path('librarian/', include('librarian.urls')),
    path('login', client.views.login, name='login'),
    path('logout', client.views.logout, name='logout'),
    path('register', client.views.register, name='register'),
]
