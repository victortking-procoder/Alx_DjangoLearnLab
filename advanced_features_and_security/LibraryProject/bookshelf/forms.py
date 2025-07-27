# myapp/forms.py
from django import forms
from .models import Post

class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['title', 'content']

# LibraryProject/bookshelf/forms.py
from django import forms
from .models import Book # Keep this for BookForm

# Definition of the BookForm (from previous steps)
class BookForm(forms.ModelForm):
    class Meta:
        model = Book
        fields = ['title', 'author_name', 'publication_date', 'isbn']

# --- New: Definition of ExampleForm ---
class ExampleForm(forms.Form):
    """
    A simple example form to demonstrate form handling with form_example.html.
    This form doesn't necessarily map directly to a model.
    """
    your_name = forms.CharField(label='Your Name', max_length=100, required=True)
    your_email = forms.EmailField(label='Your Email', required=True)
    message = forms.CharField(label='Your Message', widget=forms.Textarea, required=False)
    newsletter_signup = forms.BooleanField(label='Sign up for newsletter?', required=False)