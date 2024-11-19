from django.contrib import admin

# Register your models here.
from .models import Messages

@admin.register(Messages)
class ChatMessageAdmin(admin.ModelAdmin):
    list_display = ('username', 'message')