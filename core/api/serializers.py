from datetime import date
from rest_framework import serializers
from core.models import Task, User

class TaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = '__all__'

    def validate_due_date(self, value):
        if value <= date.today():
            raise serializers.ValidationError("Due date must be in the future.")
        return value

class TaskUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        excepts = ['id']
        fields = '__all__' 

    def validate(self, data):
        if data.get('status') == 'COMPLETED':
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

    def create(self, validated_data):
        password = validated_data.pop('password', None)
        user = super().create(validated_data)
        if password:
            user.set_password(password)  # ✅ hashes it
            user.save()
        return user

    def update(self, instance, validated_data):
        password = validated_data.pop('password', None)

        # Update other fields
        for attr, value in validated_data.items():
            setattr(instance, attr, value)

        # Handle password hashing if password is provided
        if password:
            instance.set_password(password)

        instance.save()
        return instance
