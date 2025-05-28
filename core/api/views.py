from rest_framework import generics, permissions, status
from rest_framework.exceptions import PermissionDenied
from rest_framework.response import Response
from core.models import Task, User
from core.permissions import IsSuperAdmin
from .serializers import TaskSerializer, TaskUpdateSerializer, UserSerializer
from django.contrib.auth.hashers import make_password

class TaskListAPI(generics.ListAPIView):
    serializer_class = TaskSerializer
    # permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        if user.role == 'SUPERADMIN':
            return Task.objects.all()
        elif user.role == 'ADMIN':
            return Task.objects.filter(assigned_to__assigned_admin=user)
        else:
            return Task.objects.filter(assigned_to=user)

class TaskUpdateAPI(generics.UpdateAPIView):
    serializer_class = TaskUpdateSerializer
    # permission_classes = [permissions.IsAuthenticated]
    queryset = Task.objects.all()

    def get_object(self):
        task = super().get_object()
        user = self.request.user

        # Check if the user is the assigned user
        if task.assigned_to == user:
            return task

        # Check if user is SuperAdmin
        if user.role == 'SUPERADMIN':
            return task

        # Check if user is Admin AND the task is assigned to a user under them
        if user.role == 'ADMIN' and task.assigned_to.assigned_admin == user:
            return task

        raise PermissionDenied("You do not have permission to update this task.")

    def update(self, request, *args, **kwargs):
        data = request.data
        if data.get('status') == 'COMPLETED':
            if not data.get('completion_report') or not data.get('worked_hours'):
                return Response({
                    "error": "completion_report and worked_hours are required when completing a task."
                }, status=status.HTTP_400_BAD_REQUEST)
        
        response = super().update(request, *args, **kwargs)
        if response.status_code == status.HTTP_200_OK:
            return Response({
                'status': 'success',
                'message': 'Task updated successfully',
                'data': response.data
            })
        return response

class TaskReportAPI(generics.RetrieveAPIView):
    serializer_class = TaskSerializer
    # permission_classes = [permissions.IsAuthenticated]
    queryset = Task.objects.all()

    def get_object(self):
        task = super().get_object()
        user = self.request.user
        
        # Only allow access for completed tasks
        if task.status != 'COMPLETED':
            raise PermissionDenied("This task is not completed.")
        
        # Check permissions
        if (user.role == 'SUPERADMIN' or 
            (user.role == 'ADMIN' and task.assigned_to.assigned_admin == user) or 
            task.assigned_to == user):
            return task
            
        raise PermissionDenied("You don't have permission to view this report.")
    

class UserCreateUpdateAPI(generics.CreateAPIView, generics.UpdateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsSuperAdmin]  # Only SuperAdmin can access

    def perform_create(self, serializer):
        password = serializer.validated_data.pop('password', None)
        if password:
            serializer.validated_data['password'] = make_password(password)
        serializer.save()

    def perform_update(self, serializer):
        password = serializer.validated_data.pop('password', None)
        if password:
            serializer.validated_data['password'] = make_password(password)
        serializer.save()
