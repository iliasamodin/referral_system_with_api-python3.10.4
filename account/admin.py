from django.contrib import admin
from account.models import User


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = [
        "phone_number", 
        "invite_code", 
        "is_superuser",
        "is_staff",
        "is_active"
    ]