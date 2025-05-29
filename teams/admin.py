from django.contrib import admin
from .models import Team, TeamMember


@admin.register(Team)
class TeamAdmin(admin.ModelAdmin):
    list_display = ("name", "description", "admin", "creation_time")
    search_fields = ("name", "description")
    list_filter = ("creation_time",)


@admin.register(TeamMember)
class TeamMemberAdmin(admin.ModelAdmin):
    list_display = ("team", "user", "joined_at")
    list_filter = ("joined_at",)
    search_fields = ("team__name", "user__name")
