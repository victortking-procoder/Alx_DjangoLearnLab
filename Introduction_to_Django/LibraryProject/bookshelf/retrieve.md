Command used in retrieving all attributes of the created Book instance

book = Book.objects.filter(title="1984")

for record in book:
    print(record.title, record.author, record.publication_year)

Output: 1984 George Orwell 1949