from django.db import models
from . import managers
# Create your models here.
class TimeStampedModel(models.Model):
    """Time Stamped Abstract Definition"""

    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)
    objects = managers.CustomModelManager()
    class Meta:
        abstract = True