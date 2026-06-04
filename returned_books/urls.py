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

from django.urls import path
from returned_books import views

urlpatterns = [
    # Existing
    path('Returned_books/', views.Returned_books, name='ReturnedBorrowed_books'),

    # Lending system
    path('lending/',                    views.LendingCatalogue, name='LendingCatalogue'),
    path('lending/lend/<int:pk>/',      views.LendBook,         name='LendBook'),
    path('lending/returned/<int:record_id>/', views.MarkReturned, name='MarkReturned'),
    path('lending/active/',             views.ActiveLendings,   name='ActiveLendings'),


]
