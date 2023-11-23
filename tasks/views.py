
from django.shortcuts import render, get_object_or_404, redirect
from .models import Task
from django.contrib.auth.models import User
from django.contrib import messages
from .forms import TaskForm

def view_task(request):
    tasks = Task.objects.filter(completed =False)
    user = request.user
    merchantgroup=user.groups.all() #lists all the groups
    group_names= [group.name for group in merchantgroup] #creates a loop to check for a group name
    return render(request, 'index.html', {'tasks': tasks,'group_names':group_names})
    
def deliver_task(request,id):

    obj = Task.objects.get(id=id)
    obj.completed = True
    obj.save()
    messages.success(request, ('Order posted succesfully'))
    return redirect('tasks:task_list')

def task(request, task_id):
    task = get_object_or_404(Task, pk=task_id)
    return render(request, 'index.html', {'task': task})

def add_task(request):
    
     
    if request.method == 'POST':
        form = TaskForm(request.POST)
        if form.is_valid():
            form.save()
        return redirect('index')
    else:
        form=TaskForm()
    return render(request, 'add_task.html', { 'form':form })

# def edit_task(request, task_id):
#     task = get_object_or_404(Task, pk=task_id)
#     if request.method == 'POST':
#         task.title = request.POST['title']
#         task.description = request.POST['description']
#         task.save()
#         return


# def complete_task(request, task_id):
#     task = Task.objects.get(id=task_id)
#     task.completed = True
#     task.save()
#     return redirect('/')


# def delete_task(request, task_id):
#     task = Task.objects.get(id=task_id)
#     task.delete()
#     return redirect('/')











# def update_task(request, pk):
#     task = get_object_or_404(Task, pk=pk)
#     if request.method == 'POST':
#         form = TaskForm(request.POST, instance=task)
#         if form.is_valid():
#             form.save()
#             return render(request, 'tasks/task_updated.html')
#     else:
#         form = TaskForm(instance=