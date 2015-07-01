from django.db import models
from django.contrib.auth.models import User, Group, Permission
from django.utils.translation import ugettext_lazy as _

from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver

from django.core import exceptions

from model_utils import *


class Institute(models.Model):
    name = models.CharField(max_length=256)
    logo = models.ImageField(blank=True, null=True)

    def __unicode__(self):
        return self.name


class Faculty(models.Model):
    name = models.CharField(max_length=256)
    institute = models.ForeignKey('Institute')

    def __unicode__(self):
        return self.name

    class Meta:
        verbose_name_plural = _("Faculties")


class StrategicObjective(models.Model):
    institute = models.ForeignKey('Institute')
    statement = models.CharField(max_length=512)

    def __unicode__(self):
        return self.statement


# Rename name to InstituteAdminUser ?
class InstituteAdmin(models.Model):
    user = models.OneToOneField(User, related_name='institute_admin')
    institute = models.ForeignKey('Institute', related_name='institute_admin')

    def __unicode__(self):
        return self.user.email


class ProjectLeader(models.Model):
    user = models.OneToOneField(User, related_name='project_leader')
    institute = models.ForeignKey('Institute')
    faculty = models.ForeignKey('Faculty')
    staff_no = models.CharField(max_length=64)
    position = models.CharField(max_length=128)

    def __unicode__(self):
        return self.user.username


class ReportingPeriod(models.Model):
    institute = models.ForeignKey('Institute', related_name='reporting_period')
    name = models.CharField(max_length=128)
    description = models.TextField()
    open_date = models.DateField(auto_now_add=True)
    close_date = models.DateField(null=True, blank=True)
    is_active = models.BooleanField(default=True, verbose_name=_('Open'))

    def __unicode__(self):
        return self.name


class FocusArea(models.Model):
    code = models.PositiveIntegerField(unique=True)
    choice = models.CharField(max_length=256)

    def __unicode__(self):
        return self.choice


class AdvisoryGroupRep(models.Model):
    code = models.PositiveIntegerField(unique=True)
    choice = models.CharField(max_length=256)


class ResearchTeamMember(models.Model):
    code = models.PositiveIntegerField(unique=True)
    choice = models.CharField(max_length=256)


class ProjectFunding(models.Model):
    funder = models.CharField(max_length=256)
    amount = models.DecimalField(decimal_places=2, max_digits=10)
    years = models.DecimalField(decimal_places=2, max_digits=5)
    renewable = models.BooleanField(choices=YESNO)


class PHDStudent(models.Model):
    name = models.CharField(max_length=128)


class ProjectOutputs(models.Model):
    code = models.PositiveIntegerField(unique=True)
    choice = models.CharField(max_length=128)\


class NewCourseDetail(models.Model):
    code = models.CharField(max_length=32)
    name = models.CharField(max_length=128)


class StudentType(models.Model):
    code = models.PositiveIntegerField(unique=True)
    choice = models.CharField(max_length=32)


class StudentParticipationNature(models.Model):
    code = models.PositiveIntegerField(unique=True)
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

    def __unicode__(self):
        return self.name

    class Meta:
        verbose_name='Project'
        verbose_name_plural='Projects'


