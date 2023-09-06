from django.contrib import admin
from instruction.models import APIPath, Key


@admin.register(APIPath)
class APIPathAdmin(admin.ModelAdmin):
    list_display = ["path"]


@admin.register(Key)
class KeyAdmin(admin.ModelAdmin):
    list_display = ["api_path", "key", "request_type", "active"]
    list_filter = ["api_path", "request_type", "active"]