from django.shortcuts import render
from .models import Book
from .models import Library
from django.views.generic.detail import DetailView
from django.views.generic import TemplateView

# Create your views here.
def list_books(request):
    books = Book.objects.all()
    context = {'books': books}
    return render(request, 'relationship_app/list_books.html', context)

class LibraryDetailView(DetailView, TemplateView):
    model = Library
    template_name = 'relationship_app/library_detail.html'
    context_object_name = 'library'