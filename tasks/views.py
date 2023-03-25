from django.shortcuts import render, redirect, get_object_or_404, HttpResponse
from django.views import generic
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.models import User
from django.db import IntegrityError
from django.utils import timezone
from django.contrib.auth.decorators import login_required
from .models import Task
from .forms import TaskForm

# Global Variables
app_title = _("Home")
home_view = _("Inicio")
home_title = _("Proyecto en Django")
port_title = _("Portafolio")


class HomeView(generic.TemplateView):
    template_name = "home.html"

    def get_context_data(self, **kwargs):
        context = super(HomeView, self).get_context_data(**kwargs)
        context["app_title"] = app_title
        context["title_view"] = home_view
        context["image_url"] = "assets/imgs/profile.png"
        context["aside_image_url"] = "assets/imgs/wood_light.png"
        return context


class PortfolioView(generic.TemplateView):
    template_name = "portfolio.html"
    template_url = "/portfolio"

    def get_context_data(self, **kwargs):
        context = super(PortfolioView, self).get_context_data(**kwargs)
        context["app_title"] = port_title
        context["title_view"] = home_view
        context["image_url"] = "assets/imgs/avatar_.png"
        context["aside_image_url"] = "assets/imgs/wood_light.png"
        return context


def signup(request):
        if request.method == 'GET':
            return render(request, 'register.html', {
                'form': UserCreationForm,
                'image_url':'assets/imgs/bg-4.jpg'
                
            })
        else:
            if request.POST["password1"] == request.POST["password2"]:
                try:
                    user = User.objects.create_user(
                        username=request.POST['username'], password=request.POST['password1']
                    )
                    user.save()
                    login(request, user)
                    return redirect('login')
                except IntegrityError:
                    return render(request, 'register.html', {
                        'form': UserCreationForm,
                        'image_url':'assets/imgs/bg-4.jpg', 
                        'error': 'Username Already Exists'
                    })
            return render(request, 'register.html', {
                'form': UserCreationForm,
                    'image_url':'assets/imgs/bg-4.jpg', 
                'error': 'Passwords do not match'
            })


def signin(request):
        
        if request.method == 'GET':
            return render(request, 'login.html', {
                'form': AuthenticationForm,
                'image_url':'assets/imgs/bg-4.jpg'
            })
        else:
            user = authenticate(
                request, username=request.POST['username'], password=request.POST['password']
            )
            if user is None:
                return render(request, 'login.html', {
                    'form': AuthenticationForm,
                    'image_url':'assets/imgs/bg-4.jpg',
                    'error': 'Username or Password Incorrect'})

            login(request, user)
            return redirect('tasks')


@login_required
def signout(request):
    logout(request)
    return redirect('home_page')


@login_required
def tasks(request):
    tasks = Task.objects.filter(user=request.user, datecompleted__isnull=True)
    return render(request, 'tasks.html', {
        'tasks': tasks
    })

@login_required
def completed_task(request):
    task = Task.objects.filter(user=request.user, datecompleted__isnull=False).order_by('-datecompleted')
    return render(request, 'task_complete.html',{
        'task': task
    })
    
    
@login_required
def create_task(request):
    if request.method == 'GET':
        return render(request, 'create_task.html', {
            'form': TaskForm
        })
    else:
        try:
            form = TaskForm(request.POST)
            new_task = form.save(commit=False)
            new_task.user = request.user
            new_task.save()
            return redirect('tasks')
        except ValueError:
            return render(request, 'create_task.html', {
                'form': TaskForm,
                'error': 'Error Creating Task'
            })


@login_required
def task_detail(request, task_id):
    if request.method == 'GET':
        task = get_object_or_404(Task, pk=task_id, user=request.user)
        form = TaskForm(instance=task)
        return render(request, 'task_detail.html', {
            'task': task,
            'form': form,
            })
    else:
        try:
            # Obtiene la tarea
            task = get_object_or_404(Task, pk=task_id, user=request.user)
            # recibe los datos del taskform el cual es los input
            # el cual se puede modificar y genera nuevo formulario
            form = TaskForm(request.POST, instance=task)
            # se guarda el nuevo formulario
            form.save()
            return redirect('tasks')
        except ValueError:
            return render(request, 'task_detail.html', {
            'task': task,
            'form': form,
            'error': 'Error Updating Task'
            })


@login_required
def complete_task(request, task_id):
    #buscar tarea que pertenezca al usuario correspondiente
     task = get_object_or_404(Task, pk=task_id, user=request.user)
     if request.method == 'POST':
         #marca o completa el campo datecomplete del modelo con la hora y fecha actual
         task.datecompleted = timezone.now()
         #se guarda la info
         task.save()
         return redirect('tasks')






@login_required
def delete_task(request, task_id):
    task = get_object_or_404(Task, pk=task_id, user=request.user)
    if request.method == 'POST':
        task.delete()
        return redirect('tasks')


