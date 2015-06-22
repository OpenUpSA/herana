from django.db import models
from django.contrib.auth.models import User
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
    (3, ('Annually')),
    (4, ('Ad hoc'))
)

INITIATIVE_PARTIES = (
    (1, _('A third party has been contracted to develop the product / service / intervention / policy')),
    (2, _('The project team will develop the product / service / intervention / policy')),
    (3, _('Other')),
)

RESEARCH_CLASSIFICATION = (
    (1, ('The project conducted original research')),
    (2, ('The project collected new data and conducted original research to complete the project')),
    (3, ('The project collected new data and applied existing knowledge to the data collected to complete the project')),
    (4, ('No new data was required and existing knowledge was applied to complete the project')),
    (5, ('Not applicable'))
)

RECORD_STATUS = (
    (1, 'Incomplete'),
    (2, 'Final'),
    (3, 'Rejected')
)


class Institute(models.Model):
    name = models.CharField(max_length=256)
    logo = models.ImageField()


class Faculty(models.Model):
    name = models.CharField(max_length=256)
    institute = models.ForeignKey('Institute')


class StrategicObjective(models.Model):
    institute = models.ForeignKey('Institute')
    statement = models.CharField(max_length=512)


class InstituteAdmin(models.Model):
    user = models.OneToOneField(User)
    institute = models.ForeignKey('Institute')


class ProjectLeader(models.Model):
    user = models.OneToOneField(User)
    institute = models.ForeignKey('Institute')
    faculty = models.ForeignKey('Faculty')
    staff_no = models.CharField(max_length=64)
    position = models.CharField(max_length=128)


class ReportingPeriod(models.Model):
    name = models.CharField(max_length=128)
    description = models.TextField()
    open_date = models.DateField(auto_now_add=True)
    close_date = models.DateField()


class FocusArea(models.Model):
    choice = models.CharField(max_length=256)

class AdvisoryGroupRep(models.Model):
    choice = models.CharField(max_length=256)

class ResearchTeamMember(models.Model):
    choice = models.CharField(max_length=256)

class ProjectFunding(models.Model):
    funder = models.CharField(max_length=256)
    amount = models.DecimalField(decimal_places=2, max_digits=10)
    years = models.DecimalField(decimal_places=2, max_digits=5)
    renewable = models.BooleanField(choices=YESNO)

class PHDStudent(models.Model):
    name = models.CharField(max_length=128)

class ProjectOutputs(models.Model):
    choice = models.CharField(max_length=128)\

class NewCourseDetail(models.Model):
    code = models.CharField(max_length=32)
    name = models.CharField(max_length=128)

class StudentType(models.Model):
    choice = models.CharField(max_length=32)

class StudentParticipationNature(models.Model):
    choice = models.CharField(max_length=128)

class CourseReqDetail(models.Model):
    code = models.CharField(max_length=32)
    name = models.CharField(max_length=128)

class Collaborators(models.Model):
    name = models.CharField(max_length=128)
    university = models.CharField(max_length=128)


class ProjectHeader(models.Model):
    name = models.CharField(max_length=512)
    faculty = models.ForeignKey('Faculty')
    proj_leader = models.ForeignKey('ProjectLeader')
    date_created = models.DateField(auto_now_add=True)

    is_flagship = models.BooleanField(default=False)
    is_leader = models.BooleanField(default=False)
    # status = models.ChoiceField()


class ProjectDetail(models.Model):
    header = models.ForeignKey(ProjectHeader)
    start_date = models.DateField()
    end_date = models.DateField()
    ongoing = models.BooleanField()
    multi_faculty = models.CharField(choices=YESNO, max_length=1)
    description = models.TextField()
    focus_area = models.ManyToManyField('FocusArea')
    focus_area_text = models.CharField(max_length=256)
    classification = models.PositiveIntegerField(choices=CLASSIFICATION)
    strategic_objectives = models.ManyToManyField('StrategicObjective')
    outcomes = models.TextField()
    beneficiaries = models.TextField()
    initiation = models.PositiveIntegerField(choices=INITIATION_STATEMENTS)
    authors = models.PositiveIntegerField(choices=NUMBER_AUTHORS)
    amendments_permitted = models.CharField(choices=YESNO, max_length=1)
    public_domain = models.CharField(choices=YESNO, max_length=1)
    public_domain_url = models.URLField()
    adv_group = models.CharField(choices=YESNO, max_length=1)
    adv_group_rep = models.ManyToManyField('AdvisoryGroupRep')
    adv_group_freq = models.PositiveIntegerField(choices=ADV_GROUP_FREQ)
    team_members = models.ManyToManyField(ResearchTeamMember)
    new_initiative = models.CharField(choices=YESNO, max_length=1)
    new_initiative_text = models.TextField()
    new_initiative_party = models.PositiveIntegerField(choices=INITIATIVE_PARTIES)
    new_initiative_party_text = models.TextField()
    funding = models.ManyToManyField(ProjectFunding)
    research = models.PositiveIntegerField(choices=RESEARCH_CLASSIFICATION)
    research_text = models.TextField()
    phd_research = models.CharField(choices=YESNO, max_length=1)
    phd_research_name = models.ManyToManyField('PHDStudent')
    outputs = models.ManyToManyField('ProjectOutputs')
    curriculum_changes = models.CharField(choices=YESNO, max_length=1)
    curriculum_changes_text = models.TextField()
    new_courses = models.CharField(choices=YESNO, max_length=1)
    new_course_detail = models.ManyToManyField('NewCourseDetail')
    students_involved = models.CharField(choices=YESNO, max_length=1)
    student_types = models.ManyToManyField('StudentType')
    student_nature = models.ManyToManyField(StudentParticipationNature)
    student_nature_text = models.CharField(max_length=128)
    course_requirement = models.CharField(choices=YESNO, max_length=1)
    course_req_detail = models.ManyToManyField('CourseReqDetail')
    external_collaboration = models.CharField(choices=YESNO, max_length=1)
    collaboration_detail = models.ManyToManyField('Collaborators')
    status = models.PositiveIntegerField(choices=RECORD_STATUS)
    reporting_period = models.ForeignKey('ReportingPeriod')
