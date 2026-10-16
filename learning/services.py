from datetime import timedelta
from django.db.models import Q
from django.utils import timezone
from .models import Day, Project, Task

def get_current_day(today=None):
    today = today or timezone.localdate()
    exact = Day.objects.select_related("week__section").filter(date=today).first()
    if exact:
        return exact
    return Day.objects.select_related("week__section").filter(date__lte=today).order_by("-date").first() or Day.objects.select_related("week__section").filter(date__isnull=False).order_by("date").first()

def get_current_week(today=None):
    day = get_current_day(today)
    return day.week if day else None

def get_overall_progress():
    total = Task.objects.count()
    return round(Task.objects.filter(completed=True).count() * 100 / total) if total else 0

def get_current_project():
    return Project.objects.filter(status=Project.Status.IN_PROGRESS).order_by("updated_at").first() or Project.objects.exclude(status=Project.Status.COMPLETED).order_by("created_at").first()

def get_learning_streak(today=None):
    cursor = today or timezone.localdate()
    completed_dates = set(Task.objects.filter(completed=True, day__date__isnull=False).values_list("day__date", flat=True))
    streak = 0
    while cursor in completed_dates:
        streak += 1
        cursor -= timedelta(days=1)
    return streak
