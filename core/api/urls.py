from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from .views import TaskListCreateAPI, TaskUpdateAPI, TaskReportAPI, UserCreateUpdateAPI

urlpatterns = [
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    
    path('tasks/', TaskListCreateAPI.as_view(), name='task-list'),
    path('tasks/<int:pk>/', TaskUpdateAPI.as_view(), name='task-update'),
    path('tasks/<int:pk>/report/', TaskReportAPI.as_view(), name='task-report'),
    path('tasks/create', TaskListCreateAPI.as_view(), name='task-create'),


    path('users/', UserCreateUpdateAPI.as_view(), name='user-create'),
    path('users/<int:pk>/', UserCreateUpdateAPI.as_view(), name='user-update'),
]
