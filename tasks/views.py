from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.db import IntegrityError
from .forms import createTaskForm
from .models import Task
from django.utils import timezone

# Create your views here.


def home(request):
    return render(request, 'home.html')


def signUp(request):
    if request.method == 'GET':
        return render(request, 'signup.html', {
            'form': UserCreationForm()
        })
    elif request.method == 'POST':
        if request.POST['password1'] == request.POST['password2']:
            # Registrar usuario
            try:
                user = User.objects.create_user(
                    username=request.POST['username'], password=request.POST['password1'])
                user.save()
                login(request, user)  # Crear cookies para un usuario logeado
                return redirect('tasks')
            except IntegrityError:
                return render(request, 'signup.html', {
                    'form': UserCreationForm(),
                    'error': 'El usuario ya existe'
                })
        else:
            return render(request, 'signup.html', {
                'form': UserCreationForm(),
                'error': 'Las contraseñas no coinciden.'
            })


@login_required
def tasks(request):

    task_list = Task.objects.filter(
        user=request.user, datecompleted__isnull=True)
    return render(request, 'tasks.html', {
        'is_in_task_view': True,
        'tasks': task_list,
    })


@login_required
def create_task(request):
    if request.method == 'GET':
        return render(request, 'create_task.html', {
            'createTaskForm': createTaskForm()
        })
    elif request.method == 'POST':
        try:
            form = createTaskForm(request.POST)
            new_task = form.save(commit=False)
            new_task.user = request.user
            new_task.save()
            return redirect('tasks')
        except ValueError:
            return render(request, 'create_task.html', {
                'createTaskForm': createTaskForm(),
                'error': 'Datos ingresados no válidos'
            })


@login_required
def task_detail(request, task_id):

    if request.method == 'GET':
        task = get_object_or_404(Task, pk=task_id, user=request.user)
        update_task_form = createTaskForm(instance=task)
        return render(request, 'task_detail.html', {
            'task': task,
            'is_in_create_view': True,
            'update_form': update_task_form,
        })
    elif request.method == 'POST':
        try:
            upd_task = get_object_or_404(Task, pk=task_id, user=request.user)
            upd_form = createTaskForm(request.POST, instance=upd_task)
            upd_form.save()
            return redirect('tasks')
        except ValueError:
            task = get_object_or_404(Task, pk=task_id, user=request.user)
            update_task_form = createTaskForm(instance=task)
            return render(request, 'task_detail.html', {
                'task': task,
                'is_in_create_view': True,
                'update_form': update_task_form,
                'error': "Error updating task"
            })


@login_required
def task_completed(request, task_id):
    compl_task = get_object_or_404(Task, pk=task_id, user=request.user)
    if request.method == 'POST':
        compl_task.datecompleted = timezone.now()
        compl_task.save()
        return redirect('tasks')


@login_required
def tasks_completed(request):

    task_list = Task.objects.filter(
        user=request.user, datecompleted__isnull=False)
    return render(request, 'tasks.html', {
        'tasks': task_list,
        'is_in_task_completed_view': True,
    })


@login_required
def task_deleted(request, task_id):
    del_task = get_object_or_404(Task, pk=task_id, user=request.user)
    if request.method == 'POST':
        del_task.delete()
        return redirect('tasks')


@login_required
def signOut(request):
    logout(request)
    return redirect('home')


def signIn(request):

    if request.method == 'GET':
        return render(request, 'signin.html', {
            "form": AuthenticationForm()
        })
    elif request.method == 'POST':
        user = authenticate(
            request, username=request.POST['username'], password=request.POST['password'])

        if user is None:
            return render(request, 'signin.html', {
                "form": AuthenticationForm(),
                'error': "Nombre de usuario o contraseña incorrectos"
            })
        else:
            login(request, user)
            return redirect('tasks')
