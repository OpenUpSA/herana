from django.utils.translation import ugettext_lazy as _

YESNO = (
    ('Y', _('Yes')),
    ('N', _('No')),
)

FOCUS_AREAS = (
    (1, _('Teaching and learning')),
    (2, _('Research')),
    (3, _('Service (Professional Discipline-Based)')),
    (4, _('Other'))
)

CLASSIFICATION = (
    (1, _('Project')),
    (2, _('Programme')),
    (3, _('Service')),
    (4, _('Other'))
)

INITIATION_STATEMENTS = (
    (1, _('Approached or invited by funder, company, NGO, government, research institute or by another university to submit a proposal for the project')),
    (2, _('Informed by the university research or contracts office about the reach project')),
    (3, _('Initiated by colleagues at own university')),
    (4, _('Initiated by project leader')),
    (5, _('Initiated by project leader in collaboration with colleagues')),
    (6, _('Follow-on or continuation from existing project')),
    (7, _('Project assigned to project leader')),
)

NUMBER_AUTHORS = (
    (1, _('One author')),
    (1, _('More than one author'))
)

ADV_GROUP_FREQ = (
    (1, _('Monthly')),
    (2, _('Quarterly')),
    (3, _('Annually')),
    (4, _('Ad hoc'))
)

INITIATIVE_PARTIES = (
    (1, _('A third party has been contracted to develop the product / service / intervention / policy')),
    (2, _('The project team will develop the product / service / intervention / policy')),
    (3, _('Other')),
)

RESEARCH_CLASSIFICATION = (
    (1, _('The project conducted original research')),
    (2, _('The project collected new data and conducted original research to complete the project')),
    (3, _('The project collected new data and applied existing knowledge to the data collected to complete the project')),
    (4, _('No new data was required and existing knowledge was applied to complete the project')),
    (5, _('Not applicable'))
)

PROJECT_STATUS = (
    (1, _('Complete')),
    (2, _('Ongoing'))
)

RECORD_STATUS = (
    (1, 'Draft'),
    (2, 'Final'),
    (3, 'Rejected')
)

CAPTURE_LABELS = {
    'header': _('Name of flagship engagement project'),
    'project_status': _(),
    'start_date': _(),
    'end_date': _(),
    'faculty': (' In which faculty/school is the project located?'),
    'multi_faculty': _('Does the project span multiple faculties/schools?'),
    'description': _('Please provide a short description of the project.'),
    'focus_area': _('In which of the following areas would you place your project?'),
    'focus_area_text': _('If other was chosen above, please describe.'),
    'classification': _('How would you classify this flagship engagement activity?'),
    'strategic_objectives': _('What are the 4 main strategic objectives of the project?'),
    'outcomes': _(),
    'beneficiaries': _(),
    'initiation': _(),
    'authors': _(),
    'amendments_permitted': _(),
    'public_domain': _('Will the written up findings or data or other outputs of the project be available electronically in the public domain?'),
    'public_domain_url': _('URL'),
    'adv_group': _(),
    'adv_group_rep': _(),
    'adv_group_freq': _(),
    'team_members': _(),
    'new_initiative': _(),
    'new_initiative_text': _(),
    'new_initiative_party': _(),
    'new_initiative_party_text': _(),
    'new_initiative_party_text': _(),
    'funding': _(),
    'research': _(),
    'research_text': _(),
    'phd_research': _(),
    'phd_research_name': _(),
    'outputs': _(),
    'curriculum_changes': _(),
    'curriculum_changes_text': _(),
    'new_courses': _(),
    'new_course_detail': _(),
    'students_involved': _(),
    'student_types': _(),
    'student_nature': _(),
    'student_nature_text': _(),
    'course_requirement': _(),
    'course_req_detail': _(),
    'external_collaboration': _(),
    'collaboration_detail': _(),
    'status': _(),
    'reporting_period': _(),
}

CAPTURE_HELP = {

}
