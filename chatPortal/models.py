from django.db import models
from django.contrib.auth.models import AbstractUser, Group, Permission




class Messages(models.Model):
    username = models.CharField(max_length=255)
    message = models.TextField()
    roomId = models.CharField(max_length=255)
    timestamp = models.DateTimeField(auto_now_add=True) 



    def __str__(self):
        return f"{self.username}:  {self.message}"
