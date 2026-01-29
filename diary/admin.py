
from django.contrib import admin
from .models import DiaryEntry  # This imports the model you just fixed

# This allows you to see and edit your diary entries at /admin
admin.site.register(DiaryEntry)
# Register your models here.
