from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User

# Create your models here.
class Feature(models.Model):
    name = models.CharField(max_length=100, default="NONE")
    details = models.CharField(max_length=500, default="Not yet specified")


class Event(models.Model):
    priority_choices = [
        ('low', 'Low'),
        ('medium', 'Medium'),
        ('high', 'High'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=100, default="NONE")
    details = models.CharField(max_length=500, default="Not yet specified")
    deadline = models.DateTimeField(default=timezone.now)
    priority = models.CharField(max_length=10, choices=priority_choices, default='medium')

    def __str__(self):
        return self.name