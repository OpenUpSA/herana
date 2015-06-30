from django.contrib.auth.models import User
from django import forms

from models import ProjectDetail

class ProjectDetailForm(forms.ModelForm):
    class Meta:
        model = ProjectDetail
        exclude = ('status', 'reporting_period')

    def _clean_fields(self):
        # If we are saving a draft, only the header field is required.
        if self.data['_draft']:
            for name, field in self.fields.items():
                if not name == 'header':
                    field.required = False
        super(ProjectDetailForm, self)._clean_fields()
