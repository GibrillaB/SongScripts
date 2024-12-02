from django.db import models

# Create your models here.

class Query(models.Model):
    query_text = models.CharField(max_length=255)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"'{self.query_text}' at {self.timestamp}"