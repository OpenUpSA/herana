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
    (None, _("N/A")),
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
    (1, _('1. The project conducted original research')),
    (2, _('2. The project collected new data and conducted original research to complete the project')),
    (3, _('3. The project collected new data and applied existing knowledge to the data collected to complete the project')),
    (4, _('4. No new data was required and existing knowledge was applied to complete the project')),
    (5, _('5. Not applicable'))
)

PROJECT_STATUS = (
    (1, _('Complete')),
    (2, _('Ongoing'))
)

RECORD_STATUS = (
    (1, 'Draft'),
    (2, 'Final'),
)

PROJECT_OUTPUT_LABELS = {
    'output_title': 'Title of output (e.g. title of journal article, book chapter, presentation, performance, etc.)',
    'pub_title': 'Title of journal, book, conference, blog, periodical, event, etc.',
    'url': 'URL',
    'doi': 'DOI',
    'attachment': 'Attachment (Please provide an attachment of the output should a URL not be available. If the output is confidential, embargoed, etc., please provide a PDF of the cover page only)'
}

CAPTURE_LABELS = {
    'name': _(
        'P1.0: Please enter the name of the engagement project for which you wish to capture the details.'),
    'is_leader': _('G1: Are you the designated leader of this engagement project?'),
    'is_flagship': _('G2: Do you consider this to be your flagship engagement project?'),
    'project_status': _(
        'P2.0: Project status'),
    'start_date': _(
        'Start date'),
    'end_date': _(
        'End date'),
    'faculty': (
        'P3.0: In which faculty / school is the project located?'),
    'multi_faculty': _(
        'P3.1: Does the project span multiple faculties / schools?'),
    'description': _(
        'P4.0: Please provide a short description of the project.'),
    'focus_area': _(
        'P5.0: In which of the following areas would you place your project?'),
    'focus_area_text': _(
        'If other was chosen above, please describe.'),
    'classification': _(
        'P6.0: How would you classify this flagship engagement activity?'),
    'strategic_objectives': _(
        'A1.1: What are the 4 main strategic objectives of the project?'),
    'outcomes': _(
        'A1.2: What are the planned outcomes of the project?'),
    'beneficiaries': _(
        'A1.3: Who are the intended beneficiaries of the project?'),
    'initiation': _(
        'A2.1: Which one of the following statements best describes how the project was initiated?'),
    'authors': _(
        'A2.2: How many authors were involved in the writing of the project proposal / plan?'),
    'amendments_permitted': _(
        'A2.3: To the best of your knowledge, are deviations or amendments to the request for proposal permitted by the funder?'),
    'public_domain': _(
        'A2.4: Are the project proposal, written up findings of the project available electronically in the public domain?'),
    'public_domain_url': _(
        'URL'),
    'adv_group': _(
        'A2.6: Does the project have an advisory group?'),
    'adv_group_rep': _(
        'A2.6.1: If yes, are any of the following members of the advisory group?'),
    'adv_group_freq': _(
        'A2.7: How often does the advisory group meet?'),
    'team_members': _(
        'A3.1: Are any of the following members of the research team?'),
    'team_members_text': _(
        "If other was selected, please specify."),
    'new_initiative': _(
        'A3.2: Have any of the findings / results / outcomes of the project been used to implement or develop new products / services / interventions / policies?'),
    'new_initiative_text': _(
        'If yes, please describe'),
    'new_initiative_party': _(
        'Who implemented or developed these new products / services / interventions / policies?'),
    'new_initiative_party_text': _(
        'Please provide the name of the third party or describe how the product / service / intervention / policy was developed and / or implemented'),
    'funding': _(
        'A4.1: Please list sources of project funding, the number of years for which funding has been secured, and the amount of funding (in US$)'),
    'research': _(
        'C1.1.1: In terms of the research done for the project (if applicable), which statement best describes the project'),
    'research_text': _(
        'Please describe'),
    'phd_research': _(
        'C.1.1.2: Is a student\'s PhD research linked to this project?'),
    'phd_research_name': _(
        'If yes, please provide their names'),
    'curriculum_changes': _(
        'C3.1: Has the project lead to any contributions or changes to the curriculum?'),
    'curriculum_changes_text': _(
        'If yes, please describe the types of changes made to the curriculum as a result of the project'),
    'new_courses': _(
        'C3.2: Have any new courses / modules / programmes been introduced as a result of this project?'),
    'new_course_detail': _(
        'If yes, please describe'),
    'students_involved': _(
        'C3.3.1: Are students involved in the project?'),
    'student_types': _(
        'If yes, please indicate types of students participating'),
    'student_nature': _(
        'C3.3.2: What is the nature of student participation in the project?'),
    'student_nature_text': _(
        'If other was selected, please describe.'),
    'course_requirement': _(
        'C3.4: Is participation in the project a requirement for the completion of an existing course / degree offered by the university?'),
    'course_req_detail': _(
        'If yes, please describe'),
    'external_collaboration': _(
        'C4.4: Did you collaborate with academics from other universities on the project?'),
    'collaboration_detail': _(
        'If yes, please describe'),
    'record_status': _(
        'Record status'),
    'reporting_period': _(
        'Period in which the record was captured.'),
    'is_rejected': _(
        'Rejected'),
    'is_flagged': _(
        'Suspect'),
}

CAPTURE_HELP = {
    'focus_areas': _(
        '''Select ALL applicable<br>'''),
    'strategic_objectives': (
        '''Only select 4 options. <br>'''),
    'research_text': _(
        '''If <b>1, 2 or 3</b> selected, please provide a short description of the data collected or the original research conducted <br> If <b>4 or 5</b> selected, please explain why it was not necessary to collect new data or conduct original research''')
}
