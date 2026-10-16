from django import forms
from .models import JournalEntry, Project, ProjectTask

class ProjectForm(forms.ModelForm):
    class Meta: model = Project; fields = ["title", "description", "status"]
class ProjectTaskForm(forms.ModelForm):
    class Meta: model = ProjectTask; fields = ["title", "description", "completed", "order"]
class JournalEntryForm(forms.ModelForm):
    class Meta:
        model = JournalEntry
        fields = ["date", "learned", "built", "confused", "tomorrow"]
        labels = {"learned": "What I learned", "built": "What I built", "confused": "What confused me / problems and failures", "tomorrow": "What I’ll do tomorrow"}
        widgets = {"learned": forms.Textarea(attrs={"placeholder": "Concepts, insights, or references worth keeping…"}), "built": forms.Textarea(attrs={"placeholder": "What did you implement, test, or ship?"}), "confused": forms.Textarea(attrs={"placeholder": "Questions, setbacks, and failure cases…"}), "tomorrow": forms.Textarea(attrs={"placeholder": "The next concrete step…"})}
