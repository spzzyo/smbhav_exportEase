from django.db import models

# Create your models here.
class Item(models.Model):
    item_name = models.CharField(max_length=255, blank=True)
    item_image = models.ImageField(upload_to='items/')
    def __str__(self):
        return self.item_name