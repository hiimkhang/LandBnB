from django.contrib.auth.models import AbstractUser 
from django.shortcuts import reverse
from django.db import models
from core import managers as core_managers

class User(AbstractUser):
    GENDER_MALE = "male"
    GENDER_FEMALE = "female"
    GENDER_CHOICES = (
        (GENDER_MALE, "Male"),
        (GENDER_FEMALE, "Female"),
    )

    LANGUAGE_ENGLISH = "en"
    LANGUAGE_VIETNAMESE = "vi"
    LANGUAGE_CHOICES = (
        (LANGUAGE_ENGLISH, "English"),
        (LANGUAGE_VIETNAMESE, "Vietnamese"),
    )

    LOGIN_EMAIL = "email"

    avatar = models.ImageField(null=True, blank=True)
    gender = models.CharField(choices=GENDER_CHOICES, max_length=10, null=True, blank=True)
    language = models.CharField(choices=LANGUAGE_CHOICES, max_length=2)
    birthday = models.DateField(null=True)
    superhost = models.BooleanField(default=False)
    bio = models.TextField(default="", blank=True)

    # objects = core_managers.CustomModelManager()

    def get_absolute_url(self):
        return reverse("users:profile", kwargs={"pk": self.pk})

    pass