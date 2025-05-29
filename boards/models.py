from django.db import models
import uuid
from datetime import datetime
from teams.models import Team
from users.models import User


class Board(models.Model):
    STATUS_CHOICES = [
        ("OPEN", "Open"),
        ("CLOSED", "Closed"),
    ]

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=64)
    description = models.CharField(max_length=128)
    team = models.ForeignKey(Team, on_delete=models.CASCADE, related_name="boards")
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default="OPEN")
    creation_time = models.DateTimeField(default=datetime.utcnow)
    end_time = models.DateTimeField(null=True, blank=True)

    def to_dict(self):
        return {
            "id": str(self.id),
            "name": self.name,
            "description": self.description,
            "team_id": str(self.team.id),
            "status": self.status,
            "creation_time": self.creation_time.isoformat(),
            "end_time": self.end_time.isoformat() if self.end_time else None,
        }

    class Meta:
        db_table = "boards"
        unique_together = ("name", "team")


class Task(models.Model):
    STATUS_CHOICES = [
        ("OPEN", "Open"),
        ("IN_PROGRESS", "In Progress"),
        ("COMPLETE", "Complete"),
    ]

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    title = models.CharField(max_length=64)
    description = models.CharField(max_length=128)
    board = models.ForeignKey(Board, on_delete=models.CASCADE, related_name="tasks")
    assigned_to = models.ForeignKey(
        User, on_delete=models.SET_NULL, null=True, related_name="assigned_tasks"
    )
    status = models.CharField(max_length=15, choices=STATUS_CHOICES, default="OPEN")
    creation_time = models.DateTimeField(default=datetime.utcnow)

    def to_dict(self):
        return {
            "id": str(self.id),
            "title": self.title,
            "description": self.description,
            "board_id": str(self.board.id),
            "user_id": str(self.assigned_to.id) if self.assigned_to else None,
            "status": self.status,
            "creation_time": self.creation_time.isoformat(),
        }

    class Meta:
        db_table = "tasks"
        unique_together = ("title", "board")
