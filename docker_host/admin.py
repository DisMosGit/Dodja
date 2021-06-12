from django.contrib import admin
from .models import Host, Access, Job


@admin.register(Host, Access, Job)
class HostAdmin(admin.ModelAdmin):
    pass