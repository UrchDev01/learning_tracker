from django.contrib.auth import views as auth_views
from django.urls import path
from . import views

urlpatterns = [
    path("", views.dashboard, name="dashboard"), path("dashboard/", views.dashboard, name="dashboard"),
    path("login/", views.LoginView.as_view(), name="login"), path("logout/", auth_views.LogoutView.as_view(), name="logout"),
    path("roadmap/", views.roadmap, name="roadmap"), path("roadmap/week/<int:week_number>/", views.week_detail, name="week_detail"),
    path("today/", views.today, name="today"), path("tasks/<int:task_id>/toggle/", views.toggle_task, name="toggle_task"),
    path("project-tasks/<int:task_id>/toggle/", views.toggle_project_task, name="toggle_project_task"),
    path("projects/", views.projects, name="projects"), path("projects/new/", views.project_form, name="project_new"), path("projects/<int:pk>/", views.project_detail, name="project_detail"), path("projects/<int:pk>/edit/", views.project_form, name="project_edit"),
    path("journal/", views.journal, name="journal"), path("journal/new/", views.journal_form, name="journal_new"), path("journal/<str:date>/", views.journal_detail, name="journal_detail"), path("journal/<str:date>/edit/", views.journal_form, name="journal_edit"),
]
