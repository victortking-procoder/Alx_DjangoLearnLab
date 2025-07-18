from django.urls import path
from .views import list_books, LibraryDetailView

urlpatterns = [
    path('books/', list_books, name='books'),
    path('book_detail/<int:pk>/', LibraryDetailView.as_view(), name='book_detail')
]