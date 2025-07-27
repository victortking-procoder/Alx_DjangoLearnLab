Command used to delete the Book instance

Book.objects.filter(title="Ninteen Eighty-Four").delete()

["book.delete", "from bookshelf.models import Book"]

Output: (1, {'bookshelf.Book': 1})

Output while trying to retieve book
<//QuerySet []>