# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations

def populate_questionnaire_options(apps, schema_editor):
    FocusArea = apps.get_model('herana', "FocusArea")
    AdvisoryGroupRep = apps.get_model('herana', "AdvisoryGroupRep")
    ResearchTeamMember = apps.get_model('herana', "ResearchTeamMember")
    ProjectOutputs = apps.get_model('herana', "ProjectOutputs")
    StudentType = apps.get_model('herana', "StudentType")
    StudentParticipationNature = apps.get_model('herana', "StudentParticipationNature")

    option_models = [
        (FocusArea, FOCUS_AREAS),
        (AdvisoryGroupRep, ADVISORY_GROUP_REP),
        (ResearchTeamMember, RESEARCH_TEAM_MEMEBRS),
        (ProjectOutputs, PROJECT_OUTPUTS),
        (StudentType, STUDENT_TYPES),
        (StudentParticipationNature, STUDENT_PARTICIPATION_NATURE)
    ]

    for model, options in option_models:
        for code, choice in options:
            obj = model(code=code, choice=choice)
            obj.save()

def backwards(apps, schema_editor):
    FocusArea = apps.get_model('herana', "FocusArea")
    AdvisoryGroupRep = apps.get_model('herana', "AdvisoryGroupRep")
    ResearchTeamMember = apps.get_model('herana', "ResearchTeamMember")
    ProjectOutputs = apps.get_model('herana', "ProjectOutputs")
    StudentType = apps.get_model('herana', "StudentType")
    StudentParticipationNature = apps.get_model('herana', "StudentParticipationNature")


    option_models = [
        FocusArea,
        AdvisoryGroupRep,
        ResearchTeamMember,
        ProjectOutputs,
        StudentType,
        StudentParticipationNature
    ]

    for model in option_models:
        qs = model.objects.all()
        for item in qs:
            item.delete()

class Migration(migrations.Migration):

    dependencies = [
        ('herana', '0001_initial'),
    ]

    operations = [
        migrations.RunPython(
                populate_questionnaire_options,
                backwards
            ),
    ]

FOCUS_AREAS = [
    (1, 'Teaching and learning'),
    (2, 'Research'),
    (3, 'Service (Professional Discipline-Based)'),
    (4, 'Other')
]

ADVISORY_GROUP_REP = [
    (1, 'Representatives from government or government agencies'),
    (2, 'Representatives from non-governmental organisations (NGOs)/civil society organisations (CSOs)'),
    (3, 'Representatives from the community'),
    (4, 'Representatives from business/industry'),
    (5, 'Independent representatives'),
    (6, 'Representatives from the project funders'),
]

RESEARCH_TEAM_MEMEBRS = [
    (1, 'Researchers from government or government agencies (e.g. from one of the science councils)'),
    (2, 'Researchers from NGOs/CSOs'),
    (3, 'Researchers from business/industry (e.g. private research institutes)'),
    (4, 'Researchers representing the community'),
    (5, 'Independent researchers/consultants'),
    (6, 'Researchers representing the research project’s funders'),
    (7, 'Other (Please specify)')
]

PROJECT_OUTPUTS = [
    (1, 'Journal article'),
    (2, 'Conference proceedings'),
    (3, 'Chapter in a book'),
    (4, 'Book: peer reviewed edited collection or monograph'),
    (5, 'Book: other (e.g. textbook, non-academic book, etc.)'),
    (6, 'Findings be published in a professional or trade journal/periodical/magazine'),
    (7, 'Online article or blog post'),
    (8, 'Exhibitions, performances or presentations'),
    (9, 'Findings be presented at an academic conference'),
    (10, 'Findings be presented at another forum'),
    (11, 'Other outputs not captured above'),
]

STUDENT_TYPES = [
    (1, 'Undergraduates'),
    (2, 'Masters'),
    (3, 'PhDs'),
]

STUDENT_PARTICIPATION_NATURE = [
    (1, 'Workplace placement (e.g. internships, job shadowing, etc.)'),
    (2, 'Volunteering'),
    (3, 'Presenting or offering courses, workshops or programmes'),
    (4, 'Research (data collection, conducting interviews, etc.)'),
    (5, 'Providing administrative support to the project'),
    (6, 'Other (Please specify)'),
]
