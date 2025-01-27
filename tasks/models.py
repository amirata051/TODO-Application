from django.db import models
from django.utils.timezone import now
from datetime import timedelta

class Task(models.Model):
    title = models.CharField(
        max_length=255,
        help_text="The title of the task. Must be under 255 characters."
    )  
    description = models.TextField(
        help_text="A detailed description of the task."
    )  
    due_date = models.DateTimeField(
        help_text="The due date and time for the task."
    )  
    completed = models.BooleanField(
        default=False,
        help_text="Indicates if the task is completed or not."
    )  
    created_at = models.DateTimeField(
        auto_now_add=True,
        help_text="The date and time when the task was created."
    )  
    updated_at = models.DateTimeField(
        auto_now=True,
        help_text="The date and time when the task was last updated."
    )  

    def is_due_soon(self):
        """Check if the task is due within the next 24 hours."""
        return not self.completed and self.due_date <= now() + timedelta(days=1)

    class Meta:
        ordering = ['due_date']  # Default ordering by due date
        verbose_name = "Task"
        verbose_name_plural = "Tasks"

    def __str__(self):
        return self.title  
