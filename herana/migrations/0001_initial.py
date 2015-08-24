# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import herana.models
import django.utils.timezone
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('auth', '0006_require_contenttypes_0002'),
    ]

    operations = [
        migrations.CreateModel(
            name='CustomUser',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(null=True, verbose_name='last login', blank=True)),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('email', models.EmailField(unique=True, max_length=254)),
                ('first_name', models.CharField(max_length=30, verbose_name='first name', blank=True)),
                ('last_name', models.CharField(max_length=30, verbose_name='last name', blank=True)),
                ('is_staff', models.BooleanField(default=False, help_text='Designates whether the user can log into this admin site.', verbose_name='staff status')),
                ('is_active', models.BooleanField(default=True, help_text='Designates whether this user should be treated as active. Unselect this instead of deleting accounts.', verbose_name='active')),
                ('date_joined', models.DateTimeField(default=django.utils.timezone.now, verbose_name='date joined')),
                ('groups', models.ManyToManyField(related_query_name='user', related_name='user_set', to='auth.Group', blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', verbose_name='groups')),
                ('user_permissions', models.ManyToManyField(related_query_name='user', related_name='user_set', to='auth.Permission', blank=True, help_text='Specific permissions for this user.', verbose_name='user permissions')),
            ],
            options={
                'verbose_name': 'User',
            },
        ),
        migrations.CreateModel(
            name='AdvisoryGroupRep',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('code', models.PositiveIntegerField(unique=True)),
                ('choice', models.CharField(max_length=256)),
            ],
        ),
        migrations.CreateModel(
            name='Collaborators',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=128)),
                ('university', models.CharField(max_length=128)),
            ],
        ),
        migrations.CreateModel(
            name='CourseReqDetail',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('code', models.CharField(max_length=32)),
                ('name', models.CharField(max_length=128)),
            ],
        ),
        migrations.CreateModel(
            name='FocusArea',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('code', models.PositiveIntegerField(unique=True)),
                ('choice', models.CharField(max_length=256)),
            ],
        ),
        migrations.CreateModel(
            name='Institute',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=256)),
                ('logo', models.ImageField(null=True, upload_to=herana.models.image_filename, blank=True)),
            ],
            options={
                'ordering': ['name'],
            },
        ),
        migrations.CreateModel(
            name='InstituteAdmin',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('institute', models.ForeignKey(related_name='institute_admin', to='herana.Institute')),
                ('user', models.OneToOneField(related_name='institute_admin', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='NewCourseDetail',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('code', models.CharField(max_length=32)),
                ('name', models.CharField(max_length=128)),
            ],
        ),
        migrations.CreateModel(
            name='OrgLevel',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=256)),
            ],
            options={
                'ordering': ['name'],
                'verbose_name': 'Organisational level',
                'verbose_name_plural': 'Organisational Levels',
            },
        ),
        migrations.CreateModel(
            name='PHDStudent',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=128)),
            ],
        ),
        migrations.CreateModel(
            name='ProjectDetail',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=512, verbose_name='1.1: Please enter the name of the engagement project for which you wish to capture the details.')),
                ('is_leader', models.CharField(max_length=1, null=True, verbose_name='1.2: Are you the designated leader of this engagement project?', choices=[(b'Y', 'Yes'), (b'N', 'No')])),
                ('is_flagship', models.CharField(max_length=1, null=True, verbose_name='1.3: Do you consider this to be your flagship engagement project?', choices=[(b'Y', 'Yes'), (b'N', 'No')])),
                ('project_status', models.PositiveIntegerField(null=True, verbose_name='2.1: Project status', choices=[(1, 'Complete'), (2, 'Ongoing')])),
                ('start_date', models.DateField(null=True, verbose_name='2.2.1: Start date')),
                ('end_date', models.DateField(null=True, verbose_name='2.2.2: End date', blank=True)),
                ('multi_faculty', models.CharField(max_length=1, null=True, verbose_name='2.3.1: Does the project span multiple faculties / schools?', choices=[(b'Y', 'Yes'), (b'N', 'No')])),
                ('description', models.TextField(null=True, verbose_name='2.4: Please provide a short description of the project.')),
                ('focus_area_text', models.CharField(max_length=256, null=True, verbose_name='2.5.1: If other was chosen above, please describe.', blank=True)),
                ('classification', models.PositiveIntegerField(null=True, verbose_name='2.6: How would you classify this flagship engagement activity?', choices=[(1, 'Project'), (2, 'Programme'), (3, 'Service'), (4, 'Other')])),
                ('outcomes', models.TextField(null=True, verbose_name='3.2: What are the planned outcomes of the project?')),
                ('beneficiaries', models.TextField(null=True, verbose_name='3.3: Who are the intended beneficiaries of the project?')),
                ('initiation', models.PositiveIntegerField(null=True, verbose_name='4.1: Which one of the following statements best describes how the project was initiated?', choices=[(1, 'Approached or invited by funder, company, NGO, government, research institute or by another university to submit a proposal for the project'), (2, 'Informed by the university research or contracts office about the reach project'), (3, 'Initiated by colleagues at own university'), (4, 'Initiated by project leader'), (5, 'Initiated by project leader in collaboration with colleagues'), (6, 'Follow-on or continuation from existing project'), (7, 'Project assigned to project leader')])),
                ('authors', models.PositiveIntegerField(null=True, verbose_name='4.2: How many authors were involved in the writing of the project proposal / plan?', choices=[(1, 'One author'), (2, 'More than one author')])),
                ('amendments_permitted', models.CharField(max_length=1, null=True, verbose_name='4.3: To the best of your knowledge, are deviations or amendments to the request for proposal permitted by the funder?', choices=[(b'Y', 'Yes'), (b'N', 'No')])),
                ('public_domain', models.CharField(help_text=b'If yes, please provide the URL', max_length=1, null=True, verbose_name='4.4: Are the project proposal, written up findings of the project available electronically in the public domain?', choices=[(b'Y', 'Yes'), (b'N', 'No')])),
                ('public_domain_url', models.URLField(null=True, verbose_name='4.4.1: URL', blank=True)),
                ('adv_group', models.CharField(max_length=1, null=True, verbose_name='4.5: Does the project have an advisory group?', choices=[(b'Y', 'Yes'), (b'N', 'No')])),
                ('adv_group_freq', models.PositiveIntegerField(default=None, null=True, verbose_name='4.6: How often does the advisory group meet?', blank=True, choices=[(1, 'Monthly'), (2, 'Quarterly'), (3, 'Annually'), (4, 'Ad hoc'), (None, 'Not applicable')])),
                ('team_members_text', models.TextField(null=True, verbose_name='5.1.1: If other was selected, please specify.', blank=True)),
                ('new_initiative', models.CharField(max_length=1, null=True, verbose_name='5.2: Have any of the findings / results / outcomes of the project been used to implement or develop new products / services / interventions / policies?', choices=[(b'Y', 'Yes'), (b'N', 'No')])),
                ('new_initiative_text', models.TextField(null=True, verbose_name='5.2.1: If yes, please describe', blank=True)),
                ('new_initiative_party', models.PositiveIntegerField(default=None, null=True, verbose_name='5.2.2: Who implemented or developed these new products / services / interventions / policies?', blank=True, choices=[(1, 'A third party has been contracted to develop the product / service / intervention / policy'), (2, 'The project team will develop the product / service / intervention / policy'), (3, 'Other'), (None, 'Not applicable')])),
                ('new_initiative_party_text', models.TextField(null=True, verbose_name='5.2.3: Please provide the name of the third party or describe how the product / service / intervention / policy was developed and / or implemented.', blank=True)),
                ('research', models.PositiveIntegerField(null=True, verbose_name='7.1: In terms of the research done for the project (if applicable), which statement best describes the project.', choices=[(1, '1. The project conducted original research'), (2, '2. The project collected new data and conducted original research to complete the project'), (3, '3. The project collected new data and applied existing knowledge to the data collected to complete the project'), (4, '4. No new data was required and existing knowledge was applied to complete the project'), (5, '5. Not applicable')])),
                ('research_text', models.TextField(help_text='If <b>1, 2 or 3</b> selected, please provide a short description of the data collected or the original research conducted <br> If <b>4 or 5</b> selected, please explain why it was not necessary to collect new data or conduct original research', null=True, verbose_name='7.1.1: Please describe.', blank=True)),
                ('phd_research', models.CharField(max_length=1, null=True, verbose_name="7.2: Is a student's PhD research linked to this project?", choices=[(b'Y', 'Yes'), (b'N', 'No')])),
                ('curriculum_changes', models.CharField(max_length=1, null=True, verbose_name='9.1: Has the project lead to any contributions or changes to the curriculum?', choices=[(b'Y', 'Yes'), (b'N', 'No')])),
                ('curriculum_changes_text', models.TextField(null=True, verbose_name='9.1.1: If yes, please describe the types of changes made to the curriculum as a result of the project.', blank=True)),
                ('new_courses', models.CharField(max_length=1, null=True, verbose_name='9.2: Have any new courses / modules / programmes been introduced as a result of this project?', choices=[(b'Y', 'Yes'), (b'N', 'No')])),
                ('students_involved', models.CharField(max_length=1, null=True, verbose_name='9.3: Are students involved in the project?', choices=[(b'Y', 'Yes'), (b'N', 'No')])),
                ('student_nature_text', models.CharField(max_length=128, null=True, verbose_name='9.4.1: If other was selected, please describe.', blank=True)),
                ('course_requirement', models.CharField(max_length=1, null=True, verbose_name='9.5: Is participation in the project a requirement for the completion of an existing course / degree offered by the university?', choices=[(b'Y', 'Yes'), (b'N', 'No')])),
                ('external_collaboration', models.CharField(max_length=1, null=True, verbose_name='10.1: Did you collaborate with academics from other universities on the project?', choices=[(b'Y', 'Yes'), (b'N', 'No')])),
                ('record_status', models.PositiveIntegerField(choices=[(1, b'Draft'), (2, b'Final')])),
                ('is_rejected', models.BooleanField(default=False, verbose_name='Rejected')),
                ('rejected_detail', models.TextField(null=True, blank=True)),
                ('is_flagged', models.BooleanField(default=False, verbose_name='Suspect')),
                ('is_deleted', models.BooleanField(default=False)),
                ('created_at', models.DateField(auto_now_add=True)),
                ('adv_group_rep', models.ManyToManyField(to='herana.AdvisoryGroupRep', verbose_name='4.5.1: If yes, are any of the following members of the advisory group?', blank=True)),
                ('focus_area', models.ManyToManyField(help_text='Select ALL applicable<br>', to='herana.FocusArea', verbose_name='2.5: In which of the following areas would you place your project?')),
                ('institute', models.ForeignKey(to='herana.Institute')),
            ],
            options={
                'verbose_name': 'Engagement project',
                'verbose_name_plural': 'Engagement projects',
                'permissions': (('view_projectdetail', 'Can only view project details'), ('reject_projectdetail', 'Can reject the project which has been submitted')),
            },
        ),
        migrations.CreateModel(
            name='ProjectFunding',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('funder', models.CharField(max_length=256)),
                ('amount', models.DecimalField(max_digits=10, decimal_places=2)),
                ('years', models.DecimalField(max_digits=5, decimal_places=2)),
                ('renewable', models.CharField(max_length=1, null=True, choices=[(b'Y', 'Yes'), (b'N', 'No')])),
                ('project', models.ForeignKey(to='herana.ProjectDetail')),
            ],
        ),
        migrations.CreateModel(
            name='ProjectLeader',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('staff_no', models.CharField(max_length=64)),
                ('position', models.CharField(max_length=128)),
                ('institute', models.ForeignKey(to='herana.Institute')),
                ('user', models.OneToOneField(related_name='project_leader', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='ProjectOutput',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('output_title', models.CharField(max_length=255, null=True, verbose_name='8.1.2: Title of output (e.g. title of journal article, book chapter, presentation, performance, etc.)', blank=True)),
                ('pub_title', models.CharField(max_length=255, null=True, verbose_name='8.1.3: Title of journal, book, conference, blog, periodical, event, etc.', blank=True)),
                ('url', models.URLField(null=True, verbose_name='8.1.4: URL', blank=True)),
                ('doi', models.CharField(max_length=128, null=True, verbose_name='8.1.5: DOI', blank=True)),
                ('attachment', models.FileField(upload_to=herana.models.attachment_filename, null=True, verbose_name='8.1.6: Attachment (Please provide an attachment of the output should a URL not be available. If the output is confidential, embargoed, etc., please provide a PDF of the cover page only)', blank=True)),
                ('project', models.ForeignKey(to='herana.ProjectDetail')),
            ],
        ),
        migrations.CreateModel(
            name='ProjectOutputType',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('code', models.PositiveIntegerField(unique=True)),
                ('choice', models.CharField(max_length=128)),
            ],
        ),
        migrations.CreateModel(
            name='ReportingPeriod',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=128)),
                ('description', models.TextField()),
                ('open_date', models.DateField(auto_now_add=True)),
                ('close_date', models.DateField(null=True, blank=True)),
                ('is_active', models.BooleanField(default=True, verbose_name='Open')),
                ('institute', models.ForeignKey(related_name='reporting_period', to='herana.Institute')),
            ],
        ),
        migrations.CreateModel(
            name='ResearchTeamMember',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('code', models.PositiveIntegerField(unique=True)),
                ('choice', models.CharField(max_length=256)),
            ],
        ),
        migrations.CreateModel(
            name='StrategicObjective',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('statement', models.CharField(max_length=512)),
                ('institute', models.ForeignKey(to='herana.Institute')),
            ],
        ),
        migrations.CreateModel(
            name='StudentParticipationNature',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('code', models.PositiveIntegerField(unique=True)),
                ('choice', models.CharField(max_length=128)),
            ],
        ),
        migrations.CreateModel(
            name='StudentType',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('code', models.PositiveIntegerField(unique=True)),
                ('choice', models.CharField(max_length=32)),
            ],
        ),
        migrations.CreateModel(
            name='OrgLevel1',
            fields=[
                ('orglevel_ptr', models.OneToOneField(parent_link=True, auto_created=True, primary_key=True, serialize=False, to='herana.OrgLevel')),
            ],
            options={
                'verbose_name': 'Organisational Level 1',
                'verbose_name_plural': 'Organisational Level 1',
            },
            bases=('herana.orglevel',),
        ),
        migrations.CreateModel(
            name='OrgLevel2',
            fields=[
                ('orglevel_ptr', models.OneToOneField(parent_link=True, auto_created=True, primary_key=True, serialize=False, to='herana.OrgLevel')),
                ('parent', models.ForeignKey(to='herana.OrgLevel1')),
            ],
            options={
                'verbose_name': 'Organisational Level 2',
                'verbose_name_plural': 'Organisational Level 2',
            },
            bases=('herana.orglevel',),
        ),
        migrations.CreateModel(
            name='OrgLevel3',
            fields=[
                ('orglevel_ptr', models.OneToOneField(parent_link=True, auto_created=True, primary_key=True, serialize=False, to='herana.OrgLevel')),
                ('parent', models.ForeignKey(to='herana.OrgLevel2')),
            ],
            options={
                'verbose_name': 'Organisational Level 3',
                'verbose_name_plural': 'Organisational Level 3',
            },
            bases=('herana.orglevel',),
        ),
        migrations.AddField(
            model_name='projectoutput',
            name='type',
            field=models.ForeignKey(verbose_name='8.1.1: Output type', to='herana.ProjectOutputType'),
        ),
        migrations.AddField(
            model_name='projectdetail',
            name='proj_leader',
            field=models.ForeignKey(to='herana.ProjectLeader'),
        ),
        migrations.AddField(
            model_name='projectdetail',
            name='reporting_period',
            field=models.ForeignKey(to='herana.ReportingPeriod'),
        ),
        migrations.AddField(
            model_name='projectdetail',
            name='strategic_objectives',
            field=models.ManyToManyField(help_text=b'Only select 4 options. <br>', to='herana.StrategicObjective', verbose_name='3.1: What are the 4 main strategic objectives of the project?'),
        ),
        migrations.AddField(
            model_name='projectdetail',
            name='student_nature',
            field=models.ManyToManyField(to='herana.StudentParticipationNature', verbose_name='9.4: What is the nature of student participation in the project?', blank=True),
        ),
        migrations.AddField(
            model_name='projectdetail',
            name='student_types',
            field=models.ManyToManyField(to='herana.StudentType', verbose_name='9.3.1: If yes, please indicate types of students participating.', blank=True),
        ),
        migrations.AddField(
            model_name='projectdetail',
            name='team_members',
            field=models.ManyToManyField(to='herana.ResearchTeamMember', verbose_name='5.1: Are any of the following members of the research team?', blank=True),
        ),
        migrations.AddField(
            model_name='phdstudent',
            name='project',
            field=models.ForeignKey(to='herana.ProjectDetail'),
        ),
        migrations.AddField(
            model_name='orglevel',
            name='institute',
            field=models.ForeignKey(to='herana.Institute'),
        ),
        migrations.AddField(
            model_name='newcoursedetail',
            name='project',
            field=models.ForeignKey(to='herana.ProjectDetail'),
        ),
        migrations.AddField(
            model_name='coursereqdetail',
            name='project',
            field=models.ForeignKey(to='herana.ProjectDetail'),
        ),
        migrations.AddField(
            model_name='collaborators',
            name='project',
            field=models.ForeignKey(to='herana.ProjectDetail'),
        ),
        migrations.AddField(
            model_name='projectleader',
            name='org_level_1',
            field=models.ForeignKey(to='herana.OrgLevel1'),
        ),
        migrations.AddField(
            model_name='projectleader',
            name='org_level_2',
            field=models.ForeignKey(blank=True, to='herana.OrgLevel2', null=True),
        ),
        migrations.AddField(
            model_name='projectleader',
            name='org_level_3',
            field=models.ForeignKey(blank=True, to='herana.OrgLevel3', null=True),
        ),
        migrations.AddField(
            model_name='projectdetail',
            name='org_level_1',
            field=models.ForeignKey(to='herana.OrgLevel1'),
        ),
        migrations.AddField(
            model_name='projectdetail',
            name='org_level_2',
            field=models.ForeignKey(blank=True, to='herana.OrgLevel2', null=True),
        ),
        migrations.AddField(
            model_name='projectdetail',
            name='org_level_3',
            field=models.ForeignKey(blank=True, to='herana.OrgLevel3', null=True),
        ),
    ]
