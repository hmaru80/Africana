from django.db import models
from polls.models import CartItem,Product
from django.contrib.auth.models import User

# Create your models here.


class Task(models.Model):
    
    title = models.CharField(max_length=200)
    description = models.TextField()
    completed = models.BooleanField(default=False)
    created_on=models.DateTimeField(auto_now_add=True )
    due_by=models.DateTimeField(blank=True, null=True)
    phone= models.CharField(max_length=13, default=False)
    

    def __str__(self):
        return self.title