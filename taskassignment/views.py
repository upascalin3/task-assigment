from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.http import JsonResponse
from django.core.paginator import Paginator
from taskassignment.models import *
from taskassignment.forms import *

# Create your views here.

# ==================== CONTRIBUTOR VIEWS ====================

def contributor_list(request):
    """List all contributors with pagination"""
    contributors_list = Contributor.objects.all().order_by('name')
    
    # Get page size from request, default to 10
    page_size = request.GET.get('page_size', '10')
    try:
        page_size = int(page_size)
        if page_size not in [5, 10, 20, 50]:
            page_size = 10
    except (ValueError, TypeError):
        page_size = 10
    
    # Pagination
    paginator = Paginator(contributors_list, page_size)
    page_number = request.GET.get('page')
    contributors = paginator.get_page(page_number)
    
    return render(request, 'taskassignment/contributor_list.html', {
        'contributors': contributors,
        'page_size': page_size,
        'page_sizes': [5, 10, 20, 50]
    })

def contributor_detail(request, pk):
    """View details of a specific contributor"""
    contributor = get_object_or_404(Contributor, pk=pk)
    tasks = Task.objects.filter(contributor=contributor)
    return render(request, 'taskassignment/contributor_detail.html', {
        'contributor': contributor,
        'tasks': tasks
    })

def contributor_create(request):
    """Create a new contributor"""
    if request.method == 'POST':
        form = ContributorForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Contributor created successfully!')
            return redirect('taskassignment:contributor_list')
    else:
        form = ContributorForm()
    return render(request, 'taskassignment/contributor_form.html', {'form': form, 'title': 'Create Contributor'})

def contributor_update(request, pk):
    """Update an existing contributor"""
    contributor = get_object_or_404(Contributor, pk=pk)
    if request.method == 'POST':
        form = ContributorForm(request.POST, instance=contributor)
        if form.is_valid():
            form.save()
            messages.success(request, 'Contributor updated successfully!')
            return redirect('taskassignment:contributor_detail', pk=pk)
    else:
        form = ContributorForm(instance=contributor)
    return render(request, 'taskassignment/contributor_form.html', {
        'form': form, 
        'title': 'Update Contributor',
        'contributor': contributor
    })

def contributor_delete(request, pk):
    """Delete a contributor"""
    contributor = get_object_or_404(Contributor, pk=pk)
    if request.method == 'POST':
        contributor.delete()
        messages.success(request, 'Contributor deleted successfully!')
        return redirect('taskassignment:contributor_list')
    return render(request, 'taskassignment/contributor_confirm_delete.html', {'contributor': contributor})

# ==================== TASK VIEWS ====================

def task_list(request):
    """List all tasks with filtering options and pagination"""
    tasks_list = Task.objects.all().order_by('-start')
    
    # Filter by completion status
    status_filter = request.GET.get('status')
    if status_filter == 'completed':
        tasks_list = tasks_list.filter(is_completed=True)
    elif status_filter == 'pending':
        tasks_list = tasks_list.filter(is_completed=False)
    
    # Filter by contributor
    contributor_filter = request.GET.get('contributor')
    if contributor_filter:
        tasks_list = tasks_list.filter(contributor_id=contributor_filter)
    
    # Get page size from request, default to 10
    page_size = request.GET.get('page_size', '10')
    try:
        page_size = int(page_size)
        if page_size not in [5, 10, 20, 50]:
            page_size = 10
    except (ValueError, TypeError):
        page_size = 10
    
    # Pagination
    paginator = Paginator(tasks_list, page_size)
    page_number = request.GET.get('page')
    tasks = paginator.get_page(page_number)
    
    contributors = Contributor.objects.all()
    return render(request, 'taskassignment/task_list.html', {
        'tasks': tasks,
        'contributors': contributors,
        'status_filter': status_filter,
        'contributor_filter': contributor_filter,
        'page_size': page_size,
        'page_sizes': [5, 10, 20, 50]
    })

def task_detail(request, pk):
    """View details of a specific task"""
    task = get_object_or_404(Task, pk=pk)
    return render(request, 'taskassignment/task_detail.html', {'task': task})

def task_create(request):
    """Create a new task"""
    if request.method == 'POST':
        form = TaskForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Task created successfully!')
            return redirect('taskassignment:task_list')
    else:
        form = TaskForm()
    return render(request, 'taskassignment/task_form.html', {'form': form, 'title': 'Create Task'})

def task_update(request, pk):
    """Update an existing task"""
    task = get_object_or_404(Task, pk=pk)
    if request.method == 'POST':
        form = TaskForm(request.POST, instance=task)
        if form.is_valid():
            form.save()
            messages.success(request, 'Task updated successfully!')
            return redirect('taskassignment:task_detail', pk=pk)
    else:
        form = TaskForm(instance=task)
    return render(request, 'taskassignment/task_form.html', {
        'form': form,
        'title': 'Update Task',
        'task': task
    })

def task_delete(request, pk):
    """Delete a task"""
    task = get_object_or_404(Task, pk=pk)
    if request.method == 'POST':
        task.delete()
        messages.success(request, 'Task deleted successfully!')
        return redirect('taskassignment:task_list')
    return render(request, 'taskassignment/task_confirm_delete.html', {'task': task})

def task_toggle_complete(request, pk):
    """Toggle task completion status"""
    task = get_object_or_404(Task, pk=pk)
    task.is_completed = not task.is_completed
    task.save()
    
    if request.headers.get('Accept') == 'application/json':
        return JsonResponse({
            'success': True,
            'is_completed': task.is_completed
        })
    
    messages.success(request, f'Task marked as {"completed" if task.is_completed else "pending"}!')
    return redirect('taskassignment:task_detail', pk=pk)

# ==================== DASHBOARD VIEWS ====================

def dashboard(request):
    """Main dashboard with statistics"""
    total_tasks = Task.objects.count()
    completed_tasks = Task.objects.filter(is_completed=True).count()
    pending_tasks = total_tasks - completed_tasks
    total_contributors = Contributor.objects.count()
    
    # Recent tasks
    recent_tasks = Task.objects.all().order_by('-start')[:5]
    
    # Tasks by contributor
    tasks_by_contributor = []
    for contributor in Contributor.objects.all():
        task_count = Task.objects.filter(contributor=contributor).count()
        if task_count > 0:
            tasks_by_contributor.append({
                'contributor': contributor,
                'task_count': task_count
            })
    
    context = {
        'total_tasks': total_tasks,
        'completed_tasks': completed_tasks,
        'pending_tasks': pending_tasks,
        'total_contributors': total_contributors,
        'recent_tasks': recent_tasks,
        'tasks_by_contributor': tasks_by_contributor
    }
    
    return render(request, 'taskassignment/dashboard.html', context)