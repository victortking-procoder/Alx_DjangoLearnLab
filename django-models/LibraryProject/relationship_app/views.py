from django.shortcuts import render
from .models import Book, Library

# Create your views here.
def book_list(request):
    books = Book.objects.all()
    context = {'books': books}
    return render(request, 'list_books.html', context)