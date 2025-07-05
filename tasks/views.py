from rest_framework import viewsets, generics
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth.models import User
from .models import Task
from .serializers import TaskSerializer, RegisterSerializer
from .csrf_exempt_mixin import CsrfExemptMixin
from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer


# 👤 Register API (no auth required)
class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = RegisterSerializer
    permission_classes = []


# ✅ Auth-protected Task ViewSet
class TaskViewSet(CsrfExemptMixin, viewsets.ModelViewSet):
    queryset = Task.objects.all().order_by('-created_at')
    serializer_class = TaskSerializer
    permission_classes = [IsAuthenticated]  # 🔐 Only logged-in users

    def get_queryset(self):
        # 🔄 Return only tasks created by the logged-in user
        return Task.objects.filter(user=self.request.user).order_by('-created_at')

    def perform_create(self, serializer):
        instance = serializer.save(user=self.request.user)
        self.broadcast_change("created", instance)

    def perform_update(self, serializer):
        instance = serializer.save()
        self.broadcast_change("updated", instance)

    def perform_destroy(self, instance):
        instance_id = instance.id
        instance.delete()
        self.broadcast_change("deleted", {"id": instance_id})

    def broadcast_change(self, action, task):
        # 🔔 Broadcast to WebSocket group
        channel_layer = get_channel_layer()
        async_to_sync(channel_layer.group_send)(
            "tasks",  # Group name
            {
                "type": "task_update",
                "message": {
                    "action": action,
                    "task": TaskSerializer(task).data if isinstance(task, Task) else task
                },
            }
        )
