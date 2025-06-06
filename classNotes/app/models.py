from django.db import models

class AudioFile(models.Model):
    LANGUAGE_CHOICES = [
        ("es", "Spanish"),
        ("en", "English"),
        ("fr", "French"),
    ]
    MODEL_CHOICES = [
        ("tiny", "Tiny"),
        ("base", "Base"),
        ("small", "Small"),
        ("medium", "Medium"),
        ("large", "Large"),
        ("large-v3", "Large v3"),
        
    ]

    file = models.FileField(null=True, blank=True, upload_to="input")
    language = models.CharField(max_length=10, choices=LANGUAGE_CHOICES, default="es")
    preprocess = models.BooleanField(default=True)
    model = models.CharField(max_length=50, choices=MODEL_CHOICES, default="tiny")


