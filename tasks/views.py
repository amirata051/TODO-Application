from rest_framework.response import Response
from rest_framework import status, viewsets, filters
from django_filters.rest_framework import DjangoFilterBackend
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from django.http import HttpResponse
from .models import Task
from .serializers import TaskSerializer


def home_view(request):
    """
    View for the home page.
    Displays a simple welcome message.
    """
    return HttpResponse(
        "Welcome to the TODO Application API! Use /swagger/ for API docs."
    )


class TaskViewSet(viewsets.ModelViewSet):
    """
    A ViewSet for managing Task objects.
    Provides CRUD operations with filtering, searching, and ordering capabilities.
    """

    queryset = Task.objects.all()
    serializer_class = TaskSerializer

    # Enable filtering, searching, and ordering
    filter_backends = [
        DjangoFilterBackend,
        filters.SearchFilter,
        filters.OrderingFilter,
    ]
    filterset_fields = ["completed", "due_date", "created_at"]
    search_fields = ["title", "description"]
    ordering_fields = ["due_date", "created_at"]

    @swagger_auto_schema(
        operation_summary="List all tasks",
        operation_description="Retrieve a list of all tasks with optional filters, search, and ordering.",
        responses={200: TaskSerializer(many=True)},  # Expected response
    )
    def list(self, request, *args, **kwargs):
        """
        GET /tasks/ - Retrieve all tasks.
        Supports filtering, searching, and ordering.
        """
        return super().list(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_summary="Create a new task",
        operation_description="Add a new task by providing its details.",
        request_body=TaskSerializer,  # Specify the request body
        responses={201: TaskSerializer},  # Expected response
    )
    def create(self, request, *args, **kwargs):
        """
        POST /tasks/ - Create a new task.
        """
        serializer = self.get_serializer(data=request.data)
        if not serializer.is_valid():
            # Return a 400 response with validation errors
            return Response(
                {"errors": serializer.errors}, status=status.HTTP_400_BAD_REQUEST
            )
        self.perform_create(serializer)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    @swagger_auto_schema(
        operation_summary="Retrieve a specific task",
        operation_description="Retrieve details of a task by its ID.",
        responses={200: TaskSerializer},  # Expected response
    )
    def retrieve(self, request, *args, **kwargs):
        """
        GET /tasks/{id}/ - Retrieve details of a specific task.
        """
        return super().retrieve(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_summary="Update a task",
        operation_description="Update the details of a task by its ID.",
        request_body=TaskSerializer,  # Specify the request body
        responses={200: TaskSerializer},  # Expected response
    )
    def update(self, request, *args, **kwargs):
        """
        PUT /tasks/{id}/ - Update a task.
        """
        return super().update(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_summary="Partially update a task",
        operation_description="Partially update the details of a task by its ID.",
        request_body=TaskSerializer,  # Specify the request body
        responses={200: TaskSerializer},  # Expected response
    )
    def partial_update(self, request, *args, **kwargs):
        """
        PATCH /tasks/{id}/ - Partially update a task.
        """
        return super().partial_update(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_summary="Delete a task",
        operation_description="Delete a specific task by its ID.",
        responses={204: "Task successfully deleted"},  # Expected response
    )
    def destroy(self, request, *args, **kwargs):
        """
        DELETE /tasks/{id}/ - Delete a task.
        """
        return super().destroy(request, *args, **kwargs)
