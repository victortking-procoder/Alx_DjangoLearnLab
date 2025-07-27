# myapp/views.py
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required, permission_required
from django.http import HttpResponseForbidden
from .models import Post
from .forms import PostForm # We'll create this form next

# Helper function for a forbidden response - useful with raise_exception=True
def forbidden_view(request):
    return HttpResponseForbidden("<h1>403 Forbidden: You do not have permission to access this page.</h1>")

@login_required
@permission_required('bookshelf.can_view', raise_exception=True)
def post_list(request):
    """
    Displays a list of all posts. Requires 'myapp.can_view' permission.
    """
    posts = Post.objects.all()
    return render(request, 'post_list.html', {'posts': posts})

@login_required
@permission_required('bookshelf.can_create', raise_exception=True)
def post_create(request):
    """
    Allows creation of a new post. Requires 'myapp.can_create' permission.
    """
    if request.method == 'POST':
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user # Assign the current logged-in user as author
            post.save()
            return redirect('post_list')
    else:
        form = PostForm()
    return render(request, 'post_form.html', {'form': form, 'form_type': 'Create'})

@login_required
@permission_required('bookshelf.can_edit', raise_exception=True)
def post_edit(request, pk):
    """
    Allows editing an existing post. Requires 'myapp.can_edit' permission.
    Only the author can edit in this example, but the permission ensures general edit rights.
    """
    post = get_object_or_404(Post, pk=pk)
    # Optional: Further restrict editing to only the author of the post
    if post.author != request.user and not request.user.is_superuser:
        return HttpResponseForbidden("<h1>403 Forbidden: You can only edit your own posts.</h1>")

    if request.method == 'POST':
        form = PostForm(request.POST, instance=post)
        if form.is_valid():
            form.save()
            return redirect('post_list')
    else:
        form = PostForm(instance=post)
    return render(request, 'post_form.html', {'form': form, 'form_type': 'Edit'})

@login_required
@permission_required('bookshelf.can_delete', raise_exception=True)
def post_delete(request, pk):
    """
    Allows deleting a post. Requires 'myapp.can_delete' permission.
    """
    post = get_object_or_404(Post, pk=pk)
    if request.method == 'POST':
        post.delete()
        return redirect('post_list')
    return render(request, 'post_confirm_delete.html', {'post': post})