class ProjectDetail(models.Model):
    header = models.ForeignKey(ProjectHeader, related_name='project_detail',
                               verbose_name=CAPTURE_LABELS['header'])
    project_status = models.CharField(choices=PROJECT_STATUS, max_length=1, null=True,
                                      verbose_name=CAPTURE_LABELS['project_status'])
    start_date = models.DateField(null=True,
                                  verbose_name=CAPTURE_LABELS['start_date'])
    end_date = models.DateField(null=True,
                                verbose_name=CAPTURE_LABELS['end_date'])
    faculty = models.ForeignKey('Faculty', null=True,
                                verbose_name=CAPTURE_LABELS['faculty'])
    multi_faculty = models.CharField(choices=YESNO, max_length=1, null=True,
                                     verbose_name=CAPTURE_LABELS['multi_faculty'])
    description = models.TextField(null=True,
                                   verbose_name=CAPTURE_LABELS['description'])
    focus_area = models.ManyToManyField('FocusArea',
                                        verbose_name=CAPTURE_LABELS['focus_area'],
                                        help_text=CAPTURE_HELP['focus_areas'])
    focus_area_text = models.CharField(max_length=256, null=True,
                                       verbose_name=CAPTURE_LABELS['focus_area_text'])
    classification = models.PositiveIntegerField(choices=CLASSIFICATION, null=True,
                                                 verbose_name=CAPTURE_LABELS['classification'])
    strategic_objectives = models.ManyToManyField('StrategicObjective',
                                                  verbose_name=CAPTURE_LABELS['strategic_objectives'],
                                                  help_text=CAPTURE_HELP['strategic_objectives'])
    outcomes = models.TextField(null=True,
                                verbose_name=CAPTURE_LABELS['outcomes'])
    beneficiaries = models.TextField(null=True,
                                     verbose_name=CAPTURE_LABELS['beneficiaries'])
    initiation = models.PositiveIntegerField(choices=INITIATION_STATEMENTS, null=True,
                                             verbose_name=CAPTURE_LABELS['initiation'])
    authors = models.PositiveIntegerField(choices=NUMBER_AUTHORS, null=True,
                                          verbose_name=CAPTURE_LABELS['authors'])
    amendments_permitted = models.CharField(choices=YESNO, max_length=1, null=True,
                                            verbose_name=CAPTURE_LABELS['amendments_permitted'])
    public_domain = models.CharField(choices=YESNO, max_length=1, null=True,
                                     verbose_name=CAPTURE_LABELS['public_domain'],
                                     help_text='If yes, please provide the URL')
    public_domain_url = models.URLField(null=True,
                                        verbose_name=CAPTURE_LABELS['public_domain_url'])
    adv_group = models.CharField(choices=YESNO, max_length=1, null=True,
                                 verbose_name=CAPTURE_LABELS['adv_group'])
    adv_group_rep = models.ManyToManyField('AdvisoryGroupRep',
                                           verbose_name=CAPTURE_LABELS['adv_group_rep'])
    adv_group_freq = models.PositiveIntegerField(choices=ADV_GROUP_FREQ, null=True,
                                                 verbose_name=CAPTURE_LABELS['adv_group_freq'])
    team_members = models.ManyToManyField(ResearchTeamMember,
                                          verbose_name=CAPTURE_LABELS['team_members'])
    new_initiative = models.CharField(choices=YESNO, max_length=1, null=True,
                                      verbose_name=CAPTURE_LABELS['new_initiative'])
    new_initiative_text = models.TextField(null=True,
                                           verbose_name=CAPTURE_LABELS['new_initiative_text'])
    new_initiative_party = models.PositiveIntegerField(choices=INITIATIVE_PARTIES, null=True,
                                                       verbose_name=CAPTURE_LABELS['new_initiative_party'])
    new_initiative_party_text = models.TextField(null=True,
                                                 verbose_name=CAPTURE_LABELS['new_initiative_party_text'])
    funding = models.ManyToManyField(ProjectFunding,
                                     verbose_name=CAPTURE_LABELS['funding'])
    research = models.PositiveIntegerField(choices=RESEARCH_CLASSIFICATION, null=True,
                                           verbose_name=CAPTURE_LABELS['research'])
    research_text = models.TextField(null=True,
                                     verbose_name=CAPTURE_LABELS['research_text'],
                                     help_text=CAPTURE_HELP['research_text'])
    phd_research = models.CharField(choices=YESNO, max_length=1, null=True,
                                    verbose_name=CAPTURE_LABELS['phd_research'])
    phd_research_name = models.ManyToManyField('PHDStudent',
                                               verbose_name=CAPTURE_LABELS['phd_research_name'])
    outputs = models.ManyToManyField('ProjectOutputs',
                                     verbose_name=CAPTURE_LABELS['outputs'])
    curriculum_changes = models.CharField(choices=YESNO, max_length=1, null=True,
                                          verbose_name=CAPTURE_LABELS['curriculum_changes'])
    curriculum_changes_text = models.TextField(null=True,
                                               verbose_name=CAPTURE_LABELS['curriculum_changes_text'])
    new_courses = models.CharField(choices=YESNO, max_length=1, null=True,
                                   verbose_name=CAPTURE_LABELS['new_courses'])
    new_course_detail = models.ManyToManyField('NewCourseDetail',
                                               verbose_name=CAPTURE_LABELS['new_course_detail'])
    students_involved = models.CharField(choices=YESNO, max_length=1, null=True,
                                         verbose_name=CAPTURE_LABELS['students_involved'])
    student_types = models.ManyToManyField('StudentType',
                                           verbose_name=CAPTURE_LABELS['student_types'])
    student_nature = models.ManyToManyField(StudentParticipationNature,
                                            verbose_name=CAPTURE_LABELS['student_nature'])
    student_nature_text = models.CharField(max_length=128, null=True,
                                           verbose_name=CAPTURE_LABELS['student_nature_text'])
    course_requirement = models.CharField(choices=YESNO, max_length=1, null=True,
                                          verbose_name=CAPTURE_LABELS['course_requirement'])
    course_req_detail = models.ManyToManyField('CourseReqDetail',
                                               verbose_name=CAPTURE_LABELS['course_req_detail'])
    external_collaboration = models.CharField(choices=YESNO, max_length=1, null=True,
                                              verbose_name=CAPTURE_LABELS['external_collaboration'])
    collaboration_detail = models.ManyToManyField('Collaborators',
                                                  verbose_name=CAPTURE_LABELS['collaboration_detail'])
    record_status = models.PositiveIntegerField(choices=RECORD_STATUS)
    reporting_period = models.ForeignKey('ReportingPeriod')
    # rejected = models.BooleanField(default=False)
    # rejected_detail = models.TextField(null=True)

    def __unicode__(self):
        return '%s - %s' % (self.header.name, self.reporting_period.name)

    class Meta:
        verbose_name='Project detail'
        verbose_name_plural='Project details'
        permissions = (
            ('view_projectdetail', 'Can only view project details'),
            ('reject_projectdetail', 'Can reject the project which has been submitted')
        )


