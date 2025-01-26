from django.db import models
from django.utils.timezone import now
from datetime import timedelta

class Task(models.Model):
    title = models.CharField(
        max_length=255,
        help_text="The title of the task. Must be under 255 characters."
    )  # Field for task title
    description = models.TextField(
        help_text="A detailed description of the task."
    )  # Field for task description
    due_date = models.DateTimeField(
        help_text="The due date and time for the task."
    )  # Field for due date of the task
    completed = models.BooleanField(
        default=False,
        help_text="Indicates if the task is completed or not."
    )  # Field to mark if the task is completed
    created_at = models.DateTimeField(
        auto_now_add=True,
        help_text="The date and time when the task was created."
    )  # Automatically sets the creation date
    updated_at = models.DateTimeField(
        auto_now=True,
        help_text="The date and time when the task was last updated."
    )  # Automatically updates on modification

    def is_due_soon(self):
        """Check if the task is due within the next 24 hours."""
        return not self.completed and self.due_date <= now() + timedelta(days=1)

    class Meta:
        ordering = ['due_date']  # Default ordering by due date
        verbose_name = "Task"
        verbose_name_plural = "Tasks"

    def __str__(self):
        return self.title  # String representation of the task model
