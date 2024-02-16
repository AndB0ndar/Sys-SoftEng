from django.contrib.auth import login
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required

from .forms import UserProfileForm, UserRegistrationForm


def home(request):
    return render(request, 'app_queue/home.html')


def queues(request):
    return render(request, 'app_queue/queues.html')


def queue(request, title):
    return render(request, 'app_queue/queue.html')


def register(request):
    if request.method == 'POST':
        user_form = UserRegistrationForm(request.POST)
        profile_form = UserProfileForm(request.POST)
        if user_form.is_valid() and profile_form.is_valid():
            user = user_form.save()
            user.set_password(user_form.cleaned_data['password'])
            user.save()
            profile = profile_form.save(commit=False)
            profile.user = user
            profile.save()
            login(request, user)
            return redirect('home')
    else:
        user_form = UserRegistrationForm()
        profile_form = UserProfileForm()
    return render(request, 'registration/register.html', {'user_form': user_form, 'profile_form': profile_form})

