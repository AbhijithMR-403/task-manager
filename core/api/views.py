from rest_framework import generics, status
from rest_framework.exceptions import PermissionDenied
from rest_framework.response import Response
from core.models import Task, User
from .serializers import TaskSerializer, TaskUpdateSerializer, UserSerializer

class TaskListCreateAPI(generics.ListCreateAPIView):
    serializer_class = TaskSerializer
    queryset = Task.objects.all()


class TaskUpdateAPI(generics.UpdateAPIView):
    serializer_class = TaskUpdateSerializer
    queryset = Task.objects.all()

    def get_object(self):
        task = super().get_object()
        user = task.assigned_to

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
