from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserChangeForm
from django.contrib import messages
from . models import Task
from . forms import CustomUserChangeForm, ProfileUpdateForm
from . models import Profile
from . forms import TaskForm


from django.contrib.auth.views import LogoutView

class CustomLogoutView(LogoutView):
    def get(self, request, *args, **kwargs):
        return self.post(request, *args, **kwargs)



# Create your views here.
@login_required
def add_task(request):
    if request.method == 'POST':
        form = TaskForm(request.POST)
        if form.is_valid():
            task = form.save(commit=False)
            task.user = request.user  # If Task has a user field
            task.save()
            return redirect('dashboard')
    else:
        form = TaskForm()
    return render(request, 'todo/add_task.html', {'form': form})


def register(request):
    if request.user.is_authenticated:
        return redirect('index')
    
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user) #auto login after register
            return redirect('index')
    else:
        form = UserCreationForm()
    return render(request, 'todo/register.html', {'form': form})


@login_required
def index(request):
    # tasks = Task.objects.all().order_by('-created_at')
    tasks = Task.objects.filter(user=request.user).order_by('-created_at')

    if request.method == 'POST':
        title = request.POST.get('title')

        if title:
            Task.objects.create(title = title, user=request.user)
            return redirect('index')
        
    return render(request, 'todo/index.html', {'tasks': tasks})

@login_required
def delete_task(request, task_id):
    # task = Task.objects.get(id = task_id)
    task = get_object_or_404(Task, id=task_id, user=request.user)
    task.delete()
    return redirect('index')

@login_required
def mark_complete(request, task_id):
    task = Task.objects.get(id=task_id, user=request.user)
    task.completed = True
    task.save()
    return redirect('index')

@login_required
def toggle_complete(request, task_id):
    task = get_object_or_404(Task, id=task_id, user=request.user)
    task.completed = not task.completed  # ✅ toggle logic
    task.save()
    return redirect('index')

def edit_task(request, task_id):
    task = get_object_or_404(Task, id=task_id, user=request.user)

    if request.method == 'POST':
        new_title = request.POST.get('title')
        if new_title:
            task.title = new_title
            task.save()
            return redirect('index')

    return render(request, 'todo/edit.html', {'task': task})

@login_required
def dashboard(request):
    user = request.user
    tasks = Task.objects.filter(user=user).order_by('-created_at')

    total = tasks.count()
    completed = tasks.filter(completed=True).count()
    pending = total - completed

    context = {
        'user': user,
        'tasks': tasks,
        'total': total,
        'completed': completed,
        'pending': pending,
    }
    return render(request, 'todo/dashboard.html', context)


@login_required
def edit_profile(request):
    profile, created = Profile.objects.get_or_create(user=request.user)

    if request.method == 'POST':
        form = ProfileUpdateForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            form.save()
            return redirect('dashboard')
    else:
        form = ProfileUpdateForm(instance=profile)

    return render(request, 'todo/edit_profile.html', {'form': form})
