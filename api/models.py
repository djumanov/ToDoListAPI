from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MaxValueValidator, MinValueValidator

class Task(models.Model):
    '''Task schema'''

    title = models.CharField(max_length=63)
    description = models.CharField(max_length=255, blank=True, default='')
    is_completed = models.BooleanField(default=False, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    duedate = models.DateTimeField()
    importance = models.SmallIntegerField(
        default=0,
        blank=True,
        validators=[
            MaxValueValidator(5),
            MinValueValidator(0)
        ]
    )
    user = models.ForeignKey(to=User, on_delete=models.CASCADE)

    def __str__(self):
        return self.title