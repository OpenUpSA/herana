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

    def clean(self):
        cleaned_data = super(ProjectDetailForm, self).clean()

        if cleaned_data.get('project_status') == 1 and cleaned_data.get('end_date') == None:
            msg = "A complete project must have an end date."
            self.add_error('end_date', msg)

        if cleaned_data.get('end_date') and cleaned_data.get('start_date'):
            if cleaned_data.get('end_date') < cleaned_data.get('start_date'):
                msg = "The project end date cannot be before the project start date."
                self.add_error('end_date', msg)

        if cleaned_data.get('focus_area'):
            for choice in cleaned_data.get('focus_area'):
                if choice.code == 4 and self.cleaned_data.get('focus_area_text') == '':
                    msg = "If other was chosen above, please describe."
                    self.add_error('focus_area_text', msg)

        if cleaned_data.get('strategic_objectives'):
            if len(self.cleaned_data['strategic_objectives']) > 4:
                msg = "Please select only 4 options."
                self.add_error('strategic_objectives', msg)

        if cleaned_data.get('public_domain') == 'Y' and cleaned_data.get('public_domain_url') == '':
            msg = "If yes was selected above, please provide the URL."
            self.add_error('public_domain_url', msg)

        if cleaned_data.get('adv_group') == 'Y' and cleaned_data.get('adv_group_freq') is None:
            msg = "Please indicate how often the advisory group meets."
            self.add_error('adv_group_freq', msg)
        import ipdb; ipdb.set_trace()
        if cleaned_data.get('team_members')[0].code == 7 and cleaned_data.get('team_members_text') == '':
            msg = "If other was selected above, please specify."
            self.add_error('team_members_text', msg)

        if cleaned_data.get('new_initiative') == 'Y' and cleaned_data.get('new_initiative_text') == '':
            msg = "If yes was selected above, please describe."
            self.add_error('new_initiative_text', msg)

        if cleaned_data.get('new_initiative_party') == 1 and cleaned_data('new_initiative_party_text') == '':
            msg = "Please provide the name of the third party."
            self.add_error('new_initiative_party_text', msg)

        if cleaned_data.get('new_initiative_party') == 3 and cleaned_data.get('new_initiative_party_text') == '':
            msg = "Please describe how the product / service / intervention / policy will be developed and/or implemented."
            self.add_error('new_initiative_party_text', msg)

        if not cleaned_data.get('research') is None and cleaned_data.get('research_text') == '':
            msg = "Please provide a description for your choice in the field above."
            self.add_error('research_text', msg)

        if cleaned_data.get('curriculum_changes') == 'Y' and cleaned_data.get('curriculum_changes_text') == '':
            msg = "Please describe the types of changes made to the curriculum as a result of the project."
            self.add_error('curriculum_changes_text', msg)

        if cleaned_data.get('students_involved') == 'Y' and not cleaned_data.get('student_types'):
            msg = "Please indicate the types of students involved."
            self.add_error('student_types', msg)

        if cleaned_data.get('students_involved') == 'Y' and not cleaned_data.get('student_nature'):
            msg = "Please indicate the nature of the student involvement."
            self.add_error('student_nature', msg)

        if cleaned_data.get('student_nature'):
            for item in cleaned_data.get('student_nature'):
                if item.code == 6 and cleaned_data.get('student_nature_text') == '':
                    msg = "Please describe the nature of student participation."
                    self.add_error('student_nature_text', msg)
