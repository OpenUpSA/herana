from django.contrib.auth.models import User
from django import forms

from models import ProjectDetail

class ProjectDetailForm(forms.ModelForm):
    class Meta:
        model = ProjectDetail
        exclude = ('status', 'reporting_period')