@receiver(post_save, sender=InstituteAdmin)
def assign_institute_admin_to_group(sender, **kwargs):
    if kwargs['created']:
        try:
            g = Group.objects.get(name='InstituteAdmins')
        except exceptions.ObjectDoesNotExist:
            # Move this to migrations file
            g = Group.objects.create(name='InstituteAdmins')
            admin_permissions = [
                'add_projectleader', 'delete_projectleader', 'change_projectleader',
                'add_faculty', 'delete_faculty', 'change_faculty',
                'add_reportingperiod', 'change_reportingperiod', 'delete_reportingperiod',
                'change_projectdetail', 'view_projectdetail', 'reject_projectdetail'
            ]
            perms = Permission.objects.filter(codename__in=admin_permissions)
            for perm in perms:
                g.permissions.add(perm)
            g.save()

        kwargs['instance'].user.groups.add(g)


@receiver(post_delete, sender=InstituteAdmin)
def remove_institute_admin_from_group(sender, **kwargs):
    g = Group.objects.get(name='InstituteAdmin')
    kwargs['instance'].user.groups.remove(g)


@receiver(post_save, sender=ProjectLeader)
def assign_project_leader_to_group(sender, **kwargs):
    if kwargs['created']:
        try:
            g = Group.objects.get(name='ProjectLeaders')
        except exceptions.ObjectDoesNotExist:
            # Move this to migrations file
            g = Group.objects.create(name='ProjectLeaders')
            admin_permissions = [
                'add_projectheader', 'delete_projectheader', 'change_projectheader',
                'add_projectdetail', 'delete_projectdetail', 'change_projectdetail',
            ]
            perms = Permission.objects.filter(codename__in=admin_permissions)
            for perm in perms:
                g.permissions.add(perm)
            g.save()

        kwargs['instance'].user.groups.add(g)


@receiver(post_delete, sender=ProjectLeader)
def remove_institute_admin_from_group(sender, **kwargs):
    g = Group.objects.get(name='ProjectLeaders')
    kwargs['instance'].user.groups.remove(g)
