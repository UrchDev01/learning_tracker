from datetime import date
from django.contrib.auth import views as auth_views
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseNotAllowed
from django.shortcuts import get_object_or_404, redirect, render
from django.utils import timezone
from .forms import JournalEntryForm, ProjectForm
from .models import JournalEntry, Project, ProjectTask, Section, Task, Week
from .services import get_current_day, get_current_project, get_current_week, get_learning_streak, get_overall_progress

class LoginView(auth_views.LoginView):
    template_name = "registration/login.html"

@login_required
def dashboard(request):
    current_day = get_current_day()
    return render(request, "learning/dashboard_improved.html", {"current_day": current_day, "current_week": current_day.week if current_day else None, "today_tasks": current_day.tasks.all() if current_day else Task.objects.none(), "overall_progress": get_overall_progress(), "current_project": get_current_project(), "streak": get_learning_streak()})

@login_required
def roadmap(request):
    sections = Section.objects.prefetch_related("weeks__days__tasks")
    return render(request, "learning/roadmap.html", {"sections": sections, "overall_progress": get_overall_progress()})

@login_required
def week_detail(request, week_number):
    week = get_object_or_404(Week.objects.select_related("section").prefetch_related("days__tasks"), number=week_number)
    return render(request, "learning/week_detail.html", {"week": week})

@login_required
def today(request):
    current_day = get_current_day()
    return render(request, "learning/today.html", {"today": timezone.localdate(), "current_day": current_day, "current_week": current_day.week if current_day else None, "today_tasks": current_day.tasks.all() if current_day else Task.objects.none(), "today_progress": current_day.progress if current_day else 0})

@login_required
def toggle_task(request, task_id):
    if request.method != "POST": return HttpResponseNotAllowed(["POST"])
    task = get_object_or_404(Task, pk=task_id)
    task.completed = not task.completed
    task.completed_at = timezone.now() if task.completed else None
    task.save(update_fields=["completed", "completed_at"])
    return redirect(request.POST.get("next") or "today")

@login_required
def toggle_project_task(request, task_id):
    if request.method != "POST": return HttpResponseNotAllowed(["POST"])
    task = get_object_or_404(ProjectTask, pk=task_id)
    task.completed = not task.completed
    task.save(update_fields=["completed"])
    return redirect("project_detail", pk=task.project_id)

@login_required
def projects(request):
    return render(request, "learning/projects.html", {"projects": Project.objects.prefetch_related("tasks")})

@login_required
def project_detail(request, pk):
    return render(request, "learning/project_detail.html", {"project": get_object_or_404(Project.objects.prefetch_related("tasks"), pk=pk)})

@login_required
def project_form(request, pk=None):
    project = get_object_or_404(Project, pk=pk) if pk else None
    form = ProjectForm(request.POST or None, instance=project)
    if request.method == "POST" and form.is_valid():
        project = form.save()
        return redirect("project_detail", pk=project.pk)
    return render(request, "learning/form.html", {"form": form, "title": "Edit project" if project else "New project"})

@login_required
def journal(request):
    return render(request, "learning/journal.html", {"entries": JournalEntry.objects.all()})

@login_required
def journal_detail(request, date):
    return render(request, "learning/journal_detail.html", {"entry": get_object_or_404(JournalEntry, date=date)})

@login_required
def journal_form(request, date=None):
    entry = get_object_or_404(JournalEntry, date=date) if date else None
    form = JournalEntryForm(request.POST or None, instance=entry, initial={"date": timezone.localdate()} if not entry else None)
    if request.method == "POST" and form.is_valid():
        entry = form.save()
        return redirect("journal_detail", date=entry.date.isoformat())
    return render(request, "learning/form.html", {"form": form, "title": "Edit journal entry" if entry else "New journal entry"})
