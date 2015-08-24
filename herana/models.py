import os
from datetime import datetime

from django.db import models
from django.contrib.auth.models import Group, Permission
from django.utils.translation import ugettext_lazy as _
from django.db.models.signals import post_save, post_delete, pre_save
from django.dispatch import receiver
from django.core import exceptions
from django.conf import settings

from django.utils import timezone

from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin

from model_utils import *  # noqa


# ------------------------------------------------------------------------------
# General utilities
# ------------------------------------------------------------------------------

def image_filename(instance, filename):
    """ Make S3 image filenames
    """
    return 'images/%s/%s' % (instance.id, os.path.basename(filename))

def attachment_filename(instance, filename):
    """ Make S3 attachment filenames relative to the engagement project,
    this may be modified to ensure it's unique by the storage system. """
    return 'attachments/%s/%s' % (instance.project.id, os.path.basename(filename))

# ------------------------------------------------------------------------------
# Models for administration of an institute
# ------------------------------------------------------------------------------

class Institute(models.Model):
    name = models.CharField(max_length=256)
    logo = models.ImageField(upload_to=image_filename, blank=True, null=True)

    def __unicode__(self):
        return self.name

    class Meta:
        ordering = ['name']


class StrategicObjective(models.Model):
    institute = models.ForeignKey('Institute')
    statement = models.CharField(max_length=512)

    def __unicode__(self):
        return self.statement


class OrgLevel(models.Model):
    name = models.CharField(max_length=256)
    institute = models.ForeignKey('Institute')

    def __unicode__(self):
        return self.name

    class Meta:
        verbose_name = _('Organisational level')
        verbose_name_plural = _("Organisational Levels")
        ordering = ['name']


class OrgLevel1(OrgLevel):

    class Meta:
        verbose_name = _('Organisational Level 1 Node')
        verbose_name_plural = _('Organisational Level 1 Nodes')


class OrgLevel2(OrgLevel):
    parent = models.ForeignKey('OrgLevel1')

    class Meta:
        verbose_name = _('Organisational Level 2 Node')
        verbose_name_plural = _('Organisational Level 2 Nodes')


class OrgLevel3(OrgLevel):
    parent = models.ForeignKey('OrgLevel2')

    class Meta:
        verbose_name = _('Organisational Level 3 Node')
        verbose_name_plural = _('Organisational Level 3 Nodes')


class ReportingPeriod(models.Model):
    institute = models.ForeignKey('Institute', related_name='reporting_period')
    name = models.CharField(max_length=128)
    description = models.TextField()
    open_date = models.DateField(auto_now_add=True)
    close_date = models.DateField(null=True, blank=True)
    is_active = models.BooleanField(default=True, verbose_name=_('Open'))

    def __unicode__(self):
        return self.name


# ------------------------------------------------------------------------------
# Models for users
# ------------------------------------------------------------------------------

# Rename name to InstituteAdminUser ?
class InstituteAdmin(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, related_name='institute_admin')
    institute = models.ForeignKey('Institute', related_name='institute_admin')

    def __unicode__(self):
        return self.user.email


class ProjectLeader(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, related_name='project_leader')
    institute = models.ForeignKey('Institute')
    org_level_1 = models.ForeignKey('OrgLevel1')
    org_level_2 = models.ForeignKey('OrgLevel2', null=True, blank=True)
    org_level_3 = models.ForeignKey('OrgLevel3', null=True, blank=True)
    staff_no = models.CharField(max_length=64)
    position = models.CharField(max_length=128)

    def __unicode__(self):
        return self.user.email


# ------------------------------------------------------------------------------
# Models for questionnaire many-to-many keys
# ------------------------------------------------------------------------------

class FocusArea(models.Model):
    code = models.PositiveIntegerField(unique=True)
    choice = models.CharField(max_length=256)

    def __unicode__(self):
        return self.choice


class AdvisoryGroupRep(models.Model):
    code = models.PositiveIntegerField(unique=True)
    choice = models.CharField(max_length=256)

    def __unicode__(self):
        return self.choice


class ResearchTeamMember(models.Model):
    code = models.PositiveIntegerField(unique=True)
    choice = models.CharField(max_length=256)

    def __unicode__(self):
        return self.choice


