from .models import Author, Book, Library

author = Author.objects.get(id=1)
author.books.all()

library = Library.objects.get(id=1)
library.books.all()