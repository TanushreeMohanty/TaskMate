from django import forms
from .models import Task

class TaskForm(forms.ModelForm):
    due_date = forms.DateField(widget=forms.SelectDateWidget, required=False)

    class Meta:
        model = Task
        fields = ['title', 'description', 'category', 'priority', 'due_date', 'completed']
