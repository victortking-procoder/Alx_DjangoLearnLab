Command used to delete the Book instance

Book.objects.filter(title="Ninteen Eighty-Four").delete()

Output: (1, {'bookshelf.Book': 1})

Output while trying to retieve book
<//QuerySet []>