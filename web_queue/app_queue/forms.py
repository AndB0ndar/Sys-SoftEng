from django import forms
from django.contrib.auth.models import User
from .models import UserProfile, StudyGroup, Queues


class UserRegistrationForm(forms.ModelForm):
    """
    Form for user registration.
    This form allows users to register by providing their username, email, and password

    :param password: CharField for the user's password, with a PasswordInput widget for security
    :type password: django.db.models.CharField

    .. seealso:: Meta
    """
    password = forms.CharField(label='Password', widget=forms.PasswordInput)

    class Meta:
        """
        Meta class for defining options in the form

        :param model: The User model
        :type model: django.db.models.Model
        :param fields: The fields to include in the form, which are 'username', 'email', and 'password'
        :type fields: list
        """
        model = User
        fields = ['username', 'email', 'password']


class UserProfileForm(forms.ModelForm):
    """
    Form for updating user profile information.

    This form allows users to update their profile information, including the associated
    group, first name, and last name. Users can also optionally enter a new group name

    :param new_group_name: CharField for entering a new group name, max length of 100 characters,
                          not required.
    :type new_group_name: django.db.models.CharField

    .. seealso:: Meta
    """
    new_group_name = forms.CharField(max_length=100, required=False)

    class Meta:
        """
        Meta class for defining options in the form

        :ivar model: The UserProfile model
        :type model: django.db.models.Model
        :ivar fields: The fields to include in the form, which are 'group', 'new_group_name',
                      'first_name', and 'last_name'
        :type fields: list
        """
        model = UserProfile
        fields = ['group', 'new_group_name', 'first_name', 'last_name']

    def __init__(self, *args, **kwargs):
        """
        Initializes the UserProfileForm instance

        :param args: Positional arguments
        :type args: tuple
        :param kwargs: Keyword arguments
        :type kwargs: dict
        """
        super().__init__(*args, **kwargs)
        self.fields['group'].required = False

    def clean(self):
        """
        Validates the form data

        Ensures that either an existing group is selected or a new group name is provided

        :return: The cleaned form data
        :rtype: dict
        """
        cleaned_data = super().clean()
        group = cleaned_data.get('group')
        new_group_name = cleaned_data.get('new_group_name')
        if not group and not new_group_name:
            raise forms.ValidationError('You must choose an existing group or create a new one.')
        return cleaned_data

    def save(self, commit=True):
        """
        Saves the form data to the UserProfile model, creating a new group if necessary

        :param commit: Boolean indicating whether to save the data to the database immediately
        :type commit: bool, optional

        :return: The saved UserProfile instance
        :rtype: app_queue.model.UserProfile
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
    associated group, and a description

    .. seealso:: Meta
    """
    def __init__(self, *args, **kwargs):
        """
        Initializes the QueuesForm instance

        :param args: Positional arguments
        :type args: tuple
        :param kwargs: Keyword arguments
        :type kwargs: dict
        """
        super(QueuesForm, self).__init__(*args, **kwargs)

    class Meta:
        """
        Meta class for defining options in the form

        :param model: The Queues model
        :type model: django.db.models.Model
        :param fields: The fields to include in the form, which are 'name', 'group', and 'description'
        :type fields: list
        """
        model = Queues
        fields = ['name', 'group', 'description']
