import os
from django.db import models

class Image(models.Model):
    name = models.CharField(max_length=255)
    path = models.ImageField(upload_to='images/')
    size = models.PositiveIntegerField(default=0)
    date = models.DateTimeField(auto_now_add=True)
    extracted_text = models.TextField(blank=True, null=True)

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        if self.path:
            self.size = self.path.size
            super().save(update_fields=['size'])

    def delete(self, *args, **kwargs):
        if self.path and os.path.isfile(self.path.path):
            os.remove(self.path.path)
        super().delete(*args, **kwargs)

    def __str__(self):
        return self.name
