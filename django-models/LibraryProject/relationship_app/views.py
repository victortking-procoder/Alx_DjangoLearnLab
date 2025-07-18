from django.shortcuts import render
from .models import Book
from .models import Library
from django.views.generic.detail import DetailView
from django.views.generic import TemplateView
from django.views.generic import CreateView
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login
from django.contrib.auth import logout
from django.urls import reverse_lazy
from django.contrib.auth.models import User

# Create your views here.
def list_books(request):
    books = Book.objects.all()
    context = {'books': books}
    return render(request, 'relationship_app/list_books.html', context)

class LibraryDetailView(DetailView, TemplateView):
    model = Library
    template_name = 'relationship_app/library_detail.html'
    context_object_name = 'library'

class UserRegistration(CreateView):
    form_class = UserCreationForm
    template_name = 'relationship_app/register.html'
    success_url = reverse_lazy('login')