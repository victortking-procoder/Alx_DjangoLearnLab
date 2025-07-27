from django.urls import path
from .views import list_books, LibraryDetailView, register, UserRegistration
from django.contrib.auth.views import LoginView, LogoutView
from . import views

urlpatterns = [
    path('books/', list_books, name='books'),
    path('book_detail/<int:pk>/', LibraryDetailView.as_view(), name='book_detail'),
    path('register', UserRegistration.as_view(), name=register),
    path('login/', LoginView.as_view(template_name='relationship_app/login.html'), name='login'),
    path('logout/', LogoutView.as_view(template_name='relationship_app/logout.html', name='logout')),
    path('reg/', views.register, name='reg')
]