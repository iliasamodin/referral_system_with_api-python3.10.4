from django.contrib import admin
from instruction.models import APIPath


@admin.register(APIPath)
class APIPathAdmin(admin.ModelAdmin):
    list_display = ["path"]