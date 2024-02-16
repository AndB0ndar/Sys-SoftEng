from django import forms
from django.contrib.auth.models import User
from .models import UserProfile, StudyGroup


class UserRegistrationForm(forms.ModelForm):
    password = forms.CharField(label='Password', widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ['username', 'email', 'password']


class UserProfileForm(forms.ModelForm):
    # Добавляем поле для имени группы
    new_group_name = forms.CharField(max_length=100, required=False)

    class Meta:
        model = UserProfile
        fields = ['group', 'new_group_name', 'first_name', 'last_name']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['group'].required = False

    def clean(self):
        cleaned_data = super().clean()
        group = cleaned_data.get('group')
        new_group_name = cleaned_data.get('new_group_name')

        if not group and not new_group_name:
            raise forms.ValidationError('You must choose an existing group or create a new one.')

        return cleaned_data

    def save(self, commit=True):
        instance = super().save(commit=False)
        new_group_name = self.cleaned_data.get('new_group_name')

        if new_group_name:
            group, created = StudyGroup.objects.get_or_create(name=new_group_name)
            instance.group = group

        if commit:
            instance.save()
        return instance
