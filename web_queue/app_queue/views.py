from django.contrib.auth import login
from django.db.models import Max
from django.shortcuts import render, redirect, get_object_or_404

from .forms import UserProfileForm, UserRegistrationForm, QueuesForm
from .models import Queues, Queue, UserProfile


def home(request):
    return render(request, 'app_queue/home.html')


def create_queue(request):
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
    print(request.user.userprofile.group)
    user_queues = Queues.objects.filter(group=request.user.userprofile.group)
    return render(request, 'app_queue/queues.html', {'user_queues': user_queues})


def queue(request, pk):
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
    max_position_record = Queue.objects.filter(queue_id=queue_id).aggregate(Max('position'))
    max_position = max_position_record['position__max']
    if max_position is not None:
        record = Queue.objects.get(queue_id=queue_id, position=max_position)
        return record
    else:
        return None


def delete_user(request, pk, user_id):
    record = get_object_or_404(Queue, queue=pk, user=user_id)
    record.delete()
    return redirect('queue', pk=pk)


def add_user(request, pk, user_id):
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

