from django.contrib import admin
from django.urls import path

from .views import *
from tasks import views


urlpatterns = [
    path("",HomeView.as_view(), name="home_page"),
    path("portfolio/",PortfolioView.as_view(), name="portfolio_page"),
    path("register/",views.signup, name="register"),
    path("login/",views.signin, name="login"),
    path("logout/",views.signout, name="logout"),
    path("tasks/",views.tasks, name="tasks"),
    path("tasks/complete",views.completed_task, name="completed_task"),
    path("tasks/create/",views.create_task, name="create_task"),
    path("tasks/<int:task_id>/",views.task_detail, name="task_detail"),
    path("tasks/<int:task_id>/complete",views.complete_task, name="complete_task"),
    path("tasks/<int:task_id>/delete",views.delete_task, name="delete_task"),
]
