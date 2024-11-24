from django.db import models
from django.utils import timezone  # Import timezone for current timestamp
from user.models import CustomUser

class Document(models.Model):
    exporter = models.ForeignKey(CustomUser, on_delete=models.CASCADE, default=2)
    title = models.CharField(max_length=255)
    s3_encrypted_key = models.CharField(max_length=255, default="")  # Default empty string
    s3_metadata_key = models.CharField(max_length=255, default="")  # Default empty string
    original_file = models.FileField(upload_to='documents/', null=True, blank=True)  # Allow null and blank
    timestamp = models.DateTimeField(default=timezone.now)  # Default to current timestamp using timezone.now()

    def __str__(self):
        return self.title  # Return the document title

class Request(models.Model):
    shipper = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name="requests")  # This is Actor
    document = models.ForeignKey(Document, on_delete=models.CASCADE)
    status = models.CharField(
        max_length=20,
        choices=[("Pending", "Pending"), ("Approved", "Approved"), ("Rejected", "Rejected")],
        default="Pending"  # Default to "Pending"
    )
    created_at = models.DateTimeField(auto_now_add=True, null=False)  # Automatically set the time when created
    updated_at = models.DateTimeField(auto_now=True)  # Automatically update when modified
    
    def __str__(self):
        return f"Request for {self.document.title} by {self.shipper.username} - {self.status}"
