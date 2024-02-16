from django.contrib.auth.models import User
from django.db import models


class StudyGroup(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Subject(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)

    def __str__(self):
        return self.name


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    group = models.ForeignKey(StudyGroup, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.first_name} {self.last_name}"


class Queue(models.Model):
    name = models.CharField(max_length=100)
    creator = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    group = models.ForeignKey(StudyGroup, on_delete=models.CASCADE, null=True, blank=True)
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE, null=True, blank=True)
    description = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name
