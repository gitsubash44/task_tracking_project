from django.db import models
from django.contrib.auth.models import User

class Task(models.Model):

    title = models.CharField(max_length=255)
    description = models.TextField()
    assigned_to = models.ForeignKey(User, on_delete=models.CASCADE)
    due_date = models.DateField()
    priority = models.CharField(max_length=10)
    status = models.CharField(max_length=15)

    def __str__(self):
        return self.title



class TaskNew(models.Model):
    title = models.CharField(max_length=35)
    description = models.TextField(null=True, blank=True)
    due_date = models.DateField()
    due_time = models.TimeField()
    completed = models.BooleanField(default=False)

    def __str__(self) -> str:
        return f'{self.title}'
