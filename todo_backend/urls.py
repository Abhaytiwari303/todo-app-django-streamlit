from django.http import JsonResponse
from django.contrib import admin
from django.urls import path, include
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

def home(request):
    return JsonResponse({
        "message": "Welcome to the Todo API",
        "available_routes": [
            "/admin/",
            "api/token/",
            "/api/tasks/",

        ]
    })

urlpatterns = [
    path('', home),  # 👈 New home route
    path('admin/', admin.site.urls),
    path('api/', include('tasks.urls')),
     # ✅ JWT Token URLs
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]
