# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('herana', '0002_auto_20150625_1417'),
    ]

    operations = [
        migrations.AlterField(
            model_name='projectdetail',
            name='adv_group',
            field=models.CharField(max_length=1, null=True, choices=[(b'Y', 'Yes'), (b'N', 'No')]),
        ),
        migrations.AlterField(
            model_name='projectdetail',
            name='adv_group_freq',
            field=models.PositiveIntegerField(null=True, choices=[(1, 'Monthly'), (2, 'Quarterly'), (3, 'Annually'), (4, 'Ad hoc')]),
        ),
        migrations.AlterField(
            model_name='projectdetail',
            name='adv_group_rep',
            field=models.ManyToManyField(to='herana.AdvisoryGroupRep'),
        ),
        migrations.AlterField(
            model_name='projectdetail',
            name='amendments_permitted',
            field=models.CharField(max_length=1, null=True, choices=[(b'Y', 'Yes'), (b'N', 'No')]),
        ),
        migrations.AlterField(
            model_name='projectdetail',
            name='authors',
            field=models.PositiveIntegerField(null=True, choices=[(1, 'One author'), (1, 'More than one author')]),
        ),
        migrations.AlterField(
            model_name='projectdetail',
            name='beneficiaries',
            field=models.TextField(null=True),
        ),
        migrations.AlterField(
            model_name='projectdetail',
            name='classification',
            field=models.PositiveIntegerField(null=True, choices=[(1, 'Project'), (2, 'Programme'), (3, 'Service'), (4, 'Other')]),
        ),
        migrations.AlterField(
            model_name='projectdetail',
            name='collaboration_detail',
            field=models.ManyToManyField(to='herana.Collaborators'),
        ),
        migrations.AlterField(
            model_name='projectdetail',
            name='course_req_detail',
            field=models.ManyToManyField(to='herana.CourseReqDetail'),
        ),
        migrations.AlterField(
            model_name='projectdetail',
            name='course_requirement',
            field=models.CharField(max_length=1, null=True, choices=[(b'Y', 'Yes'), (b'N', 'No')]),
        ),
        migrations.AlterField(
            model_name='projectdetail',
            name='curriculum_changes',
            field=models.CharField(max_length=1, null=True, choices=[(b'Y', 'Yes'), (b'N', 'No')]),
        ),
        migrations.AlterField(
            model_name='projectdetail',
            name='curriculum_changes_text',
            field=models.TextField(null=True),
        ),
        migrations.AlterField(
            model_name='projectdetail',
            name='description',
            field=models.TextField(null=True),
        ),
        migrations.AlterField(
            model_name='projectdetail',
            name='end_date',
            field=models.DateField(null=True),
        ),
        migrations.AlterField(
            model_name='projectdetail',
            name='external_collaboration',
            field=models.CharField(max_length=1, null=True, choices=[(b'Y', 'Yes'), (b'N', 'No')]),
        ),
        migrations.AlterField(
            model_name='projectdetail',
            name='focus_area',
            field=models.ManyToManyField(to='herana.FocusArea'),
        ),
        migrations.AlterField(
            model_name='projectdetail',
            name='focus_area_text',
            field=models.CharField(max_length=256, null=True),
        ),
        migrations.AlterField(
            model_name='projectdetail',
            name='funding',
            field=models.ManyToManyField(to='herana.ProjectFunding'),
        ),
        migrations.AlterField(
            model_name='projectdetail',
            name='header',
            field=models.ForeignKey(related_name='project_detail', to='herana.ProjectHeader'),
        ),
        migrations.AlterField(
            model_name='projectdetail',
            name='initiation',
            field=models.PositiveIntegerField(null=True, choices=[(1, 'Approached or invited by funder, company, NGO, government, research institute or by another university to submit a proposal for the project'), (2, 'Informed by the university research or contracts office about the reach project'), (3, 'Initiated by colleagues at own university'), (4, 'Initiated by project leader'), (5, 'Initiated by project leader in collaboration with colleagues'), (6, 'Follow-on or continuation from existing project'), (7, 'Project assigned to project leader')]),
        ),
        migrations.AlterField(
            model_name='projectdetail',
            name='multi_faculty',
            field=models.CharField(max_length=1, null=True, choices=[(b'Y', 'Yes'), (b'N', 'No')]),
        ),
        migrations.AlterField(
            model_name='projectdetail',
            name='new_course_detail',
            field=models.ManyToManyField(to='herana.NewCourseDetail'),
        ),
        migrations.AlterField(
            model_name='projectdetail',
            name='new_courses',
            field=models.CharField(max_length=1, null=True, choices=[(b'Y', 'Yes'), (b'N', 'No')]),
        ),
        migrations.AlterField(
            model_name='projectdetail',
            name='new_initiative',
            field=models.CharField(max_length=1, null=True, choices=[(b'Y', 'Yes'), (b'N', 'No')]),
        ),
        migrations.AlterField(
            model_name='projectdetail',
            name='new_initiative_party',
            field=models.PositiveIntegerField(null=True, choices=[(1, 'A third party has been contracted to develop the product / service / intervention / policy'), (2, 'The project team will develop the product / service / intervention / policy'), (3, 'Other')]),
        ),
        migrations.AlterField(
            model_name='projectdetail',
            name='new_initiative_party_text',
            field=models.TextField(null=True),
        ),
        migrations.AlterField(
            model_name='projectdetail',
            name='new_initiative_text',
            field=models.TextField(null=True),
        ),
        migrations.AlterField(
            model_name='projectdetail',
            name='ongoing',
            field=models.CharField(max_length=1, null=True, choices=[(b'Y', 'Yes'), (b'N', 'No')]),
        ),
        migrations.AlterField(
            model_name='projectdetail',
            name='outcomes',
            field=models.TextField(null=True),
        ),
        migrations.AlterField(
            model_name='projectdetail',
            name='outputs',
            field=models.ManyToManyField(to='herana.ProjectOutputs'),
        ),
        migrations.AlterField(
            model_name='projectdetail',
            name='phd_research',
            field=models.CharField(max_length=1, null=True, choices=[(b'Y', 'Yes'), (b'N', 'No')]),
        ),
        migrations.AlterField(
            model_name='projectdetail',
            name='phd_research_name',
            field=models.ManyToManyField(to='herana.PHDStudent'),
        ),
        migrations.AlterField(
            model_name='projectdetail',
            name='public_domain',
            field=models.CharField(max_length=1, null=True, choices=[(b'Y', 'Yes'), (b'N', 'No')]),
        ),
        migrations.AlterField(
            model_name='projectdetail',
            name='public_domain_url',
            field=models.URLField(null=True),
        ),
        migrations.AlterField(
            model_name='projectdetail',
            name='research',
            field=models.PositiveIntegerField(null=True, choices=[(1, 'The project conducted original research'), (2, 'The project collected new data and conducted original research to complete the project'), (3, 'The project collected new data and applied existing knowledge to the data collected to complete the project'), (4, 'No new data was required and existing knowledge was applied to complete the project'), (5, 'Not applicable')]),
        ),
        migrations.AlterField(
            model_name='projectdetail',
            name='research_text',
            field=models.TextField(null=True),
        ),
        migrations.AlterField(
            model_name='projectdetail',
            name='start_date',
            field=models.DateField(null=True),
        ),
        migrations.AlterField(
            model_name='projectdetail',
            name='status',
            field=models.PositiveIntegerField(choices=[(1, b'Incomplete'), (2, b'Final'), (3, b'Rejected')]),
        ),
        migrations.AlterField(
            model_name='projectdetail',
            name='strategic_objectives',
            field=models.ManyToManyField(to='herana.StrategicObjective'),
        ),
        migrations.AlterField(
            model_name='projectdetail',
            name='student_nature',
            field=models.ManyToManyField(to='herana.StudentParticipationNature'),
        ),
        migrations.AlterField(
            model_name='projectdetail',
            name='student_nature_text',
            field=models.CharField(max_length=128, null=True),
        ),
        migrations.AlterField(
            model_name='projectdetail',
            name='student_types',
            field=models.ManyToManyField(to='herana.StudentType'),
        ),
        migrations.AlterField(
            model_name='projectdetail',
            name='students_involved',
            field=models.CharField(max_length=1, null=True, choices=[(b'Y', 'Yes'), (b'N', 'No')]),
        ),
        migrations.AlterField(
            model_name='projectdetail',
            name='team_members',
            field=models.ManyToManyField(to='herana.ResearchTeamMember'),
        ),
    ]
