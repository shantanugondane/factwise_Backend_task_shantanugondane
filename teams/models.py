from django.db import models
import uuid
from datetime import datetime
from users.models import User


class Team(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=64, unique=True)
    description = models.CharField(max_length=128)
    admin = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="administered_teams"
    )
    creation_time = models.DateTimeField(default=datetime.utcnow)
    members = models.ManyToManyField(User, through="TeamMember", related_name="teams")

    def to_dict(self):
        return {
            "id": str(self.id),
            "name": self.name,
            "description": self.description,
            "admin": str(self.admin.id),
            "creation_time": self.creation_time.isoformat(),
        }

    class Meta:
        db_table = "teams"


class TeamMember(models.Model):
    team = models.ForeignKey(Team, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    joined_at = models.DateTimeField(default=datetime.utcnow)

    class Meta:
        db_table = "team_members"
        unique_together = ("team", "user")