class StudentType(models.Model):
    code = models.PositiveIntegerField(unique=True)
    choice = models.CharField(max_length=32)

    def __unicode__(self):
        return self.choice


class StudentParticipationNature(models.Model):
    code = models.PositiveIntegerField(unique=True)
    choice = models.CharField(max_length=128)

    def __unicode__(self):
        return self.choice


class ProjectOutputType(models.Model):
    code = models.PositiveIntegerField(unique=True)
    choice = models.CharField(max_length=128)

    def __unicode__(self):
        return self.choice


# ------------------------------------------------------------------------------
# Models for questionnaire inlines
# ------------------------------------------------------------------------------

class ProjectFunding(models.Model):
    funder = models.CharField(max_length=256)
    amount = models.DecimalField(decimal_places=2, max_digits=10)
    years = models.DecimalField(decimal_places=2, max_digits=5)
    renewable = models.CharField(choices=YESNO, max_length=1, null=True)
    project = models.ForeignKey('ProjectDetail')


class PHDStudent(models.Model):
    name = models.CharField(max_length=128)
    project = models.ForeignKey('ProjectDetail')


class ProjectOutput(models.Model):
    project = models.ForeignKey('ProjectDetail')
    type = models.ForeignKey('ProjectOutputType',
                             verbose_name=PROJECT_OUTPUT_LABELS['type'])
    output_title = models.CharField(max_length=255, null=True, blank=True,
                                    verbose_name=PROJECT_OUTPUT_LABELS['output_title'])
    pub_title = models.CharField(max_length=255, null=True, blank=True,
                                 verbose_name=PROJECT_OUTPUT_LABELS['pub_title'])
    url = models.URLField(null=True, blank=True,
                          verbose_name=PROJECT_OUTPUT_LABELS['url'])
    doi = models.CharField(max_length=128, null=True, blank=True,
                           verbose_name=PROJECT_OUTPUT_LABELS['doi'])
    attachment = models.FileField(upload_to=attachment_filename, null=True, blank=True,
                                  verbose_name=PROJECT_OUTPUT_LABELS['attachment'])


class NewCourseDetail(models.Model):
    code = models.CharField(max_length=32)
    name = models.CharField(max_length=128)
    project = models.ForeignKey('ProjectDetail')


class CourseReqDetail(models.Model):
    code = models.CharField(max_length=32)
    name = models.CharField(max_length=128)
    project = models.ForeignKey('ProjectDetail')


class Collaborators(models.Model):
    name = models.CharField(max_length=128)
    university = models.CharField(max_length=128)
    project = models.ForeignKey('ProjectDetail')


