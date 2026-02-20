from rest_framework import viewsets, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.contrib.auth.models import User
from django.contrib.auth.hashers import make_password

from .models import Task
from .serializers import TaskSerializer


# 🔹 Task ViewSet (User-specific tasks)
class TaskViewSet(viewsets.ModelViewSet):
    serializer_class = TaskSerializer
    permission_classes = [IsAuthenticated]
    queryset = Task.objects.all()

    # Show only logged-in user's tasks
    def get_queryset(self):
        return Task.objects.filter(
            user=self.request.user
        ).order_by('-created_at')

    # Automatically assign user when creating task
    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


# 🔹 Register API
@api_view(['POST'])
def register_user(request):
    username = request.data.get("username")
    email = request.data.get("email")
    password = request.data.get("password")

    if not username or not email or not password:
        return Response(
            {"error": "All fields are required"},
            status=status.HTTP_400_BAD_REQUEST
        )

    if User.objects.filter(username=username).exists():
        return Response(
            {"error": "Username already exists. Please login."},
            status=status.HTTP_400_BAD_REQUEST
        )

    if User.objects.filter(email=email).exists():
        return Response(
            {"error": "Email already registered."},
            status=status.HTTP_400_BAD_REQUEST
        )

    User.objects.create(
        username=username,
        email=email,
        password=make_password(password)
    )

    return Response(
        {"message": "User registered successfully"},
        status=status.HTTP_201_CREATED
    )
