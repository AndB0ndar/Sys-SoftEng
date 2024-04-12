from django.contrib.auth.models import User
from django.db import models
from django.urls import reverse


class StudyGroup(models.Model):
    """
    Model representing a study group.

    This model stores information about study groups, including their name.

    Attributes:
    - name: CharField representing the name of the study group, with a maximum length of 100 characters.

    Methods:
    - __str__: Returns a string representation of the study group, which is its name.
    """
    name = models.CharField(max_length=100)

    def __str__(self):
        """
        Returns a string representation of the study group.

        Returns:
        - The name of the study group.
        """
        return self.name


class UserProfile(models.Model):
    """
    Model representing a user profile.

    This model stores additional information about users, including their associated user object,
    study group, first name, and last name.

    Attributes:
    - user: OneToOneField representing the associated User object.
    - group: ForeignKey representing the associated StudyGroup.
    - first_name: CharField representing the first name of the user, with a maximum length of 100 characters.
    - last_name: CharField representing the last name of the user, with a maximum length of 100 characters.

    Methods:
    - __str__: Returns a string representation of the user profile, which is the concatenation of the
               user's first name and last name.
    """
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    group = models.ForeignKey(StudyGroup, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)

    def __str__(self):
        """
        Returns a string representation of the user profile.

        Returns:
        - The concatenation of the user's first name and last name.
        """
        return f"{self.first_name} {self.last_name}"


class Queues(models.Model):
    """
    Model representing a queue.

    This model stores information about queues, including their name, creator, associated group,
    description, and creation timestamp.

    Attributes:
    - name: CharField representing the name of the queue, with a maximum length of 100 characters.
    - creator: ForeignKey representing the creator of the queue, associated with a UserProfile.
    - group: ForeignKey representing the associated StudyGroup for the queue.
    - description: TextField representing a description of the queue, optional.
    - created_at: DateTimeField representing the timestamp when the queue was created, automatically
                  set to the current date and time upon creation.

    Methods:
    - get_path: Returns the URL path for accessing the queue detail view.
    - __str__: Returns a string representation of the queue, which is its name.
    """
    name = models.CharField(max_length=100)

    creator = models.ForeignKey(UserProfile, on_delete=models.CASCADE, null=True, blank=True)
    group = models.ForeignKey(StudyGroup, on_delete=models.CASCADE, null=True, blank=True)

    description = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def get_path(self):
        """
        Returns the URL path for accessing the queue detail view.

        Returns:
        - The URL path for the queue detail view, including the queue's primary key.
        """
        return reverse('queue', args=[str(self.pk)])

    def __str__(self):
        """
        Returns a string representation of the queue.

        Returns:
        - The name of the queue.
        """
        return self.name


class Queue(models.Model):
    """
    Model representing a user's position in a queue.

    This model stores information about a user's position in a specific queue,
    including the queue itself, the user, and their position in the queue.

    Attributes:
    - queue: ForeignKey representing the associated queue.
    - user: ForeignKey representing the user in the queue, associated with a UserProfile.
    - position: IntegerField representing the user's position in the queue.
    """
    queue = models.ForeignKey(Queues, on_delete=models.CASCADE)
    user = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    position = models.IntegerField()

