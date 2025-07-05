from django.contrib import admin
from .models import Task

@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    list_display = ['title', 'priority', 'category', 'due_date', 'completed']
    list_filter = ['priority', 'category', 'completed']
    search_fields = ['title', 'description']
