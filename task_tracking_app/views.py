from django.shortcuts import render, redirect, get_object_or_404
from django.shortcuts import get_object_or_404
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.decorators import login_required
from .forms import UserRegistrationForm, TaskForm
from .models import Task, TaskNew
# Create your views here.


def register(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')
    else:
        form = UserRegistrationForm()
    return render(request, 'register.html', {'form': form})


def user_login(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('dashboard')  # Redirect to dashboard after successful login
    else:
        form = AuthenticationForm()
    return render(request, 'login.html', {'form': form})

@login_required
def dashboard(request):
    tasks = Task.objects.filter(assigned_to=request.user)
    return render(request, 'dashboard.html', {'tasks': tasks})

@login_required
def task_detail(request, task_id):
    task = get_object_or_404(Task, id=task_id)
    return render(request, 'task_detail.html', {'task': task})

@login_required
def create_task(request):
    if request.method == 'POST':
        form = TaskForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('dashboard')
    else:
        form = TaskForm()
    return render(request, 'create_edit_task.html', {'form': form})

@login_required
def edit_task(request, task_id):
    task = get_object_or_404(Task, id=task_id)
    if request.method == 'POST':
        form = TaskForm(request.POST, instance=task)
        if form.is_valid():
            form.save()
            return redirect('dashboard')
    else:
        form = TaskForm(instance=task)
    return render(request, 'create_edit_task.html', {'form': form})

# Create views here.
def home(request):
    tasks = TaskNew.objects.all()

    return render(request, 'dashboard.html', {
        'tasks': tasks,
    })

def completed(request):
    completed_tasks = TaskNew.objects.filter(completed=True)

    return render(request, 'completed.html', {
        'tasks': completed_tasks,
    })

def remaining(request):
    remaining_tasks = TaskNew.objects.filter(completed=False)
    return render(request, 'remaining.html', {
        'tasks': remaining_tasks,
    })
    
    
    
    
    # CRUD
    
    
def add_task(request):
    if request.method == "POST":
        title = request.POST.get('title')
        description = request.POST.get('description')
        due_date = request.POST.get('due_date')
        due_time = request.POST.get('due_time')
        completed = False

        if title and due_date and due_time:
            task = TaskNew( 
                title=title,
                description=description,
                due_date=due_date,
                due_time=due_time,
                completed=completed
            )
            task.save()
            return redirect('home')
    return render(request, 'add_task.html')


def delete_task(request, task_id):
    task = TaskNew.objects.get(id=task_id)
    return render(request, 'delete.html', {
        "task": task,
    })

def task_detail(request, task_id):
    task = TaskNew.objects.get(id=task_id)
    return render(request, 'task_detail.html', {
        "task": task,
    })


def toggle_complete(request, task_id):
    task = get_object_or_404(TaskNew, id=task_id)
    task.completed = not task.completed  # Toggle the completed status
    task.save()  # Save the changes to the task
    return redirect('home')


def remove_task(request, task_id):
    task = TaskNew.objects.get(id=task_id)
    if task:
        task.delete()
        return redirect('home')
