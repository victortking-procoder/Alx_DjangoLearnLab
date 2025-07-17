from .models import Author, Book, Library

author = Author.objects.get(name=author_name)
author.books.all()

library = Library.objects.get(name=library_name)
library.books.all()