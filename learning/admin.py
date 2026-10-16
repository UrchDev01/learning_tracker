from django.contrib import admin
from .models import Day, JournalEntry, Project, ProjectTask, Section, Task, Week

class WeekInline(admin.TabularInline): model = Week; extra = 0
class DayInline(admin.TabularInline): model = Day; extra = 0
class TaskInline(admin.TabularInline): model = Task; extra = 0
class ProjectTaskInline(admin.TabularInline): model = ProjectTask; extra = 0
@admin.register(Section)
class SectionAdmin(admin.ModelAdmin): list_display = ("order", "title"); ordering = ("order",); search_fields = ("title",); inlines = [WeekInline]
@admin.register(Week)
class WeekAdmin(admin.ModelAdmin): list_display = ("number", "title", "section", "completed"); list_filter = ("section", "completed"); ordering = ("number",); search_fields = ("title", "objective"); inlines = [DayInline]
@admin.register(Day)
class DayAdmin(admin.ModelAdmin): list_display = ("week", "day_number", "title", "date"); list_filter = ("week__section",); ordering = ("week", "day_number"); inlines = [TaskInline]
@admin.register(Task)
class TaskAdmin(admin.ModelAdmin): list_display = ("title", "day", "completed", "order"); list_filter = ("completed", "day__week__section"); search_fields = ("title", "description")
@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin): list_display = ("title", "status", "progress"); list_filter = ("status",); search_fields = ("title", "description"); inlines = [ProjectTaskInline]
@admin.register(JournalEntry)
class JournalEntryAdmin(admin.ModelAdmin): list_display = ("date", "updated_at"); ordering = ("-date",); search_fields = ("learned", "built", "confused", "tomorrow")
