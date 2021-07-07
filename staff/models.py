from django.db import models
from administrator.models import *
# Create your models here.


class Staff(models.Model):
    department = models.ForeignKey(
        Department, on_delete=models.SET_NULL, null=True)
    admin = models.OneToOneField(CustomUser, on_delete=models.CASCADE)

    def __str__(self):
        return str(self.admin)


class CourseAllocation(models.Model):
    staff = models.ForeignKey(Staff, on_delete=models.CASCADE)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    session = models.ForeignKey(Session, null=True, on_delete=models.SET_NULL)
    approved = models.BooleanField(null=True)  # * To be reviewed by admin
    registered_date = models.DateTimeField(auto_now_add=True)
    response_date = models.DateTimeField(auto_now=True)

    def __str__(self):
        return str(self.course) + " assigned to " + str(self.staff) + " with status : " + str(self.approved)


class Assignment(models.Model):
    staff = models.ForeignKey(Staff, on_delete=models.CASCADE)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    session = models.ForeignKey(Session, null=True, on_delete=models.SET_NULL)
    created_date = models.DateTimeField(auto_now_add=True)
    edited_date = models.DateTimeField(auto_now=True)
    expiry_date = models.DateField()
