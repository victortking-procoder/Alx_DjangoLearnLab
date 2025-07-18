from django.shortcuts import render
from .models import Book, Library
from django.views.generic import DetailView, TemplateView

# Create your views here.
def book_list(request):
    books = Book.objects.all()
    context = {'books': books}
    return render(request, 'relationship_app/list_books.html', context)

class BookDetailView(DetailView, TemplateView):
    model = Library
    template_name = 'relationship_app/library_detail.html'
    context_object_name = 'library'