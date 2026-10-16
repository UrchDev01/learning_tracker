from django.db import models


class ProgressMixin:
    def progress_from_tasks(self):
        tasks = self._task_queryset()
        total = tasks.count()
        return round(tasks.filter(completed=True).count() * 100 / total) if total else 0


class Section(ProgressMixin, models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    order = models.PositiveIntegerField(unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    class Meta: ordering = ["order"]
    def __str__(self): return self.title
    def _task_queryset(self): return Task.objects.filter(day__week__section=self)
    @property
    def progress(self): return self.progress_from_tasks()


class Week(ProgressMixin, models.Model):
    section = models.ForeignKey(Section, on_delete=models.CASCADE, related_name="weeks")
    number = models.PositiveIntegerField(unique=True)
    title = models.CharField(max_length=200)
    objective = models.TextField()
    completed = models.BooleanField(default=False)
    class Meta: ordering = ["number"]
    def __str__(self): return f"Week {self.number}: {self.title}"
    def _task_queryset(self): return Task.objects.filter(day__week=self)
    @property
    def progress(self): return self.progress_from_tasks()


class Day(ProgressMixin, models.Model):
    week = models.ForeignKey(Week, on_delete=models.CASCADE, related_name="days")
    day_number = models.PositiveSmallIntegerField()
    title = models.CharField(max_length=200)
    date = models.DateField(null=True, blank=True, db_index=True)
    class Meta:
        ordering = ["day_number"]
        constraints = [models.UniqueConstraint(fields=["week", "day_number"], name="unique_day_per_week")]
    def __str__(self): return f"{self.week} — Day {self.day_number}: {self.title}"
    def _task_queryset(self): return self.tasks.all()
    @property
    def progress(self): return self.progress_from_tasks()


class Task(models.Model):
    day = models.ForeignKey(Day, on_delete=models.CASCADE, related_name="tasks")
    title = models.CharField(max_length=300)
    description = models.TextField(blank=True)
    completed = models.BooleanField(default=False)
    order = models.PositiveIntegerField(default=0)
    completed_at = models.DateTimeField(null=True, blank=True)
    class Meta:
        ordering = ["order", "id"]
        constraints = [models.UniqueConstraint(fields=["day", "order"], name="unique_task_order_per_day")]
    def __str__(self): return self.title


class Project(models.Model):
    class Status(models.TextChoices):
        NOT_STARTED = "not_started", "Not started"
        IN_PROGRESS = "in_progress", "In progress"
        COMPLETED = "completed", "Completed"
    title = models.CharField(max_length=200)
    description = models.TextField()
    status = models.CharField(max_length=30, choices=Status.choices, default=Status.NOT_STARTED, db_index=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    class Meta: ordering = ["status", "title"]
    def __str__(self): return self.title
    @property
    def progress(self):
        total = self.tasks.count()
        return round(self.tasks.filter(completed=True).count() * 100 / total) if total else 0


class ProjectTask(models.Model):
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name="tasks")
    title = models.CharField(max_length=300)
    description = models.TextField(blank=True)
    completed = models.BooleanField(default=False)
    order = models.PositiveIntegerField(default=0)
    class Meta:
        ordering = ["order", "id"]
        constraints = [models.UniqueConstraint(fields=["project", "order"], name="unique_project_task_order")]
    def __str__(self): return self.title


class JournalEntry(models.Model):
    date = models.DateField(unique=True)
    learned = models.TextField(blank=True)
    built = models.TextField(blank=True)
    confused = models.TextField(blank=True)
    tomorrow = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    class Meta: ordering = ["-date"]
    def __str__(self): return self.date.isoformat()
