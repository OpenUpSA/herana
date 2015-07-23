# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('herana', '0002_populate_questionnaire_options'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='customuser',
            options={'verbose_name': 'User'},
        ),
        migrations.AddField(
            model_name='projectdetail',
            name='team_members_text',
            field=models.TextField(null=True, verbose_name='If other was selected, please describe.', blank=True),
        ),
        migrations.AlterField(
            model_name='projectdetail',
            name='adv_group',
            field=models.CharField(max_length=1, null=True, verbose_name='A2.6: Does the project have an advisory group?', choices=[(b'Y', 'Yes'), (b'N', 'No')]),
        ),
        migrations.AlterField(
            model_name='projectdetail',
            name='adv_group_freq',
            field=models.PositiveIntegerField(default=None, null=True, verbose_name='A2.7: How often does the advisory group meet?', blank=True, choices=[(None, 'N/A'), (1, 'Monthly'), (2, 'Quarterly'), (3, 'Annually'), (4, 'Ad hoc')]),
        ),
        migrations.AlterField(
            model_name='projectdetail',
            name='adv_group_rep',
            field=models.ManyToManyField(to='herana.AdvisoryGroupRep', verbose_name='A2.6.1: If yes, are any of the following members of the advisory group?', blank=True),
        ),
        migrations.AlterField(
            model_name='projectdetail',
            name='amendments_permitted',
            field=models.CharField(max_length=1, null=True, verbose_name='A2.3: To the best of your knowledge, are deviations or amendments to the request for proposal permitted by the funder?', choices=[(b'Y', 'Yes'), (b'N', 'No')]),
        ),
        migrations.AlterField(
            model_name='projectdetail',
            name='authors',
            field=models.PositiveIntegerField(null=True, verbose_name='A2.2: How many authors were involved in the writing of the project proposal / plan?', choices=[(1, 'One author'), (2, 'More than one author')]),
        ),
        migrations.AlterField(
            model_name='projectdetail',
            name='beneficiaries',
            field=models.TextField(null=True, verbose_name='A1.3: Who are the intended beneficiaries of the project?'),
        ),
        migrations.AlterField(
            model_name='projectdetail',
            name='classification',
            field=models.PositiveIntegerField(null=True, verbose_name='P6.0: How would you classify this flagship engagement activity?', choices=[(1, 'Project'), (2, 'Programme'), (3, 'Service'), (4, 'Other')]),
        ),
        migrations.AlterField(
            model_name='projectdetail',
            name='course_requirement',
            field=models.CharField(max_length=1, null=True, verbose_name='C3.4: Is participation in the project a requirement for the completion of an existing course / degree offered by the university?', choices=[(b'Y', 'Yes'), (b'N', 'No')]),
        ),
        migrations.AlterField(
            model_name='projectdetail',
            name='curriculum_changes',
            field=models.CharField(max_length=1, null=True, verbose_name='C3.1: Has the project lead to any contributions or changes to the curriculum?', choices=[(b'Y', 'Yes'), (b'N', 'No')]),
        ),
        migrations.AlterField(
            model_name='projectdetail',
            name='description',
            field=models.TextField(null=True, verbose_name='P4.0: Please provide a short description of the project.'),
        ),
        migrations.AlterField(
            model_name='projectdetail',
            name='external_collaboration',
            field=models.CharField(max_length=1, null=True, verbose_name='C4.4: Did you collaborate with academics from other universities on the project?', choices=[(b'Y', 'Yes'), (b'N', 'No')]),
        ),
        migrations.AlterField(
            model_name='projectdetail',
            name='faculty',
            field=models.ForeignKey(verbose_name=b'P3.0: In which faculty / school is the project located?', to='herana.Faculty', null=True),
        ),
        migrations.AlterField(
            model_name='projectdetail',
            name='focus_area',
            field=models.ManyToManyField(help_text='Select ALL applicable<br>', to='herana.FocusArea', verbose_name='P5.0: In which of the following areas would you place your project?'),
        ),
        migrations.AlterField(
            model_name='projectdetail',
            name='initiation',
            field=models.PositiveIntegerField(null=True, verbose_name='A2.1: Which one of the following statements best describes how the project was initiated?', choices=[(1, 'Approached or invited by funder, company, NGO, government, research institute or by another university to submit a proposal for the project'), (2, 'Informed by the university research or contracts office about the reach project'), (3, 'Initiated by colleagues at own university'), (4, 'Initiated by project leader'), (5, 'Initiated by project leader in collaboration with colleagues'), (6, 'Follow-on or continuation from existing project'), (7, 'Project assigned to project leader')]),
        ),
        migrations.AlterField(
            model_name='projectdetail',
            name='is_flagship',
            field=models.CharField(max_length=1, null=True, verbose_name='G2: Do you consider this to be your flagship engagement project?', choices=[(b'Y', 'Yes'), (b'N', 'No')]),
        ),
        migrations.AlterField(
            model_name='projectdetail',
            name='is_leader',
            field=models.CharField(max_length=1, null=True, verbose_name='G1: Are you the designated leader of this engagement project?', choices=[(b'Y', 'Yes'), (b'N', 'No')]),
        ),
        migrations.AlterField(
            model_name='projectdetail',
            name='multi_faculty',
            field=models.CharField(max_length=1, null=True, verbose_name='P3.1: Does the project span multiple faculties / schools?', choices=[(b'Y', 'Yes'), (b'N', 'No')]),
        ),
        migrations.AlterField(
            model_name='projectdetail',
            name='name',
            field=models.CharField(max_length=512, verbose_name='P1.0: Please enter the name of the engagement project for which you wish to capture the details.'),
        ),
        migrations.AlterField(
            model_name='projectdetail',
            name='new_courses',
            field=models.CharField(max_length=1, null=True, verbose_name='C3.2: Have any new courses / modules / programmes been introduced as a result of this project?', choices=[(b'Y', 'Yes'), (b'N', 'No')]),
        ),
        migrations.AlterField(
            model_name='projectdetail',
            name='new_initiative',
            field=models.CharField(max_length=1, null=True, verbose_name='A3.2: Will any of the findings / results / outcomes of the project be used to implement or develop new products / services / interventions / policies?', choices=[(b'Y', 'Yes'), (b'N', 'No')]),
        ),
        migrations.AlterField(
            model_name='projectdetail',
            name='new_initiative_party',
            field=models.PositiveIntegerField(blank=True, null=True, verbose_name='Who will implement or develop these new products / services / interventions / policies?', choices=[(1, 'A third party has been contracted to develop the product / service / intervention / policy'), (2, 'The project team will develop the product / service / intervention / policy'), (3, 'Other')]),
        ),
        migrations.AlterField(
            model_name='projectdetail',
            name='new_initiative_party_text',
            field=models.TextField(null=True, verbose_name='Please provide the name of the third party or describe how the product / service / intervention / policy will be developed and / or implemented', blank=True),
        ),
        migrations.AlterField(
            model_name='projectdetail',
            name='outcomes',
            field=models.TextField(null=True, verbose_name='A1.2: What are the planned outcomes of the project?'),
        ),
        migrations.AlterField(
            model_name='projectdetail',
            name='outputs',
            field=models.ManyToManyField(to='herana.ProjectOutputs', verbose_name='C2: Please list the completed publications and other outputs for this project'),
        ),
        migrations.AlterField(
            model_name='projectdetail',
            name='phd_research',
            field=models.CharField(max_length=1, null=True, verbose_name="C.1.1.2: Is a student's PhD research linked to this project?", choices=[(b'Y', 'Yes'), (b'N', 'No')]),
        ),
        migrations.AlterField(
            model_name='projectdetail',
            name='project_status',
            field=models.PositiveIntegerField(null=True, verbose_name='P2.0: Project status', choices=[(1, 'Complete'), (2, 'Ongoing')]),
        ),
        migrations.AlterField(
            model_name='projectdetail',
            name='public_domain',
            field=models.CharField(help_text=b'If yes, please provide the URL', max_length=1, null=True, verbose_name='A2.4: Will the written up findings or data or other outputs of the project be available electronically in the public domain?', choices=[(b'Y', 'Yes'), (b'N', 'No')]),
        ),
        migrations.AlterField(
            model_name='projectdetail',
            name='research',
            field=models.PositiveIntegerField(null=True, verbose_name='C1.1.1: In terms of the research done for the project (if applicable), which statement best describes the project', choices=[(1, '1. The project conducted original research'), (2, '2. The project collected new data and conducted original research to complete the project'), (3, '3. The project collected new data and applied existing knowledge to the data collected to complete the project'), (4, '4. No new data was required and existing knowledge was applied to complete the project'), (5, '5. Not applicable')]),
        ),
        migrations.AlterField(
            model_name='projectdetail',
            name='strategic_objectives',
            field=models.ManyToManyField(help_text=b'Only select 4 options. <br>', to='herana.StrategicObjective', verbose_name='A1.1: What are the 4 main strategic objectives of the project?'),
        ),
        migrations.AlterField(
            model_name='projectdetail',
            name='student_nature',
            field=models.ManyToManyField(to='herana.StudentParticipationNature', verbose_name='C3.3.2: What is the nature of student participation in the project?', blank=True),
        ),
        migrations.AlterField(
            model_name='projectdetail',
            name='students_involved',
            field=models.CharField(max_length=1, null=True, verbose_name='C3.3.1: Are students involved in the project?', choices=[(b'Y', 'Yes'), (b'N', 'No')]),
        ),
        migrations.AlterField(
            model_name='projectdetail',
            name='team_members',
            field=models.ManyToManyField(to='herana.ResearchTeamMember', verbose_name='A3.1: Are any of the following members of the research team?', blank=True),
        ),
    ]
