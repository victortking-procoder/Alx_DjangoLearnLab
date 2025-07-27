# LibraryProject/bookshelf/views.py
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required, permission_required
from django.http import HttpResponseForbidden
from django.db.models import Q # For secure search queries
from django.contrib import messages # For displaying feedback messages
from .models import Book # Assuming Book model is defined in bookshelf/models.py
from .forms import ExampleForm
from .forms import BookForm

# --- Helper Function for Forbidden Access ---
def forbidden_view(request):
    """
    Renders a 403 Forbidden page. Used when permission_required
    decorator has raise_exception=True.
    """
    return HttpResponseForbidden("<h1>403 Forbidden: You do not have permission to access this page.</h1>")

# --- Book Management Views ---

@login_required
@permission_required('bookshelf.can_view', raise_exception=True)
def book_list(request):
    """
    Displays a list of all books, with an optional search functionality.
    Requires 'bookshelf.can_view' permission for access.
    Demonstrates secure input handling for search queries using Django ORM.
    """
    books = Book.objects.all()
    # Get and sanitize search query using .strip() to remove leading/trailing whitespace.
    # The ORM's filter() method correctly parameterizes input, preventing SQL injection.
    search_query = request.GET.get('q', '').strip()

    if search_query:
        # Use Q objects for complex OR queries across multiple fields.
        books = books.filter(
            Q(title__icontains=search_query) |
            Q(author_name__icontains=search_query) |
            Q(isbn__icontains=search_query)
        ).distinct() # Use distinct() to avoid duplicate results if a book matches multiple Q conditions

    context = {
        'books': books,
        'search_query': search_query, # Pass the sanitized query back to the template for display
        # Pass permission flags to the template for conditional rendering of buttons/links
        'can_add_book': request.user.has_perm('bookshelf.can_create'),
        'can_edit_book': request.user.has_perm('bookshelf.can_edit'),
        'can_delete_book': request.user.has_perm('bookshelf.can_delete'),
    }
    return render(request, 'bookshelf/book_list.html', context)

@login_required
@permission_required('bookshelf.can_create', raise_exception=True)
def book_add(request):
    """
    Allows authenticated users with 'bookshelf.can_create' permission to add new books.
    Django Forms handle automatic validation and sanitization of user input,
    preventing common vulnerabilities like XSS and ensuring data integrity.
    """
    if request.method == 'POST':
        form = BookForm(request.POST)
        if form.is_valid():
            book = form.save(commit=False) # Don't save to DB yet
            book.added_by = request.user # Assign the current logged-in user as the adder
            book.save() # Now save the book instance
            messages.success(request, f"Book '{book.title}' added successfully!")
            return redirect('book_list')
        else:
            # If form is invalid, errors will be in form.errors and rendered in template
            messages.error(request, "Please correct the errors in the form.")
    else:
        form = BookForm() # Empty form for GET requests

    return render(request, 'bookshelf/book_form.html', {'form': form, 'form_type': 'Add'})

@login_required
@permission_required('bookshelf.can_edit', raise_exception=True)
def book_edit(request, pk):
    """
    Allows authenticated users with 'bookshelf.can_edit' permission to edit existing books.
    Uses Django's ORM (get_object_or_404) for safe retrieval of the book instance by PK.
    Django Forms ensure secure handling of updated data.
    """
    book = get_object_or_404(Book, pk=pk) # Safely retrieves object by primary key

    # Optional: Implement an additional layer of security/business logic.
    # For example, only allow the user who added the book, or superusers, to edit it.
    # if book.added_by != request.user and not request.user.is_superuser:
    #     messages.error(request, "You can only edit books you have added.")
    #     return HttpResponseForbidden("<h1>403 Forbidden: You can only edit books you added.</h1>")

    if request.method == 'POST':
        form = BookForm(request.POST, instance=book)
        if form.is_valid():
            form.save() # Save the updated book instance
            messages.success(request, f"Book '{book.title}' updated successfully!")
            return redirect('book_list')
        else:
            messages.error(request, "Please correct the errors in the form.")
    else:
        form = BookForm(instance=book) # Pre-populate form with existing book data

    return render(request, 'bookshelf/book_form.html', {'form': form, 'form_type': 'Edit'})

@login_required
@permission_required('bookshelf.can_delete', raise_exception=True)
def book_delete(request, pk):
    """
    Allows authenticated users with 'bookshelf.can_delete' permission to delete books.
    The primary key (pk) is safely handled by get_object_or_404.
    Requires a POST request to confirm deletion, protecting against accidental deletions via GET.
    """
    book = get_object_or_404(Book, pk=pk) # Safely retrieves object by primary key

    if request.method == 'POST':
        # The {% csrf_token %} in the template protects this POST request
        book.delete()
        messages.success(request, f"Book '{book.title}' deleted successfully!")
        return redirect('book_list')

    # For GET request, display confirmation page
    return render(request, 'bookshelf/book_confirm_delete.html', {'book': book})

# --- Example Form View ---
@login_required # Example of a view potentially requiring login
def example_form_view(request):
    """
    View to demonstrate a generic form (ExampleForm) and secure input handling.
    This view shows how Django Forms handle cleaning and validation of arbitrary data.
    """
    if request.method == 'POST':
        form = ExampleForm(request.POST)
        if form.is_valid():
            # All data in form.cleaned_data is already cleaned, validated, and sanitized.
            # No need for manual escaping or type conversion for basic types.
            name = form.cleaned_data['your_name']
            email = form.cleaned_data['your_email']
            message = form.cleaned_data['message']
            newsletter = form.cleaned_data['newsletter_signup']

            # In a real application, you would now securely process this data:
            # - Save to database (using ORM)
            # - Send an email (using Django's email sending functions)
            # - Perform other business logic

            # For demonstration: Display a success message
            messages.success(request, f"Thank you, {name}! Your message has been received.")

            # Redirect after POST to prevent accidental form re-submission on refresh
            return redirect('example_form')
        else:
            # If form is invalid, form.errors will contain details, which the template renders.
            messages.error(request, "There were errors in your submission. Please check the form.")
    else:
        form = ExampleForm() # Create an empty form instance for GET requests

    return render(request, 'bookshelf/form_example.html', {'form': form})