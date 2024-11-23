from user.models import CustomUser

from django.db import models

class Document(models.Model):
    from django.db import models

class Document(models.Model):
    exporter = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    s3_encrypted_key = models.CharField(max_length=255, default="")  # Default empty string
    s3_metadata_key = models.CharField(max_length=255, default="")  # Default empty string
    original_file = models.FileField(upload_to='documents/', null=True, blank=True)  # Allow null and blank
    timestamp = models.DateTimeField(auto_now_add=True)  # Automatically set to the current timestamp

    def __str__(self):
        return self.category


    def __str__(self):
        return self.title
