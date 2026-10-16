from datetime import timedelta
from django.contrib.auth import get_user_model
from django.core.management import call_command
from django.db import IntegrityError
from django.test import TestCase
from django.urls import reverse
from django.utils import timezone
from .models import Day, JournalEntry, Project, Section, Task, Week
from .services import get_learning_streak, get_overall_progress

class BaseData(TestCase):
    def setUp(self):
        self.section = Section.objects.create(title="Foundations", description="", order=1)
        self.week = Week.objects.create(section=self.section, number=1, title="Prompts", objective="Learn prompts")
        self.day = Day.objects.create(week=self.week, day_number=1, title="Basics", date=timezone.localdate())

class ModelAndProgressTests(BaseData):
    def test_relationships_status_and_uniqueness(self):
        task = Task.objects.create(day=self.day, title="Practice", order=1)
        project = Project.objects.create(title="P", description="", status=Project.Status.NOT_STARTED)
        self.assertEqual(task.day.week.section, self.section)
        self.assertEqual(project.status, "not_started")
        JournalEntry.objects.create(date=timezone.localdate())
        with self.assertRaises(IntegrityError): JournalEntry.objects.create(date=timezone.localdate())
    def test_progress_and_zero_task(self):
        self.assertEqual(self.day.progress, 0)
        Task.objects.create(day=self.day, title="One", completed=True, order=1)
        Task.objects.create(day=self.day, title="Two", order=2)
        self.assertEqual(self.day.progress, 50)
        self.assertEqual(self.week.progress, 50)
        self.assertEqual(self.section.progress, 50)
        self.assertEqual(get_overall_progress(), 50)

class StreakTests(BaseData):
    def test_consecutive_streak_and_same_day_tasks(self):
        today = timezone.localdate()
        for offset in (0, 1):
            day = Day.objects.create(week=self.week, day_number=offset + 2, title="Day", date=today - timedelta(days=offset))
            Task.objects.create(day=day, title="Done", order=1, completed=True)
            Task.objects.create(day=day, title="Also done", order=2, completed=True)
        self.assertEqual(get_learning_streak(today), 2)
    def test_missing_day_and_no_completion(self):
        self.assertEqual(get_learning_streak(), 0)
        Task.objects.create(day=self.day, title="Done", order=1, completed=True)
        self.assertEqual(get_learning_streak(), 1)

class ViewTests(BaseData):
    def setUp(self):
        super().setUp()
        self.user = get_user_model().objects.create_user("learner", password="pass12345")
        self.task = Task.objects.create(day=self.day, title="Practice", order=1)
    def test_protected_pages_and_views(self):
        self.assertEqual(self.client.get(reverse("dashboard")).status_code, 302)
        self.client.login(username="learner", password="pass12345")
        for name, kwargs in [("dashboard", {}), ("today", {}), ("roadmap", {}), ("week_detail", {"week_number": 1}), ("projects", {}), ("journal", {})]:
            self.assertEqual(self.client.get(reverse(name, kwargs=kwargs)).status_code, 200)
    def test_task_toggle(self):
        self.client.login(username="learner", password="pass12345")
        response = self.client.post(reverse("toggle_task", args=[self.task.pk]))
        self.assertRedirects(response, reverse("today"))
        self.task.refresh_from_db(); self.assertTrue(self.task.completed)

class SeedTests(TestCase):
    def test_seed_creates_expected_roadmap(self):
        call_command("seed_roadmap", start_date="2026-01-01")
        self.assertEqual(Week.objects.count(), 40)
        self.assertEqual(Day.objects.count(), 280)
        self.assertEqual(Project.objects.count(), 3)
        self.assertTrue(all(week.days.count() == 7 for week in Week.objects.all()))

    def test_seed_matches_phase_based_curriculum(self):
        call_command("seed_roadmap", start_date="2026-01-01")
        titles = [section.title for section in Section.objects.order_by("order").all()]
        self.assertIn("Phase 1 — Prompt Engineering", titles)
        self.assertIn("Phase 2 — Machine Learning + Mathematics", titles)
        self.assertIn("Phase 6 — AI Agents", titles)
        self.assertTrue(Week.objects.filter(number=1, title__icontains="LLM basics").exists())
