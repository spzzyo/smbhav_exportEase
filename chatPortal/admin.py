from django.contrib import admin
from django.contrib.auth.admin import UserAdmin


# Register your models here.
from .models import Messages

@admin.register(Messages)
class ChatMessageAdmin(admin.ModelAdmin):
    list_display = ('username', 'message','roomId')

