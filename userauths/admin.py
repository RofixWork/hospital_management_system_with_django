from django.contrib import admin

from .models import User


# Register your models here.
@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ["id", "email", "username", "user_type"]
    search_fields = ["email", "username"]
    list_filter = ["user_type"]
    list_display_links = ["email"]
