# LibraryProject/bookshelf/views.py
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required, permission_required
from django.http import HttpResponseForbidden
from .models import Book
from .forms import BookForm

# Helper function for a forbidden response
def forbidden_view(request):
    return HttpResponseForbidden("<h1>403 Forbidden: You do not have permission to access this page.</h1>")

@login_required
@permission_required('bookshelf.can_view', raise_exception=True) # Changed: 'bookshelf.can_view'
def book_list(request):
    """
    Displays a list of all books. Requires 'bookshelf.can_view' permission.
    """
    books = Book.objects.all()
    context = {
        'books': books,
        'can_add_book': request.user.has_perm('bookshelf.can_create'),  # Changed: 'bookshelf.can_create'
        'can_edit_book': request.user.has_perm('bookshelf.can_edit'),    # Changed: 'bookshelf.can_edit'
        'can_delete_book': request.user.has_perm('bookshelf.can_delete'), # Changed: 'bookshelf.can_delete'
    }
    return render(request, 'bookshelf/book_list.html', context)


@login_required
@permission_required('bookshelf.can_create', raise_exception=True) # Changed: 'bookshelf.can_create'
def book_add(request):
    """
    Allows adding a new book. Requires 'bookshelf.can_create' permission.
    """
    if request.method == 'POST':
        form = BookForm(request.POST)
        if form.is_valid():
            book = form.save(commit=False)
            book.added_by = request.user
            book.save()
            return redirect('book_list')
    else:
        form = BookForm()
    return render(request, 'bookshelf/book_form.html', {'form': form, 'form_type': 'Add'})


@login_required
@permission_required('bookshelf.can_edit', raise_exception=True) # Changed: 'bookshelf.can_edit'
def book_edit(request, pk):
    """
    Allows editing an existing book. Requires 'bookshelf.can_edit' permission.
    """
    book = get_object_or_404(Book, pk=pk)
    # Optional: Further restrict editing to only the user who added it or superuser
    # if book.added_by != request.user and not request.user.is_superuser:
    #     return HttpResponseForbidden("<h1>403 Forbidden: You can only edit books you added.</h1>")

    if request.method == 'POST':
        form = BookForm(request.POST, instance=book)
        if form.is_valid():
            form.save()
            return redirect('book_list')
    else:
        form = BookForm(instance=book)
    return render(request, 'bookshelf/book_form.html', {'form': form, 'form_type': 'Edit'})


@login_required
@permission_required('bookshelf.can_delete', raise_exception=True) # Changed: 'bookshelf.can_delete'
def book_delete(request, pk):
    """
    Allows deleting a book. Requires 'bookshelf.can_delete' permission.
    """
    book = get_object_or_404(Book, pk=pk)
    if request.method == 'POST':
        book.delete()
        return redirect('book_list')
    return render(request, 'bookshelf/book_confirm_delete.html', {'book': book})