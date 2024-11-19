from django.db import models

# Create your models here.
class Messages(models.Model):
    username = models.CharField(max_length=255)
    message = models.TextField()


    def __str__(self):
        return f"{self.username}:  {self.message}"