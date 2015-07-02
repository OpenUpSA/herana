from django.contrib.auth.models import User
from django import forms

from models import ProjectDetail

class ProjectDetailForm(forms.ModelForm):
    class Meta:
        model = ProjectDetail
        exclude = ('proj_leader', 'date_created', 'record_status', 'reporting_period', 'rejected', 'rejected_detail')

    def _clean_fields(self):
        # If we are saving a draft, only the header field is required.
        if '_draft' in self.data:
            for name, field in self.fields.items():
                if not name == 'name':
                    field.required = False
        super(ProjectDetailForm, self)._clean_fields()

    def clean_end_date(self):
        if self.cleaned_data['project_status'] == 1 and self.cleaned_data['end_date'] == None:
            msg = "A complete project must have an end date."
            self.add_error('end_date', msg)

    def clean_focus_area_text(self):
        for choice in self.cleaned_data['focus_area']:
            if choice.code == 4 and self.cleaned_data['focus_area_text'] == '':
                msg = "If other was chosen above, please describe."
                self.add_error('focus_area_text', msg)

    def clean_strategic_objectives(self):
        if self.cleaned_data['strategic_objectives'].exists():
            if len(self.cleaned_data['strategic_objectives']) != 4:
                msg = "Please select only 4 options."
                self.add_error('strategic_objectives', msg)

    def clean_public_domain_url(self):
        if self.cleaned_data['public_domain'] == 'Y' and self.cleaned_data['public_domain_url'] == '':
            msg = "If yes was selected above, please provide the URL."
            self.add_error('public_domain_url', msg)

    def clean_new_initiative_text(self):
        if self.cleaned_data['new_initiative'] == 'Y' and self.cleaned_data['new_initiative_text'] == '':
            msg = "If yes was selected above, please describe."
            self.add_error('new_initiative_text', msg)

    def clean_new_initiative_party_text(self):
        if self.cleaned_data['new_initiative_party'] == 1 and self.cleaned_data['new_initiative_party_text'] == '':
            msg = "Please provide the name of the third party."
            self.add_error('new_initiative_party_text', msg)
        if self.cleaned_data['new_initiative_party'] == 3 and self.cleaned_data['new_initiative_party_text'] == '':
            msg = "Please describe how the product / service / intervention / policy will be developed and/or implemented."
            self.add_error('new_initiative_party_text', msg)

    def clean_research_text(self):
        if not self.cleaned_data['research'] is None and self.cleaned_data['research_text'] == '':
            msg = "Please provide a description for your choice in the field above."
            self.add_error('research_text', msg)

    def clean_curriculum_changes_text(self):
        if self.cleaned_data['curriculum_changes'] == 'Y' and self.cleaned_data['curriculum_changes_text'] == '':
            msg = "Please describe the types of changes made to the curriculum as a result of the project."
            self.add_error('curriculum_changes_text', msg)

    def clean_student_types(self):
        if self.cleaned_data['students_involved'] == 'Y' and not self.cleaned_data['student_types'].exists():
            msg = "Please indicate the types of students involved."
            self.add_error('student_types', msg)

    def clean_student_nature_text(self):
        if self.cleaned_data['student_nature'] == 6 and self.cleaned_data['student_nature_text'] == 'Y':
            msg = "Please describe the nature of student participation."
            self.add_error('student_types', msg)


