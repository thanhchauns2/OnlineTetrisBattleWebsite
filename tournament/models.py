# models.py
from django.db import models
from django.contrib.auth.models import User

class SelectedUser(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    # Các trường khác nếu cần

    def __str__(self):
        return self.user.username
