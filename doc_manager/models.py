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
    

class Request(models.Model):
    shipper = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name="requests") # this is Actor
    document = models.ForeignKey(Document, on_delete=models.CASCADE)
    status = models.CharField(
        max_length=20,
        choices=[("Pending", "Pending"), ("Approved", "Approved"), ("Rejected", "Rejected")],
        default="Pending"
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)