Command used to update title attribute of the Book instance

Book.objects.filter(title="1984").update(title="Ninteen Eighty-Four")

["book.title", "Nineteen Eighty-Four"]

Output: 1