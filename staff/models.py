from django.db import models
from administrator.models import *
# Create your models here.


class Staff(models.Model):
    department = models.ForeignKey(Department, on_delete=models.CASCADE)
    admin = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
