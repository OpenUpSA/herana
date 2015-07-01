from django.utils.translation import ugettext_lazy as _

YESNO = (
    ('Y', _('Yes')),
    ('N', _('No')),
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
    (2, _('More than one author'))
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
)

CAPTURE_LABELS = {
    'name': _(
        'Please select the engagement project for which you wish to capture the details.'),
    'is_leader': _('Are you the designated leader of this engagement project?'),
    'is_flagship': _('Do you consider this to be your flagship engagement project?'),
    'project_status': _(
        'Project status'),
    'start_date': _(
        'Start date'),
    'end_date': _(
        'End date'),
    'faculty': (
        'In which faculty/school is the project located?'),
    'multi_faculty': _(
        'Does the project span multiple faculties/schools?'),
    'description': _(
        'Please provide a short description of the project.'),
    'focus_area': _(
        'In which of the following areas would you place your project?'),
    'focus_area_text': _(
        'If other was chosen above, please describe.'),
    'classification': _(
        'How would you classify this flagship engagement activity?'),
    'strategic_objectives': _(
        'What are the 4 main strategic objectives of the project?'),
    'outcomes': _(
        'What are the planned outcomes of the project?'),
    'beneficiaries': _(
        'Who are the intended beneficiaries of the project?'),
    'initiation': _(
        'Which one of the following statements best describes how the project was initiated?'),
    'authors': _(
        'How many authors were involved in the writing of the project proposal/plan?'),
    'amendments_permitted': _(
        'To the best of your knowledge, are deviations or amendments to the request for proposal permitted by the funder?'),
    'public_domain': _(
        'Will the written up findings or data or other outputs of the project be available electronically in the public domain?'),
    'public_domain_url': _(
        'URL'),
    'adv_group': _(
        'Does the project have an advisory group?'),
    'adv_group_rep': _(
        'If yes, are any of the following members of the advisory group?'),
    'adv_group_freq': _(
        'How often does the advisory group meet?'),
    'team_members': _(
        'Are any of the following members of the research team?'),
    'new_initiative': _(
        'Will any of the findings/results/outcomes of the project be used to implement or develop new products/services/interventions/policies?'),
    'new_initiative_text': _(
        'If yes, please describe'),
    'new_initiative_party': _(
        'Who will implement or develop these new products/services/interventions/policies?'),
    'new_initiative_party_text': _(
        'Please provide the name of the third party or describe how the product / service / intervention / policy will be developed and/or implemented'),
    'funding': _(
        'Please list sources of project funding, the number of years for which funding has been secured, and the amount of funding (in US$)'),
    'research': _(
        'In terms of the research done for the project (if applicable), which statement best describes the project'),
    'research_text': _(
        'Please describe'),
    'phd_research': _(
        'Is a student\'s PhD research linked to this project?'),
    'phd_research_name': _(
        'If yes, please provide their names'),
    'outputs': _(
        'Please list the completed publications and other outputs for this project'),
    'curriculum_changes': _(
        'Has the project lead to any contributions or changes to the curriculum?'),
    'curriculum_changes_text': _(
        'If yes, please describe the types of changes made to the curriculum as a result of the project'),
    'new_courses': _(
        'Have any new courses/modules/programmes been introduced as a result of this project?'),
    'new_course_detail': _(
        'If yes, please describe'),
    'students_involved': _(
        'Are students involved in the project?'),
    'student_types': _(
        'If yes, please indicate types of students participating'),
    'student_nature': _(
        'What is the nature of student participation in the project?'),
    'student_nature_text': _(
        'If other was selected, please describe.'),
    'course_requirement': _(
        'Is participation in the project a requirement for the completion of an existing course/degree offered by the university?'),
    'course_req_detail': _(
        'If yes, please describe'),
    'external_collaboration': _(
        'Did you collaborate with academics from other universities on the project?'),
    'collaboration_detail': _(
        'If yes, please describe'),
    'record_status': _(
        'Record status'),
    'reporting_period': _(
        'Period in which the record was captured.'),
}

CAPTURE_HELP = {
    'focus_areas': _(
        '''Select ALL applicable<br>'''),
    'strategic_objectives': (
        '''Only select 4 options. <br>'''),
    'research_text': _(
        '''If <b>1, 2 or 3</b> selected, please provide a short description of the data collected or the original research conducted <br> If <b>4 or 5</b> selected, please explain why it was not necessary to collect new data or conduct original research''')
}
