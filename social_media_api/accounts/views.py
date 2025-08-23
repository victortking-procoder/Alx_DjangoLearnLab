from django.contrib.auth import get_user_model
from rest_framework import generics, permissions, status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.authtoken.models import Token
from django.shortcuts import get_object_or_404

from .serializers import RegisterSerializer, LoginSerializer, UserSerializer
from .serializers import FollowResponseSerializer

User = get_user_model()

class FollowUserView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, user_id):
        """
        Follow user with id=user_id.
        The authenticated user will add target to their `following`.
        """
        target = get_object_or_404(User, pk=user_id)
        if request.user.id == target.id:
            return Response({"detail": "You cannot follow yourself."}, status=status.HTTP_400_BAD_REQUEST)

        request.user.following.add(target)
        # Build response
        data = {
            "user_id": target.id,
            "username": target.username,
            "followers_count": target.followers.count(),
            "following_count": target.following.count(),
            "following": True,
        }
        serializer = FollowResponseSerializer(data)
        return Response(serializer.data, status=status.HTTP_200_OK)


class UnfollowUserView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, user_id):
        """
        Unfollow user with id=user_id.
        """
        target = get_object_or_404(User, pk=user_id)
        if request.user.id == target.id:
            return Response({"detail": "You cannot unfollow yourself."}, status=status.HTTP_400_BAD_REQUEST)

        request.user.following.remove(target)
        data = {
            "user_id": target.id,
            "username": target.username,
            "followers_count": target.followers.count(),
            "following_count": target.following.count(),
            "following": False,
        }
        serializer = FollowResponseSerializer(data)
        return Response(serializer.data, status=status.HTTP_200_OK)

class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = RegisterSerializer
    permission_classes = [permissions.AllowAny]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        token = Token.objects.get(user=user)
        data = {
            "user": UserSerializer(user, context={"request": request}).data,
            "token": token.key,
        }
        return Response(data, status=status.HTTP_201_CREATED)


class LoginView(APIView):
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data["user"]
        token, _ = Token.objects.get_or_create(user=user)
        return Response({
            "token": token.key,
            "user": UserSerializer(user, context={"request": request}).data
        })


class ProfileView(generics.RetrieveUpdateAPIView):
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        return self.request.user