from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Task(models.Model):

    def __str__(self):
        return self.title + ' -> ' + self.user.username

    title = models.CharField(max_length=100)
    description = models.TextField(blank=True, max_length=250)
    created = models.DateTimeField(auto_now_add=True)
    datecompleted = models.DateTimeField(null=True, blank=True) #La completa el usuario
    is_important = models.BooleanField(default=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE)