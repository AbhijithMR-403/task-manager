from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from .views import TaskListAPI, TaskUpdateAPI

urlpatterns = [
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    
    path('tasks/', TaskListAPI.as_view(), name='api_tasks'),
    path('tasks/<int:pk>/', TaskUpdateAPI.as_view(), name='api_task_update'),
]
