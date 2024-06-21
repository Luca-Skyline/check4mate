from django.db import models

# Create your models here.

class CapturedImage(models.Model):
    image = models.ImageField(upload_to='captured_images/')