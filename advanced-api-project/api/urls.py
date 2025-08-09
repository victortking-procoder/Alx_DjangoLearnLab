from django.urls import path
from .views import ListView
from .views import CreateView
from .views import DetailView
from .views import UpdateView
from .views import DeleteView

urlpatterns = [
    path('books/', ListView.as_view(), name='list-view'),
    path('books/', CreateView.as_view(), name='create-view'),
    path('books/<int:pk>/', DetailView.as_view(), name='detail-view'),
    path('books/<int:pk>/', UpdateView.as_view(), name='update-view'),
    path('books/<int:pk>/', DeleteView.as_view(), name='delete-view'),
]