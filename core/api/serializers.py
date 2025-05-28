from rest_framework import serializers
from core.models import Task, User

class TaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = '__all__'


class TaskUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = ['status', 'completion_report', 'worked_hours']

    def validate(self, data):
        if data.get('status') == 'Completed':
            if not data.get('completion_report'):
                raise serializers.ValidationError("Completion report is required.")
            if not data.get('worked_hours'):
                raise serializers.ValidationError("Worked hours are required.")
        return data


class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=False)
    
    class Meta:
        model = User
        fields = [
            'id', 'username', 'email', 'role', 
            'assigned_admin', 'password', 'first_name', 
            'last_name'
        ]
        extra_kwargs = {
            'assigned_admin': {'required': False},
            'password': {'write_only': True}
        }

    def validate(self, data):
        # Ensure only SuperAdmin can create admins/superadmins
        request = self.context.get('request')
        if request and request.user.role != 'SUPERADMIN':
            if 'role' in data and data['role'] in ['ADMIN', 'SUPERADMIN']:
                raise serializers.ValidationError(
                    "Only SuperAdmin can create admins."
                )
        return data
