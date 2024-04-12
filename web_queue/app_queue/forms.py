from django import forms
from django.contrib.auth.models import User
from .models import UserProfile, StudyGroup, Queues


class UserRegistrationForm(forms.ModelForm):
    """
    Form for user registration.

    This form allows users to register by providing their username, email, and password.

    Attributes:
    - password: CharField for the user's password, with a PasswordInput widget for security.

    Meta:
    - model: The User model.
    - fields: The fields to include in the form, which are 'username', 'email', and 'password'.
    """
    password = forms.CharField(label='Password', widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ['username', 'email', 'password']


class UserProfileForm(forms.ModelForm):
    """
    Form for updating user profile information.

    This form allows users to update their profile information, including the associated
    group, first name, and last name. Users can also optionally enter a new group name.

    Attributes:
    - new_group_name: CharField for entering a new group name, max length of 100 characters,
                      not required.

    Meta:
    - model: The UserProfile model.
    - fields: The fields to include in the form, which are 'group', 'new_group_name',
              'first_name', and 'last_name'.

    Methods:
    - __init__: Initializes the UserProfileForm instance.
    - clean: Validates the form data to ensure either an existing group is selected or
             a new group name is provided.
    - save: Saves the form data to the UserProfile model, creating a new group if necessary.
    """
    new_group_name = forms.CharField(max_length=100, required=False)

    class Meta:
        model = UserProfile
        fields = ['group', 'new_group_name', 'first_name', 'last_name']

    def __init__(self, *args, **kwargs):
        """
        Initializes the UserProfileForm instance.

        Parameters:
        - *args: Positional arguments.
        - **kwargs: Keyword arguments.
        """
        super().__init__(*args, **kwargs)
        self.fields['group'].required = False

    def clean(self):
        """
        Validates the form data.

        Ensures that either an existing group is selected or a new group name is provided.

        Returns:
        - The cleaned form data.
        """
        cleaned_data = super().clean()
        group = cleaned_data.get('group')
        new_group_name = cleaned_data.get('new_group_name')
        if not group and not new_group_name:
            raise forms.ValidationError('You must choose an existing group or create a new one.')
        return cleaned_data

    def save(self, commit=True):
        """
        Saves the form data to the UserProfile model, creating a new group if necessary.

        Parameters:
        - commit: Boolean indicating whether to save the data to the database immediately.

        Returns:
        - The saved UserProfile instance.
        """
        instance = super().save(commit=False)
        new_group_name = self.cleaned_data.get('new_group_name')

        if new_group_name:
            group, created = StudyGroup.objects.get_or_create(name=new_group_name)
            instance.group = group

        if commit:
            instance.save()
        return instance


class QueuesForm(forms.ModelForm):
    """
    Form for creating or updating a queue.

    This form allows users to create or update a queue by providing its name,
    associated group, and a description.

    Meta:
    - model: The Queues model.
    - fields: The fields to include in the form, which are 'name', 'group', and 'description'.
    """
    def __init__(self, *args, **kwargs):
        """
        Initializes the QueuesForm instance.

        Parameters:
        - *args: Positional arguments.
        - **kwargs: Keyword arguments.
        """
        super(QueuesForm, self).__init__(*args, **kwargs)

    class Meta:
        model = Queues
        fields = ['name', 'group', 'description']
