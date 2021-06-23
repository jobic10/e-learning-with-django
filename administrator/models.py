from django.db import models
from account.models import CustomUser
from django.core.validators import ValidationError


class Department(models.Model):
    name = models.CharField(max_length=40, unique=True)
    is_general = models.BooleanField(default=False)

    def __str__(self):
        return self.name


class Course(models.Model):
    name = models.CharField(max_length=50)
    code = models.CharField(max_length=10, unique=True)
    unit = models.IntegerField()
    department = models.ForeignKey(Department, on_delete=models.CASCADE)


class Session(models.Model):
    year = models.CharField(max_length=10, unique=True)  # E.g. 2020/2021

    def __str__(self):
        return self.year


class Settings(models.Model):
    facebook_url = models.URLField(null=True)
    twitter_url = models.URLField(null=True)
    github_url = models.URLField(null=True)
    address = models.CharField(max_length=100, null=True)
    email = models.EmailField(default="jobowonubi@gmail.com")
    phone = models.CharField(max_length=15, default="08100134741")
    current_academic_session = models.OneToOneField(
        Session, on_delete=models.SET_NULL, null=True)

    """
    https://stackoverflow.com/questions/39412968/allow-only-one-instance-of-a-model-in-django
    Since we need just one instance of settings
    """

    def is_valid(self, *args, **kwargs):
        if not self.pk and Settings.objects.exists():
            # if you'll not check for self.pk
            # then error will also raised in update of exists model
            raise ValidationError('Update Settings Instead')
        return super(Settings, self).is_valid(*args, **kwargs)
