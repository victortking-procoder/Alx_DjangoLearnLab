from rest_framework.test import APITestCase
from django.urls import reverse
from rest_framework import status
from django.contrib.auth import get_user_model
from .models import Book, Author

User = get_user_model()

class BookAPITestCase(APITestCase):
    def setUp(self):
        # Create a test user for authenticated requests
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        self.client.force_authenticate(user=self.user)
        self.client.login(user=self.user)
        
        # Create some sample data
        self.author1 = Author.objects.create(name='J.R.R. Tolkien')
        self.author2 = Author.objects.create(name='George Orwell')
        self.book1 = Book.objects.create(
            title='The Hobbit',
            publication_year=1937,
            author=self.author1
        )
        self.book2 = Book.objects.create(
            title='1984',
            publication_year=1949,
            author=self.author2
        )

    def test_list_books(self):
        """
        Ensure we can list books and the response data is correct.
        """
        response = self.client.get(reverse('list-view'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)
        self.assertEqual(response.data[0]['title'], 'The Hobbit')

    def test_create_book_authenticated(self):
        """
        Ensure an authenticated user can create a book.
        """
        self.client.force_authenticate(user=self.user)
        data = {
            'title': 'Animal Farm',
            'publication_year': 1945,
            'author': self.author2.id
        }
        response = self.client.post(reverse('create-view'), data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Book.objects.count(), 3)
        self.assertEqual(response.data['title'], 'Animal Farm')

def test_create_book_unauthenticated_fails(self):
    """
    Ensure an unauthenticated user cannot create a book.
    """
    self.client.force_authenticate(user=None)
    data = {
        'title': 'The Lord of the Rings',
        'publication_year': 1954,
        'author': self.author1.id
    }
    response = self.client.post(reverse('create-view'), data, format='json')
    self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)


def test_retrieve_book_detail(self):
    """
    Ensure we can retrieve a single book by its primary key.
    """
    response = self.client.get(reverse('detail-view', args=[self.book1.id]))
    self.assertEqual(response.status_code, status.HTTP_200_OK)
    self.assertEqual(response.data['title'], 'The Hobbit')

def test_update_book(self):
    """
    Ensure an authenticated user can update a book.
    """
    data = {'title': 'The Hobbit: An Unexpected Journey'}
    response = self.client.patch(reverse('update-view', args=[self.book1.id]), data, format='json')
    self.assertEqual(response.status_code, status.HTTP_200_OK)
    self.book1.refresh_from_db()
    self.assertEqual(self.book1.title, 'The Hobbit: An Unexpected Journey')

def test_delete_book(self):
    """
    Ensure an authenticated user can delete a book.
    """
    response = self.client.delete(reverse('delete-view', args=[self.book1.id]))
    self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
    self.assertEqual(Book.objects.count(), 1)

def test_filter_books_by_title(self):
    """
    Ensure filtering by title works correctly.
    """
    response = self.client.get(reverse('list-view') + '?title=1984')
    self.assertEqual(response.status_code, status.HTTP_200_OK)
    self.assertEqual(len(response.data), 1)
    self.assertEqual(response.data[0]['title'], '1984')

def test_search_books(self):
    """
    Ensure searching by title works correctly.
    """
    response = self.client.get(reverse('list-view') + '?search=Hobbit')
    self.assertEqual(response.status_code, status.HTTP_200_OK)
    self.assertEqual(len(response.data), 1)
    self.assertEqual(response.data[0]['title'], 'The Hobbit')

def test_ordering_books(self):
    """
    Ensure ordering by title works correctly.
    """
    # Order by title descending
    response = self.client.get(reverse('list-view') + '?ordering=-title')
    self.assertEqual(response.status_code, status.HTTP_200_OK)
    self.assertEqual(response.data[0]['title'], 'The Hobbit')
    self.assertEqual(response.data[1]['title'], '1984')