# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
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
            name='Faculty',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=256)),
            ],
            options={
                'verbose_name_plural': 'Faculties',
            },
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
                ('logo', models.ImageField(null=True, upload_to=b'', blank=True)),
            ],
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
                ('name', models.CharField(max_length=512, verbose_name='P1.0: Please enter the name of the engagement project for which you wish to capture the details.')),
                ('date_created', models.DateField(auto_now_add=True)),
                ('is_leader', models.CharField(max_length=1, null=True, verbose_name='G1: Are you the designated leader of this engagement project?', choices=[(b'Y', 'Yes'), (b'N', 'No')])),
                ('is_flagship', models.CharField(max_length=1, null=True, verbose_name='G2: Do you consider this to be your flagship engagement project?', choices=[(b'Y', 'Yes'), (b'N', 'No')])),
                ('project_status', models.PositiveIntegerField(null=True, verbose_name='P2.0: Project status', choices=[(1, 'Complete'), (2, 'Ongoing')])),
                ('start_date', models.DateField(null=True, verbose_name='Start date')),
                ('end_date', models.DateField(null=True, verbose_name='End date', blank=True)),
                ('multi_faculty', models.CharField(max_length=1, null=True, verbose_name='P3.1: Does the project span multiple faculties / schools?', choices=[(b'Y', 'Yes'), (b'N', 'No')])),
                ('description', models.TextField(null=True, verbose_name='P4.0: Please provide a short description of the project.')),
                ('focus_area_text', models.CharField(max_length=256, null=True, verbose_name='If other was chosen above, please describe.', blank=True)),
                ('classification', models.PositiveIntegerField(null=True, verbose_name='P6.0: How would you classify this flagship engagement activity?', choices=[(1, 'Project'), (2, 'Programme'), (3, 'Service'), (4, 'Other')])),
                ('outcomes', models.TextField(null=True, verbose_name='A1.2: What are the planned outcomes of the project?')),
                ('beneficiaries', models.TextField(null=True, verbose_name='A1.3: Who are the intended beneficiaries of the project?')),
                ('initiation', models.PositiveIntegerField(null=True, verbose_name='A2.1: Which one of the following statements best describes how the project was initiated?', choices=[(1, 'Approached or invited by funder, company, NGO, government, research institute or by another university to submit a proposal for the project'), (2, 'Informed by the university research or contracts office about the reach project'), (3, 'Initiated by colleagues at own university'), (4, 'Initiated by project leader'), (5, 'Initiated by project leader in collaboration with colleagues'), (6, 'Follow-on or continuation from existing project'), (7, 'Project assigned to project leader')])),
                ('authors', models.PositiveIntegerField(null=True, verbose_name='A2.2: How many authors were involved in the writing of the project proposal / plan?', choices=[(1, 'One author'), (2, 'More than one author')])),
                ('amendments_permitted', models.CharField(max_length=1, null=True, verbose_name='A2.3: To the best of your knowledge, are deviations or amendments to the request for proposal permitted by the funder?', choices=[(b'Y', 'Yes'), (b'N', 'No')])),
                ('public_domain', models.CharField(help_text=b'If yes, please provide the URL', max_length=1, null=True, verbose_name='A2.4: Will the written up findings or data or other outputs of the project be available electronically in the public domain?', choices=[(b'Y', 'Yes'), (b'N', 'No')])),
                ('public_domain_url', models.URLField(null=True, verbose_name='URL', blank=True)),
                ('adv_group', models.CharField(max_length=1, null=True, verbose_name='A2.6: Does the project have an advisory group?', choices=[(b'Y', 'Yes'), (b'N', 'No')])),
                ('adv_group_freq', models.PositiveIntegerField(default=None, null=True, verbose_name='A2.7: How often does the advisory group meet?', blank=True, choices=[(None, 'N/A'), (1, 'Monthly'), (2, 'Quarterly'), (3, 'Annually'), (4, 'Ad hoc')])),
                ('team_members_text', models.TextField(null=True, verbose_name='If other was selected, please specify.', blank=True)),
                ('new_initiative', models.CharField(max_length=1, null=True, verbose_name='A3.2: Will any of the findings / results / outcomes of the project be used to implement or develop new products / services / interventions / policies?', choices=[(b'Y', 'Yes'), (b'N', 'No')])),
                ('new_initiative_text', models.TextField(null=True, verbose_name='If yes, please describe', blank=True)),
                ('new_initiative_party', models.PositiveIntegerField(blank=True, null=True, verbose_name='Who will implement or develop these new products / services / interventions / policies?', choices=[(1, 'A third party has been contracted to develop the product / service / intervention / policy'), (2, 'The project team will develop the product / service / intervention / policy'), (3, 'Other')])),
                ('new_initiative_party_text', models.TextField(null=True, verbose_name='Please provide the name of the third party or describe how the product / service / intervention / policy will be developed and / or implemented', blank=True)),
                ('research', models.PositiveIntegerField(null=True, verbose_name='C1.1.1: In terms of the research done for the project (if applicable), which statement best describes the project', choices=[(1, '1. The project conducted original research'), (2, '2. The project collected new data and conducted original research to complete the project'), (3, '3. The project collected new data and applied existing knowledge to the data collected to complete the project'), (4, '4. No new data was required and existing knowledge was applied to complete the project'), (5, '5. Not applicable')])),
                ('research_text', models.TextField(help_text='If <b>1, 2 or 3</b> selected, please provide a short description of the data collected or the original research conducted <br> If <b>4 or 5</b> selected, please explain why it was not necessary to collect new data or conduct original research', null=True, verbose_name='Please describe', blank=True)),
                ('phd_research', models.CharField(max_length=1, null=True, verbose_name="C.1.1.2: Is a student's PhD research linked to this project?", choices=[(b'Y', 'Yes'), (b'N', 'No')])),
                ('curriculum_changes', models.CharField(max_length=1, null=True, verbose_name='C3.1: Has the project lead to any contributions or changes to the curriculum?', choices=[(b'Y', 'Yes'), (b'N', 'No')])),
                ('curriculum_changes_text', models.TextField(null=True, verbose_name='If yes, please describe the types of changes made to the curriculum as a result of the project', blank=True)),
                ('new_courses', models.CharField(max_length=1, null=True, verbose_name='C3.2: Have any new courses / modules / programmes been introduced as a result of this project?', choices=[(b'Y', 'Yes'), (b'N', 'No')])),
                ('students_involved', models.CharField(max_length=1, null=True, verbose_name='C3.3.1: Are students involved in the project?', choices=[(b'Y', 'Yes'), (b'N', 'No')])),
                ('student_nature_text', models.CharField(max_length=128, null=True, verbose_name='If other was selected, please describe.', blank=True)),
                ('course_requirement', models.CharField(max_length=1, null=True, verbose_name='C3.4: Is participation in the project a requirement for the completion of an existing course / degree offered by the university?', choices=[(b'Y', 'Yes'), (b'N', 'No')])),
                ('external_collaboration', models.CharField(max_length=1, null=True, verbose_name='C4.4: Did you collaborate with academics from other universities on the project?', choices=[(b'Y', 'Yes'), (b'N', 'No')])),
                ('record_status', models.PositiveIntegerField(choices=[(1, b'Draft'), (2, b'Final')])),
                ('rejected', models.BooleanField(default=False)),
                ('rejected_detail', models.TextField(null=True)),
                ('adv_group_rep', models.ManyToManyField(to='herana.AdvisoryGroupRep', verbose_name='A2.6.1: If yes, are any of the following members of the advisory group?', blank=True)),
                ('faculty', models.ForeignKey(verbose_name=b'P3.0: In which faculty / school is the project located?', to='herana.Faculty', null=True)),
                ('focus_area', models.ManyToManyField(help_text='Select ALL applicable<br>', to='herana.FocusArea', verbose_name='P5.0: In which of the following areas would you place your project?')),
            ],
            options={
                'verbose_name': 'Project detail',
                'verbose_name_plural': 'Project details',
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
                ('faculty', models.ForeignKey(to='herana.Faculty')),
                ('institute', models.ForeignKey(to='herana.Institute')),
                ('user', models.OneToOneField(related_name='project_leader', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='ProjectOutput',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('url', models.URLField(null=True, blank=True)),
                ('doi', models.CharField(max_length=128, null=True, blank=True)),
                ('attachment', models.FileField(null=True, upload_to=b'projects/attachments/output/', blank=True)),
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
        migrations.AddField(
            model_name='projectoutput',
            name='type',
            field=models.ForeignKey(to='herana.ProjectOutputType'),
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
            field=models.ManyToManyField(help_text=b'Only select 4 options. <br>', to='herana.StrategicObjective', verbose_name='A1.1: What are the 4 main strategic objectives of the project?'),
        ),
        migrations.AddField(
            model_name='projectdetail',
            name='student_nature',
            field=models.ManyToManyField(to='herana.StudentParticipationNature', verbose_name='C3.3.2: What is the nature of student participation in the project?', blank=True),
        ),
        migrations.AddField(
            model_name='projectdetail',
            name='student_types',
            field=models.ManyToManyField(to='herana.StudentType', verbose_name='If yes, please indicate types of students participating', blank=True),
        ),
        migrations.AddField(
            model_name='projectdetail',
            name='team_members',
            field=models.ManyToManyField(to='herana.ResearchTeamMember', verbose_name='A3.1: Are any of the following members of the research team?', blank=True),
        ),
        migrations.AddField(
            model_name='phdstudent',
            name='project',
            field=models.ForeignKey(to='herana.ProjectDetail'),
        ),
        migrations.AddField(
            model_name='newcoursedetail',
            name='project',
            field=models.ForeignKey(to='herana.ProjectDetail'),
        ),
        migrations.AddField(
            model_name='faculty',
            name='institute',
            field=models.ForeignKey(to='herana.Institute'),
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
    ]
