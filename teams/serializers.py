from rest_framework import serializers
from .models import Team, TeamMember
from users.serializers import UserSerializer


class TeamSerializer(serializers.ModelSerializer):
    class Meta:
        model = Team
        fields = ["id", "name", "description", "admin", "creation_time"]
        read_only_fields = ["id", "creation_time"]


class TeamCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Team
        fields = ["name", "description", "admin"]


class TeamUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Team
        fields = ["description", "admin"]


class TeamMemberSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)

    class Meta:
        model = TeamMember
        fields = ["user", "joined_at"]
        read_only_fields = ["joined_at"]


class TeamMemberAddSerializer(serializers.Serializer):
    users = serializers.ListField(
        child=serializers.UUIDField(), min_length=1, max_length=50
    )
