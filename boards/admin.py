from django.contrib import admin
from .models import Board, Task


@admin.register(Board)
class BoardAdmin(admin.ModelAdmin):
    list_display = ("name", "description", "team", "status", "creation_time")
    search_fields = ("name", "description")
    list_filter = ("status", "creation_time")


@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    list_display = (
        "title",
        "description",
        "board",
        "assigned_to",
        "status",
        "creation_time",
    )
    search_fields = ("title", "description")
    list_filter = ("status", "creation_time")
