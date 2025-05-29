from django.shortcuts import render
from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.decorators import action
from django.utils import timezone
from .models import Board, Task
from .serializers import (
    BoardSerializer,
    BoardCreateSerializer,
    TaskSerializer,
    TaskCreateSerializer,
    TaskStatusUpdateSerializer,
)

# Create your views here.


class BoardViewSet(viewsets.ModelViewSet):
    queryset = Board.objects.all()
    serializer_class = BoardSerializer

    def get_serializer_class(self):
        if self.action == "create":
            return BoardCreateSerializer
        return BoardSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        return Response(
            {"id": str(serializer.instance.id)}, status=status.HTTP_201_CREATED
        )

    @action(detail=True, methods=["post"])
    def close(self, request, pk=None):
        board = self.get_object()

        # Check if all tasks are complete
        incomplete_tasks = Task.objects.filter(board=board).exclude(status="COMPLETE")
        if incomplete_tasks.exists():
            return Response(
                {"error": "Cannot close board with incomplete tasks"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        board.status = "CLOSED"
        board.end_time = timezone.now()
        board.save()

        return Response(status=status.HTTP_204_NO_CONTENT)

    @action(detail=False, methods=["get"])
    def team_boards(self, request):
        team_id = request.query_params.get("team_id")
        if not team_id:
            return Response(
                {"error": "team_id parameter is required"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        boards = Board.objects.filter(team_id=team_id, status="OPEN")
        serializer = BoardSerializer(boards, many=True)
        return Response(serializer.data)

    @action(detail=True, methods=["get"])
    def export(self, request, pk=None):
        board = self.get_object()
        tasks = Task.objects.filter(board=board)

        # Create a text file with board details
        filename = f"board_{board.id}.txt"
        filepath = f"out/{filename}"

        with open(filepath, "w") as f:
            f.write(f"Board: {board.name}\n")
            f.write(f"Description: {board.description}\n")
            f.write(f"Status: {board.status}\n")
            f.write(f"Created: {board.creation_time}\n")
            f.write("\nTasks:\n")
            f.write("-" * 50 + "\n")

            for task in tasks:
                f.write(f"Title: {task.title}\n")
                f.write(f"Description: {task.description}\n")
                f.write(f"Status: {task.status}\n")
                f.write(
                    f"Assigned to: {task.assigned_to.name if task.assigned_to else 'Unassigned'}\n"
                )
                f.write("-" * 50 + "\n")

        return Response({"out_file": filename})


class TaskViewSet(viewsets.ModelViewSet):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer

    def get_serializer_class(self):
        if self.action == "create":
            return TaskCreateSerializer
        elif self.action == "update_status":
            return TaskStatusUpdateSerializer
        return TaskSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        # Check if board is open
        board = serializer.validated_data["board"]
        if board.status != "OPEN":
            return Response(
                {"error": "Cannot add tasks to a closed board"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        self.perform_create(serializer)
        return Response(
            {"id": str(serializer.instance.id)}, status=status.HTTP_201_CREATED
        )

    @action(detail=True, methods=["patch"])
    def update_status(self, request, pk=None):
        task = self.get_object()
        serializer = self.get_serializer(task, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)
