from django.contrib.auth.models import User
from django.db import models
from django.urls import reverse


class StudyGroup(models.Model):
    """
    Model representing a study group.
    This model stores information about study groups, including their name

    :param name: CharField representing the name of the study group, with a maximum length of 100 characters
    :type name: django.db.models.CharField
    """

    name = models.CharField(max_length=100)

    def __str__(self):
        """
        Returns a string representation of the study group.

        :return: The name of the study group.
        :rtype: str
        """
        return self.name


class UserProfile(models.Model):
    """
    Model representing a user profile.

    This model stores additional information about users, including their associated user object,
    study group, first name, and last name

    :param user: OneToOneField representing the associated User object
    :type user: django.db.models.OneToOneField
    :param group: ForeignKey representing the associated StudyGroup
    :type group: django.db.models.ForeignKey
    :param first_name: CharField representing the first name of the user, with a maximum length of 100 characters
    :type first_name: django.db.models.CharField
    :param last_name: CharField representing the last name of the user, with a maximum length of 100 characters
    :type last_name: django.db.models.CharField
    """

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    group = models.ForeignKey(StudyGroup, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)

    def __str__(self):
        """
        Returns a string representation of the user profile.

        :return: The concatenation of the user's first name and last name.
        :rtype: str
        """
        return f"{self.first_name} {self.last_name}"



class Queues(models.Model):
    """
    Model representing a queue.

    This model stores information about queues, including their name, creator, associated group,
    description, and creation timestamp

    :param name: CharField representing the name of the queue, with a maximum length of 100 characters
    :type name: django.db.models.CharField
    :param creator: ForeignKey representing the creator of the queue, associated with a UserProfile
    :type creator: django.db.models.ForeignKey
    :param group: ForeignKey representing the associated StudyGroup for the queue
    :type group: django.db.models.ForeignKey
    :param description: TextField representing a description of the queue, optional
    :type description: django.db.models.TextField
    :param created_at: DateTimeField representing the timestamp when the queue was created, automatically
                      set to the current date and time upon creation
    :type created_at: django.db.models.DateTimeField
    """

    name = models.CharField(max_length=100)

    creator = models.ForeignKey(UserProfile, on_delete=models.CASCADE, null=True, blank=True)
    group = models.ForeignKey(StudyGroup, on_delete=models.CASCADE, null=True, blank=True)

    description = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def get_path(self):
        """
        Returns the URL path for accessing the queue detail view

        :return: The URL path for the queue detail view, including the queue's primary key
        :rtype: str
        """
        return reverse('queue', args=[str(self.pk)])

    def __str__(self):
        """
        Returns a string representation of the queue

        :return: The name of the queue
        :rtype: str
        """
        return self.name



class Queue(models.Model):
    """
    Model representing a user's position in a queue.

    This model stores information about a user's position in a specific queue,
    including the queue itself, the user, and their position in the queue

    :param queue: ForeignKey representing the associated queue
    :type queue: django.db.models.ForeignKey
    :param user: ForeignKey representing the user in the queue, associated with a UserProfile
    :type user: django.db.models.ForeignKey
    :param position: IntegerField representing the user's position in the queue
    :type position: django.db.models.IntegerField
    """
    queue = models.ForeignKey(Queues, on_delete=models.CASCADE)
    user = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    position = models.IntegerField()

