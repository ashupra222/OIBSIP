from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    email = models.EmailField(unique=True, null=False)
    otp = models.PositiveIntegerField(null=True)
    verified = models.BooleanField(null=False, auto_created=False, default=False)

    def __str__(self) -> str:
        return self.first_name + ' ' + self.last_name
