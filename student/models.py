from django.db import models
from administrator.models import Department, Session, Course
from account.models import CustomUser
# Create your models here.


class Student(models.Model):
    regno = models.CharField(max_length=15, unique=True)
    department = models.ForeignKey(Department, on_delete=models.CASCADE)
    dob = models.DateField()
    admin = models.OneToOneField(CustomUser, on_delete=models.CASCADE)


class Registration(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    session = models.ForeignKey(Session, on_delete=models.CASCADE)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    first_test = models.FloatField(default=0)  # Max 20
    second_test = models.FloatField(default=0)  # Max 20
    exam = models.FloatField(default=0)  # Max : 60
