from django.contrib import admin
from .models import Hint


@admin.register(Hint)
class HintAdmin(admin.ModelAdmin):
    pass