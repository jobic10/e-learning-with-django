from django.db import models
from administrator.models import Department, Session, Course
from account.models import CustomUser
# Create your models here.


class Student(models.Model):
    regno = models.CharField(max_length=15, unique=True)
    department = models.ForeignKey(
        Department, on_delete=models.SET_NULL, null=True)
    dob = models.DateField()
    admin = models.OneToOneField(CustomUser, on_delete=models.CASCADE)


class CourseRegistration(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    approved = models.BooleanField(null=True)  # By course lecturer
    session = models.ForeignKey(Session, on_delete=models.CASCADE)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    first_test = models.FloatField(default=0)  # Max 20
    second_test = models.FloatField(default=0)  # Max 20
    exam = models.FloatField(default=0)  # Max : 60
