from django.contrib.auth import login
from django.db.models import Max
from django.http import HttpResponse
from django.shortcuts import render, redirect, get_object_or_404

from .forms import UserProfileForm, UserRegistrationForm, QueuesForm
from .models import Queues, Queue, UserProfile


def home(request):
    """
    Displays the home page of the queue application

    :param request: Django HttpRequest object
    :type request: django.http.HttpRequest

    :return: HttpResponse object with the rendered template 'app_queue/home.html'
    :rtype: django.http.HttpRequest
    """
    return render(request, 'app_queue/home.html')


def create_queue(request):
    """
    Displays the queue creation page and handles the POST request to create a new queue

    :param request: Django HttpRequest object
    :type request: django.http.HttpRequest

    :return: If the request method is POST and the form is valid, creates a new queue and redirects to the queues list page.
             Otherwise, displays the queue creation form with an empty or pre-filled form
    :rtype: django.http.HttpRequest
    """
    if request.method == 'POST':
        form = QueuesForm(request.POST)
        if form.is_valid():
            # group = request.user.userprofile.group
            # form.instance.group = group
            user = request.user.userprofile
            form.instance.creator = user
            queue = form.save()
            Queue.objects.create(queue=queue, user=user, position=0)
            return redirect('queues')
    else:
        group = request.user.userprofile.group
        form = QueuesForm(initial={'group': group})
    return render(request, 'app_queue/create_queue.html', {'form': form})


def queues(request):
    """
    Displays a list of queues associated with the currently logged-in user's group

    :param request: Django HttpRequest object
    :type request: django.http.HttpRequest

    :return: HttpResponse object with the rendered template 'app_queue/queues.html',
             including a dictionary containing 'user_queues' - the queues associated
             with the user's group
    :rtype: django.http.HttpRequest
    """
    user_queues = Queues.objects.filter(group=request.user.userprofile.group)
    return render(request, 'app_queue/queues.html', {'user_queues': user_queues})


def queue(request, pk):
    """
    Displays the details of a specific queue identified by its primary key (pk)

    :param request: Django HttpRequest object
    :type request: django.http.HttpRequest
    :param pk: Primary key of the queue to be displayed
    :type pk: int

    :return: HttpResponse object with the rendered template 'app_queue/queue.html',
             including a dictionary containing:
               - 'records': A sorted list of records in the queue.
               - 'queue_pk': The primary key of the queue being displayed.
               - 'user_pk': The primary key of the currently logged-in user.
    :rtype: django.http.HttpRequest
    """
    records = Queue.objects.filter(queue=pk)
    pos = 0
    for r in records:
        pos = r.position = pos + 1

    records = sorted(records, key=lambda x: x.position)
    context = {
        'records': records,
        'queue_pk': pk,
        'user_pk': request.user.userprofile.pk,
    }
    return render(request, 'app_queue/queue.html', context)


def get_max_position_record(queue_id):
    """
    Retrieves the record with the maximum position in the specified queue

    :param queue_id: ID of the queue for which the maximum position record is to be retrieved
    :type queue_id: int

    :return: The record with the maximum position in the specified queue, or None if the queue is empty
    :rtype: Queue or None
    """
    max_position_record = Queue.objects.filter(queue_id=queue_id).aggregate(Max('position'))
    max_position = max_position_record['position__max']
    if max_position is not None:
        record = Queue.objects.get(queue_id=queue_id, position=max_position)
        return record
    else:
        return None


def delete_user(request, pk, user_id):
    """
    Deletes a specific user from a queue

    :param request: Django HttpRequest object
    :type request: django.http.HttpRequest
    :param pk: Primary key of the queue from which the user should be deleted
    :type pk: int
    :param user_id: ID of the user to be deleted from the queue
    :type user_id: int

    :return: Redirects to the 'queue' view for the same queue (specified by pk) after
             deleting the user. If the queue does not exist or the user is not found
             in the queue, returns an HTTP 404 Not Found error
    :rtype: django.http.HttpResponseRedirect
    """
    record = get_object_or_404(Queue, queue=pk, user=user_id)
    record.delete()
    return redirect('queue', pk=pk)


def add_user(request, pk, user_id):
    """
    Adds a user to a queue

    :param request: Django HttpRequest object
    :type request: django.http.HttpRequest
    :param pk: Primary key of the queue to which the user should be added
    :type pk: int
    :param user_id: ID of the user to be added to the queue
    :type user_id: int

    :return: Redirects to the 'queue' view for the same queue (specified by pk) after
             adding the user. If the queue does not exist or the user is already in the queue,
             or an error occurs while determining the position, redirects back to the 'queue' view
    :rtype: django.http.HttpResponseRedirect
    """
    record = get_max_position_record(pk)
    if record is not None:
        if record.user.pk == user_id:
            return redirect('queue', pk=pk)
        position = record.position + 1
    else:
        position = 0
    Queue.objects.create(queue=Queues.objects.get(pk=pk), user=UserProfile.objects.get(pk=user_id), position=position)
    return redirect('queue', pk=pk)


def update_user(request, pk, user_id):
    """
    Updates the position of a user in a queue by deleting and re-adding them

    :param request: Django HttpRequest object
    :type request: django.http.HttpRequest
    :param pk: Primary key of the queue in which the user's position should be updated
    :type pk: int
    :param user_id: ID of the user whose position in the queue should be updated
    :type user_id: int

    :return: Redirects to the 'queue' view for the same queue (specified by pk) after
             updating the user's position. If the queue does not exist or the user is not found
             in the queue, returns an HTTP 404 Not Found error
    :rtype: django.http.HttpResponseRedirect
    """
    record = get_object_or_404(Queue, queue=pk, user=user_id)
    record.delete()

    record = get_max_position_record(pk)
    if record is not None:
        position = record.position + 1
    else:
        position = 0
    Queue.objects.create(queue=Queues.objects.get(pk=pk), user=UserProfile.objects.get(pk=user_id), position=position)

    return redirect('queue', pk=pk)


def register(request):
    """
    Handles user registration process

    :param request: Django HttpRequest object
    :type request: django.http.HttpRequest

    :return: If the request method is POST and both user and profile forms are valid,
             registers the user, logs them in, and redirects to the 'home' page.
             Otherwise, renders the registration form with empty or pre-filled forms
    :rtype: django.http.HttpRequest
    """
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


def profile(request):
    """
    Displays and handles updates to the user's profile

    :param request: Django HttpRequest object
    :type request: django.http.HttpRequest

    :return: If the request method is POST and the form is valid, updates the user's profile
             data and redirects to the 'user_profile' page.
             Otherwise, renders the profile form with the user's current profile data
    :rtype: django.http.HttpRequest
    """
    user_profile = UserProfile.objects.get(user=request.user)
    if request.method == 'POST':
        form = UserProfileForm(request.POST, instance=user_profile)
        if form.is_valid():
            # Обновляем данные профиля пользователя
            user_profile = form.save(commit=False)
            user = request.user
            user.username = form.cleaned_data['username']
            user.save()
            user_profile.save()
            return redirect('user_profile')
    else:
        form = UserProfileForm(instance=user_profile, initial={'username': request.user.username})
    return render(request, 'app_queue/profile.html', {'form': form})
