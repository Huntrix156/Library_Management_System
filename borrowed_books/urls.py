"""
URL configuration for library project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/6.0/topics/http/urls/
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
from django.urls import path
from borrowed_books import views

urlpatterns = [
    path('Addbook/',views.Addbook,name='Addbook'),
    path('Dashboard/',views.Dashboard,name='Dashboard'),
    path('base/',views.base,name='base'),
    path('BookCatalogue/',views.BookCatalogue,name='BookCatalogue'),
    path('book/<int:pk>/', views.BookDetail, name='BookDetail'),   # READ detail → /book/5/
    path('book/<int:pk>/edit/', views.EditBook, name='EditBook'),  # UPDATE → /book/5/edit/
    path('book/<int:pk>/delete/', views.DeleteBook, name='DeleteBook'), # DELETE → /book/5/delete/
    path('',views.index,name='index'),
    path('b/',views.b,name='b'),
]
