from django.shortcuts import render
from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.decorators import action
from .models import Team, TeamMember
from .serializers import (
    TeamSerializer,
    TeamCreateSerializer,
    TeamUpdateSerializer,
    TeamMemberSerializer,
    TeamMemberAddSerializer,
)
from users.models import User

# Create your views here.


class TeamViewSet(viewsets.ModelViewSet):
    queryset = Team.objects.all()
    serializer_class = TeamSerializer

    def get_serializer_class(self):
        if self.action == "create":
            return TeamCreateSerializer
        elif self.action in ["update", "partial_update"]:
            return TeamUpdateSerializer
        return TeamSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        return Response(
            {"id": str(serializer.instance.id)}, status=status.HTTP_201_CREATED
        )

    @action(detail=True, methods=["post"])
    def add_users(self, request, pk=None):
        team = self.get_object()
        serializer = TeamMemberAddSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        users = User.objects.filter(id__in=serializer.validated_data["users"])
        if len(users) > 50:
            return Response(
                {"error": "Cannot add more than 50 users to a team"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        for user in users:
            TeamMember.objects.get_or_create(team=team, user=user)

        return Response(status=status.HTTP_204_NO_CONTENT)

    @action(detail=True, methods=["post"])
    def remove_users(self, request, pk=None):
        team = self.get_object()
        serializer = TeamMemberAddSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        TeamMember.objects.filter(
            team=team, user_id__in=serializer.validated_data["users"]
        ).delete()

        return Response(status=status.HTTP_204_NO_CONTENT)

    @action(detail=True, methods=["get"])
    def users(self, request, pk=None):
        team = self.get_object()
        members = TeamMember.objects.filter(team=team)
        serializer = TeamMemberSerializer(members, many=True)
        return Response(serializer.data)
