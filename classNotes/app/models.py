from django.db import models

# Create your models here.
class AudioFile(models.Model):
    file = models.FileField(null=True, upload_to="input")
