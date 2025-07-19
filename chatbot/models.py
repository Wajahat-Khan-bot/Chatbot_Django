from django.db import models
import uuid

class Business(models.Model):
    name         = models.CharField(max_length=255)
    identifier   = models.SlugField(unique=True)
    access_token = models.CharField(max_length=64, default=uuid.uuid4, unique=True)
    services     = models.TextField()
    location     = models.URLField()
    email        = models.EmailField()
    phone        = models.CharField(max_length=20)

    def __str__(self):
        return self.name
