from django.contrib import admin
from .models import User


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ("name", "display_name", "creation_time")
    search_fields = ("name", "display_name")
    list_filter = ("creation_time",)
