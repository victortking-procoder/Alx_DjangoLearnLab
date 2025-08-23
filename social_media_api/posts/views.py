from django.contrib.auth import get_user_model
from rest_framework import viewsets, permissions, filters
from rest_framework.exceptions import PermissionDenied
from .models import Post, Comment
from .serializers import PostSerializer, CommentSerializer
from .permissions import IsOwnerOrReadOnly

User = get_user_model()


class PostViewSet(viewsets.ModelViewSet):
    """
    CRUD for posts.
    - List & retrieve: public (read-only)
    - Create/Update/Delete: authenticated + owner-only for edits
    - Search: ?search=<query> matches title or content
    - Pagination: global PageNumberPagination
    """
    queryset = Post.objects.select_related("author").all()
    serializer_class = PostSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly]
    filter_backends = [filters.SearchFilter]
    search_fields = ["title", "content"]

    def perform_create(self, serializer):
        if not self.request.user.is_authenticated:
            raise PermissionDenied("Authentication required.")
        serializer.save(author=self.request.user)


class CommentViewSet(viewsets.ModelViewSet):
    """
    CRUD for comments.
    - List & retrieve: public (read-only)
    - Create/Update/Delete: authenticated + owner-only for edits
    - Filter by post via query param: ?post=<post_id> (basic filter)
    """
    queryset = Comment.objects.select_related("author", "post").all()
    serializer_class = CommentSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly]

    def get_queryset(self):
        qs = super().get_queryset()
        post_id = self.request.query_params.get("post")
        if post_id:
            qs = qs.filter(post_id=post_id)
        return qs

    def perform_create(self, serializer):
        if not self.request.user.is_authenticated:
            raise PermissionDenied("Authentication required.")
        serializer.save(author=self.request.user)