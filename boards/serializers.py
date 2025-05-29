from rest_framework import serializers
from .models import Board, Task
from users.serializers import UserSerializer


class BoardSerializer(serializers.ModelSerializer):
    class Meta:
        model = Board
        fields = [
            "id",
            "name",
            "description",
            "team",
            "status",
            "creation_time",
            "end_time",
        ]
        read_only_fields = ["id", "creation_time", "end_time"]


class BoardCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Board
        fields = ["name", "description", "team"]


class TaskSerializer(serializers.ModelSerializer):
    assigned_to = UserSerializer(read_only=True)

    class Meta:
        model = Task
        fields = [
            "id",
            "title",
            "description",
            "board",
            "assigned_to",
            "status",
            "creation_time",
        ]
        read_only_fields = ["id", "creation_time"]


class TaskCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = ["title", "description", "board", "assigned_to"]


class TaskStatusUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = ["status"]
