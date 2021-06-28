from django.db import models
from django.contrib.auth.models import User

# Create your models here.


class Todo(models.Model):
    status_choice = [
        ('C', 'Completed'),
        ('F', 'Pending')
    ]
    title = models.CharField(max_length=50)
    status = models.CharField(max_length=2, choices=status_choice)
    date = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
