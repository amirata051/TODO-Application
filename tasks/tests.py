from django.test import TestCase
from rest_framework.test import APIClient
from rest_framework import status
from .models import Task
from .serializers import TaskSerializer
from datetime import datetime, timedelta
from django.utils.timezone import make_aware

class TaskModelTest(TestCase):
    def setUp(self):
        self.task = Task.objects.create(
            title="Test Task",
            description="This is a test task",
            due_date=make_aware(datetime.now() + timedelta(days=1)),
            completed=False
        )

    def test_task_creation(self):
        """Test task creation and field values"""
        self.assertEqual(self.task.title, "Test Task")
        self.assertFalse(self.task.completed)

    def test_due_date_past(self):
        """Test creation of a task with a past due date"""
        data = {
            "title": "Invalid Task",
            "description": "Due date is in the past",
            "due_date": make_aware(datetime.now() - timedelta(days=1)).isoformat(),
            "completed": False
        }
        serializer = TaskSerializer(data=data)
        self.assertFalse(serializer.is_valid())
        self.assertIn("due_date", serializer.errors)

    def test_long_title(self):
        """Test a task with a title that exceeds the max length"""
        data = {
            "title": "x" * 256,  # Assuming max length is 255
            "description": "Valid description",
            "due_date": make_aware(datetime.now() + timedelta(days=1)).isoformat(),
            "completed": False
        }
        serializer = TaskSerializer(data=data)
        self.assertFalse(serializer.is_valid())
        self.assertIn("title", serializer.errors)


class TaskSerializerTest(TestCase):
    def test_valid_data(self):
        """Test serializer with valid data"""
        data = {
            "title": "Valid Task",
            "description": "This is valid",
            "due_date": make_aware(datetime.now() + timedelta(days=1)).isoformat(),
            "completed": False
        }
        serializer = TaskSerializer(data=data)
        self.assertTrue(serializer.is_valid())

    def test_invalid_data(self):
        """Test serializer with invalid data"""
        data = {"title": "", "description": ""}
        serializer = TaskSerializer(data=data)
        self.assertFalse(serializer.is_valid())
        self.assertIn("title", serializer.errors)

    def test_missing_fields(self):
        """Test serializer with missing fields"""
        data = {"title": "Task without due date"}
        serializer = TaskSerializer(data=data)
        self.assertFalse(serializer.is_valid())
        self.assertIn("due_date", serializer.errors)


class TaskAPITest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.task1 = Task.objects.create(
            title="API Task 1",
            description="First test task for API",
            due_date=make_aware(datetime.now() + timedelta(days=1)),
            completed=False
        )
        self.task2 = Task.objects.create(
            title="API Task 2",
            description="Second test task for API",
            due_date=make_aware(datetime.now() + timedelta(days=2)),
            completed=True
        )

    def test_get_tasks(self):
        """Test retrieving the list of tasks"""
        response = self.client.get("/api/tasks/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)

    def test_create_task(self):
        """Test creating a new task via API"""
        data = {
            "title": "New API Task",
            "description": "Testing task creation via API",
            "due_date": make_aware(datetime.now() + timedelta(days=2)).isoformat(),
            "completed": False
        }
        response = self.client.post("/api/tasks/", data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Task.objects.count(), 3)

    def test_create_task_invalid(self):
        """Test creating a task with invalid data"""
        data = {"title": ""}
        response = self.client.post("/api/tasks/", data, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_update_task(self):
        """Test updating a task via API"""
        data = {"title": "Updated Title"}
        response = self.client.patch(f"/api/tasks/{self.task1.id}/", data, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["title"], "Updated Title")

    def test_delete_task(self):
        """Test deleting a task via API"""
        response = self.client.delete(f"/api/tasks/{self.task1.id}/")
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Task.objects.count(), 1)

    def test_filter_tasks(self):
        """Test filtering tasks based on completed status"""
        response = self.client.get("/api/tasks/?completed=True")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

    def test_search_tasks(self):
        """Test searching tasks based on title"""
        response = self.client.get("/api/tasks/?search=API Task 1")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

    def test_order_tasks(self):
        """Test ordering tasks by due date"""
        response = self.client.get("/api/tasks/?ordering=due_date")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        tasks = response.data
        self.assertLessEqual(tasks[0]["due_date"], tasks[1]["due_date"])
