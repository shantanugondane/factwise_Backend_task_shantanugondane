from django.db import models
import uuid
from datetime import datetime


class User(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=64, unique=True)
    display_name = models.CharField(max_length=64)
    description = models.TextField(blank=True)
    creation_time = models.DateTimeField(default=datetime.utcnow)

    def to_dict(self):
        return {
            "id": str(self.id),
            "name": self.name,
            "display_name": self.display_name,
            "description": self.description,
            "creation_time": self.creation_time.isoformat(),
        }

    class Meta:
        db_table = "users"
