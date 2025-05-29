from django.shortcuts import render
from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.decorators import action
from .models import User
from .serializers import UserSerializer, UserCreateSerializer, UserUpdateSerializer
from teams.models import Team
from teams.serializers import TeamSerializer

# Create your views here.


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer

    def get_serializer_class(self):
        if self.action == "create":
            return UserCreateSerializer
        elif self.action in ["update", "partial_update"]:
            return UserUpdateSerializer
        return UserSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        return Response(
            {"id": str(serializer.instance.id)}, status=status.HTTP_201_CREATED
        )

    @action(detail=True, methods=["get"])
    def teams(self, request, pk=None):
        user = self.get_object()
        teams = Team.objects.filter(members=user)
        serializer = TeamSerializer(teams, many=True)
        return Response(serializer.data)
