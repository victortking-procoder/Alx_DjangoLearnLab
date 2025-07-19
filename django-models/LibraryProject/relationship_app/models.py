from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Author(models.Model):
    name = models.CharField()

    def __str__(self):
        return self.name

class Book(models.Model):
    title = models.CharField()
    author = models.ForeignKey(Author, on_delete=models.CASCADE, related_name='books')

    def __str__(self):
        return self.title

class Library(models.Model):
    name = models.CharField()
    books = models.ManyToManyField(Book, related_name='libraries')

    def __str__(self):
        return self.name

class Librarian(models.Model):
    name = models.CharField()
    library = models.OneToOneField(Library, on_delete=models.CASCADE)

    def __str__(self):
        return self.name

class UserProfile(models.Model):
    class RoleChoices(models.TextChoices):
        ADMIN = 'Admin', 'Admin'
        LIBRARIAN = 'Librarian', 'Librarian'
        MEMBER = 'Member', 'Member'

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    role = models.CharField(max_length=100, choices=RoleChoices.choices)

    def __str__(self):
        return f"{self.user.username} - {self.role}"