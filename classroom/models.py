from django.db import models
from administrator.models import Session, Course
from student.models import Student
from account.models import CustomUser
from django.core.validators import MinValueValidator
from ckeditor_uploader.fields import RichTextUploadingField
# Create your models here.


class Assignment(models.Model):
    import datetime
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    question = RichTextUploadingField()
    session = models.ForeignKey(Session, null=True, on_delete=models.SET_NULL)
    created_date = models.DateTimeField(auto_now_add=True)
    edited_date = models.DateTimeField(auto_now=True)
    expiry_date = models.DateField(
        validators=[MinValueValidator(datetime.date.today() + datetime.timedelta(days=1))])


class Submission(models.Model):
    assignment = models.ForeignKey(Assignment, on_delete=models.CASCADE)
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    answer = RichTextUploadingField()
    submission_date = models.DateTimeField(auto_now_add=True)


class Stream(models.Model):
    message = models.CharField(max_length=200)
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    date = models.DateTimeField(auto_now_add=True)
    session = models.ForeignKey(Session, null=True, on_delete=models.CASCADE)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)


class StreamReply(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    message = models.CharField(max_length=200)
    date = models.DateTimeField(auto_now_add=True)
    stream = models.ForeignKey(Stream, on_delete=models.CASCADE)
