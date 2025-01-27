from rest_framework import serializers
from .models import Task
from django.utils.timezone import now, make_aware

class TaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = '__all__'

    
    def validate_title(self, value):
        if len(value) < 3:
            raise serializers.ValidationError("Title must be at least 3 characters long.")
        return value

    def validate_due_date(self, value):
        if value.tzinfo is None:  # If naive, make it timezone-aware
            value = make_aware(value)
        if value < now():  # Compare with timezone-aware datetime
            raise serializers.ValidationError("Due date cannot be in the past.")
        return value

    # Custom validation for the entire object
    def validate(self, data):
        completed = data.get('completed', False)  # Safely retrieve 'completed'
        due_date = data.get('due_date')  # Safely retrieve 'due_date'
        
        if completed and due_date and due_date > now():
            raise serializers.ValidationError("A task cannot be marked as completed if the due date is in the future.")
        return data
