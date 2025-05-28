from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, permissions
from core.models import Task
from .serializers import TaskSerializer, TaskUpdateSerializer

class TaskListAPI(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        tasks = Task.objects.filter(assigned_to=request.user)
        serializer = TaskSerializer(tasks, many=True)
        return Response(serializer.data)

class TaskUpdateAPI(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def put(self, request, pk):
        try:
            task = Task.objects.get(pk=pk, assigned_to=request.user)
        except Task.DoesNotExist:
            return Response({"detail": "Task not found or not authorized."}, status=status.HTTP_404_NOT_FOUND)

        serializer = TaskUpdateSerializer(task, data=request.data, partial=True)
        if serializer.is_valid():
            if serializer.validated_data.get("status") == "COMPLETED":
                # Ensure completion_report and worked_hours are present
                if not serializer.validated_data.get("completion_report") or not serializer.validated_data.get("worked_hours"):
                    return Response(
                        {"detail": "Completion report and worked hours are required when completing a task."},
                        status=status.HTTP_400_BAD_REQUEST
                    )
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
