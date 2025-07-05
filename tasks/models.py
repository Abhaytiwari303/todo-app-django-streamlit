from django.db import models
from django.contrib.auth.models import User

PRIORITY_CHOICES = [
    ('Low', 'Low'),
    ('Medium', 'Medium'),
    ('High', 'High'),
]

CATEGORY_CHOICES = [
    ('Personal', 'Personal'),
    ('Work', 'Work'),
    ('Study', 'Study'),
    ('Others', 'Others'),
]

class Task(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    priority = models.CharField(max_length=10, choices=PRIORITY_CHOICES)
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES)
    due_date = models.DateField()
    completed = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='tasks', null=True, blank=True)
    def __str__(self):
        return self.title
    def get_absolute_url(self):
        # Example: Redirect to Streamlit page with task ID as query param
        return f"http://localhost:8501/?task_id={self.id}"
