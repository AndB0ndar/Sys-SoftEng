from django.contrib.auth.models import User
from django.db import models
from django.urls import reverse


class StudyGroup(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    group = models.ForeignKey(StudyGroup, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.first_name} {self.last_name}"


class Queues(models.Model):
    name = models.CharField(max_length=100)

    creator = models.ForeignKey(UserProfile, on_delete=models.CASCADE, null=True, blank=True)
    group = models.ForeignKey(StudyGroup, on_delete=models.CASCADE, null=True, blank=True)

    description = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def get_path(self):
        return reverse('queue', args=[str(self.pk)])

    def __str__(self):
        return self.name


class Queue(models.Model):
    queue = models.ForeignKey(Queues, on_delete=models.CASCADE)
    user = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    position = models.IntegerField()