class ProjectDetail(models.Model):
    name = models.CharField(max_length=512,
                            verbose_name=CAPTURE_LABELS['name'])
    proj_leader = models.ForeignKey('ProjectLeader')
    institute = models.ForeignKey('Institute')
    org_level_1 = models.ForeignKey('OrgLevel1')
    org_level_2 = models.ForeignKey('OrgLevel2', null=True, blank=True)
    org_level_3 = models.ForeignKey('OrgLevel3', null=True, blank=True)
    is_leader = models.CharField(choices=YESNO, max_length=1, null=True,
                                 verbose_name=CAPTURE_LABELS['is_leader'])
    is_flagship = models.CharField(choices=YESNO, max_length=1, null=True,
                                   verbose_name=CAPTURE_LABELS['is_flagship'])
    project_status = models.PositiveIntegerField(choices=PROJECT_STATUS, null=True,
                                                 verbose_name=CAPTURE_LABELS['project_status'])
    start_date = models.DateField(null=True,
                                  verbose_name=CAPTURE_LABELS['start_date'])
    end_date = models.DateField(null=True, blank=True,
                                verbose_name=CAPTURE_LABELS['end_date'])
    multi_faculty = models.CharField(choices=YESNO, max_length=1, null=True,
                                     verbose_name=CAPTURE_LABELS['multi_faculty'])
    description = models.TextField(null=True,
                                   verbose_name=CAPTURE_LABELS['description'])
    focus_area = models.ManyToManyField('FocusArea',
                                        verbose_name=CAPTURE_LABELS['focus_area'],
                                        help_text=CAPTURE_HELP['focus_areas'])
    focus_area_text = models.CharField(max_length=256, null=True, blank=True,
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
    public_domain_url = models.URLField(null=True, blank=True,
                                        verbose_name=CAPTURE_LABELS['public_domain_url'])
    adv_group = models.CharField(choices=YESNO, max_length=1, null=True,
                                 verbose_name=CAPTURE_LABELS['adv_group'])
    adv_group_rep = models.ManyToManyField('AdvisoryGroupRep', blank=True,
                                           verbose_name=CAPTURE_LABELS['adv_group_rep'])
    adv_group_freq = models.PositiveIntegerField(choices=ADV_GROUP_FREQ, null=True, default=None, blank=True,
                                                 verbose_name=CAPTURE_LABELS['adv_group_freq'])
    team_members = models.ManyToManyField(ResearchTeamMember, blank=True,
                                          verbose_name=CAPTURE_LABELS['team_members'])
    team_members_text = models.TextField(null=True, blank=True,
                                        verbose_name=CAPTURE_LABELS['team_members_text'])
    new_initiative = models.CharField(choices=YESNO, max_length=1, null=True,
                                      verbose_name=CAPTURE_LABELS['new_initiative'])
    new_initiative_text = models.TextField(null=True, blank=True,
                                           verbose_name=CAPTURE_LABELS['new_initiative_text'])
    new_initiative_party = models.PositiveIntegerField(choices=INITIATIVE_PARTIES, default=None, null=True, blank=True,
                                                       verbose_name=CAPTURE_LABELS['new_initiative_party'])
    new_initiative_party_text = models.TextField(null=True, blank=True,
                                                 verbose_name=CAPTURE_LABELS['new_initiative_party_text'])
    research = models.PositiveIntegerField(choices=RESEARCH_CLASSIFICATION, null=True,
                                           verbose_name=CAPTURE_LABELS['research'])
    research_text = models.TextField(null=True, blank=True,
                                     verbose_name=CAPTURE_LABELS['research_text'],
                                     help_text=CAPTURE_HELP['research_text'])
    phd_research = models.CharField(choices=YESNO, max_length=1, null=True,
                                    verbose_name=CAPTURE_LABELS['phd_research'])
    curriculum_changes = models.CharField(choices=YESNO, max_length=1, null=True,
                                          verbose_name=CAPTURE_LABELS['curriculum_changes'])
    curriculum_changes_text = models.TextField(null=True, blank=True,
                                               verbose_name=CAPTURE_LABELS['curriculum_changes_text'])
    new_courses = models.CharField(choices=YESNO, max_length=1, null=True,
                                   verbose_name=CAPTURE_LABELS['new_courses'])
    students_involved = models.CharField(choices=YESNO, max_length=1, null=True,
                                         verbose_name=CAPTURE_LABELS['students_involved'])
    student_types = models.ManyToManyField('StudentType', blank=True,
                                           verbose_name=CAPTURE_LABELS['student_types'])
    student_nature = models.ManyToManyField('StudentParticipationNature',
                                            verbose_name=CAPTURE_LABELS['student_nature'],
                                            blank=True)
    student_nature_text = models.CharField(max_length=128, null=True, blank=True,
                                           verbose_name=CAPTURE_LABELS['student_nature_text'])
    course_requirement = models.CharField(choices=YESNO, max_length=1, null=True,
                                          verbose_name=CAPTURE_LABELS['course_requirement'])
    external_collaboration = models.CharField(choices=YESNO, max_length=1, null=True,
                                              verbose_name=CAPTURE_LABELS['external_collaboration'])
    record_status = models.PositiveIntegerField(choices=RECORD_STATUS)
    reporting_period = models.ForeignKey('ReportingPeriod')
    is_rejected = models.BooleanField(default=False, verbose_name=CAPTURE_LABELS['is_rejected'])
    rejected_detail = models.TextField(null=True, blank=True)
    is_flagged = models.BooleanField(default=False, verbose_name=CAPTURE_LABELS['is_flagged'])
    is_deleted = models.BooleanField(default=False)
    created_at = models.DateField(auto_now_add=True)

    def __unicode__(self):
        return '%s - %s' % (self.name, self.reporting_period.name)

    class Meta:
        verbose_name='Engagement project'
        verbose_name_plural='Engagement projects'
        permissions = (
            ('view_projectdetail', 'Can only view project details'),
            ('reject_projectdetail', 'Can reject the project which has been submitted')
        )

# ------------------------------------------------------------------------------
# Custom User
# ------------------------------------------------------------------------------

class CustomUserManager(BaseUserManager):
    def _create_user(self, email, password,
                     is_staff, is_superuser, **extra_fields):
        """
        Creates and saves a User with the given username, email and password.
        """
        now = timezone.now()
        if not email:
            raise ValueError('The given email must be set')
        email = self.normalize_email(email)
        user = self.model(email=email,
                          is_staff=is_staff, is_active=True,
                          is_superuser=is_superuser,
                          date_joined=now, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email, password=None, **extra_fields):
        return self._create_user(email, password, False, False,
                                 **extra_fields)

    def create_superuser(self, email, password, **extra_fields):
        return self._create_user(email, password, True, True,
                                 **extra_fields)


class CustomUser(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(unique=True)

    first_name = models.CharField(_('first name'), max_length=30, blank=True)
    last_name = models.CharField(_('last name'), max_length=30, blank=True)
    is_staff = models.BooleanField(_('staff status'), default=False,
        help_text=_('Designates whether the user can log into this admin '
                    'site.'))
    is_active = models.BooleanField(_('active'), default=True,
        help_text=_('Designates whether this user should be treated as '
                    'active. Unselect this instead of deleting accounts.'))
    date_joined = models.DateTimeField(_('date joined'), default=timezone.now)


    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    def get_full_name(self):
        """
        Returns the first_name plus the last_name, with a space in between.
        """
        full_name = '%s %s' % (self.first_name, self.last_name)
        return full_name.strip()

    def get_short_name(self):
        "Returns the short name for the user."
        return self.first_name

    def email_user(self, subject, message, from_email=None, **kwargs):
        """
        Sends an email to this User.
        """
        send_mail(subject, message, from_email, [self.email], **kwargs)

    def is_institute_admin(self):
        try:
            g = Group.objects.get(name='InstituteAdmins')
        except ObjectDoesNotExist:
            return False
        if g in self.groups.all():
            return True
        return False

    objects = CustomUserManager()

    class Meta:
        verbose_name = 'User'


# ------------------------------------------------------------------------------
# Model signals
# ------------------------------------------------------------------------------

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
                'add_orglevel1', 'delete_orglevel1', 'change_orglevel1',
                'add_orglevel2', 'delete_orglevel2', 'change_orglevel2',
                'add_orglevel3', 'delete_orglevel3', 'change_orglevel3',
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
    g = Group.objects.get(name='InstituteAdmins')
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
                'add_projectdetail', 'change_projectdetail',
                'add_projectfunding', 'delete_projectfunding', 'change_projectfunding',
                'add_phdstudent', 'delete_phdstudent', 'change_phdstudent',
                'add_newcoursedetail', 'delete_newcoursedetail', 'change_newcoursedetail',
                'add_coursereqdetail', 'delete_coursereqdetail', 'change_coursereqdetail',
                'add_collaborators', 'delete_collaborators', 'change_collaborators',
                'add_projectoutput', 'delete_projectoutput', 'change_projectoutput'
            ]
            perms = Permission.objects.filter(codename__in=admin_permissions)
            for perm in perms:
                g.permissions.add(perm)
            g.save()
        kwargs['instance'].user.groups.add(g)


@receiver(post_delete, sender=ProjectLeader)
def remove_user_from_project_leaders(sender, **kwargs):
    g = Group.objects.get(name='ProjectLeaders')
    kwargs['instance'].user.groups.remove(g)


@receiver(pre_save, sender=settings.AUTH_USER_MODEL)
def set_user_as_staff(sender, instance, **kwargs):
    if not instance.is_staff:
        instance.is_staff = True
