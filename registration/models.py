from django.contrib.auth.models import User
from django.db import models

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    elo = models.IntegerField(default=1200)
    member1_name = models.CharField(max_length=20, default='')
    member1_id = models.CharField(max_length=20, default='')
    member1_class = models.CharField(max_length=20, default='')
    member2_name = models.CharField(max_length=20, default='')
    member2_id = models.CharField(max_length=20, default='')
    member2_class = models.CharField(max_length=20, default='')
    member3_name = models.CharField(max_length=20, default='')
    member3_id = models.CharField(max_length=20, default='')
    member3_class = models.CharField(max_length=20, default='')