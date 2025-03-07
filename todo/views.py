from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.forms import UserCreationForm
from .models import Task
from .forms import TaskForm
from datetime import datetime, timedelta

# Home page (Redirects to login if not authenticated)
def home(request):
    if request.user.is_authenticated:
        return redirect('task_list')
    return render(request, 'home.html')

# User Registration
def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)  # Auto-login after registration
            return redirect('task_list')
    else:
        form = UserCreationForm()
    return render(request, 'register.html', {'form': form})

# User Login
def user_login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('task_list')
        else:
            return render(request, 'login.html', {'error': 'Invalid username or password'})
    return render(request, 'login.html')

# User Logout (Session-based)
@login_required
def user_logout(request):
    logout(request)
    return redirect('login')  # Redirects to login page instead of home

# View All Tasks
@login_required
def task_list(request):
    tasks = Task.objects.filter(user=request.user).order_by('due_date', 'priority')

    # Filtering based on GET parameters
    category_filter = request.GET.get('category')
    priority_filter = request.GET.get('priority')

    if category_filter:
        tasks = tasks.filter(category=category_filter)

    if priority_filter:
        tasks = tasks.filter(priority=priority_filter)

    # Calculate time left for each task
    now = datetime.now()
    for task in tasks:
        if task.due_date:
            due_datetime = datetime.combine(task.due_date, datetime.min.time())  
            time_remaining = due_datetime - now

            if time_remaining.total_seconds() < 0:
                task.time_left = "⏳ Overdue!"
            else:
                days = time_remaining.days
                hours, remainder = divmod(time_remaining.seconds, 3600)
                minutes, _ = divmod(remainder, 60)
                task.time_left = f"{days}d {hours}h {minutes}m left"
        else:
            task.time_left = "No Deadline"

    return render(request, 'task_list.html', {'tasks': tasks})

# Create a Task
@login_required
def task_create(request):
    if request.method == 'POST':
        form = TaskForm(request.POST)
        if form.is_valid():
            task = form.save(commit=False)
            task.user = request.user  # Assign task to logged-in user
            task.save()
            return redirect('task_list')
    else:
        form = TaskForm()
    return render(request, 'task_form.html', {'form': form})

# Update a Task
@login_required
def task_update(request, task_id):
    task = get_object_or_404(Task, id=task_id, user=request.user)
    
    if request.method == 'POST':
        form = TaskForm(request.POST, instance=task)
        if form.is_valid():
            form.save()
            return redirect('task_list')
    else:
        form = TaskForm(instance=task)

    return render(request, 'task_form.html', {'form': form})

# Delete a Task
@login_required
def task_delete(request, task_id):
    task = get_object_or_404(Task, id=task_id, user=request.user)

    if request.method == 'POST':
        task.delete()
        return redirect('task_list')

    return render(request, 'task_confirm_delete.html', {'task': task})
