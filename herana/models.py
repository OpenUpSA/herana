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

        permissions = ()

class StrategicObjective(models.Model):
    institute = models.ForeignKey('Institute')
    statement = models.CharField(max_length=512)


# Rename name to InstituteAdminUser ?
class InstituteAdmin(models.Model):
    user = models.OneToOneField(User, related_name='institute_admin')
    institute = models.ForeignKey('Institute', related_name='institute_admin')

    def __unicode__(self):
        return self.user.email


class ProjectLeader(models.Model):
    user = models.OneToOneField(User)
    institute = models.ForeignKey('Institute')
    faculty = models.ForeignKey('Faculty')
    staff_no = models.CharField(max_length=64)
    position = models.CharField(max_length=128)


class ReportingPeriod(models.Model):
    institute = models.ForeignKey('Institute', related_name='reporting_period')
    name = models.CharField(max_length=128)
    description = models.TextField()
    open_date = models.DateField(auto_now_add=True)
    close_date = models.DateField(blank=True)
    is_active = models.BooleanField(default=True, verbose_name=_('Open'))

    def __unicode__(self):
        return self.name

    def save(self, *args, **kwargs):
        import ipdb; ipdb.set_trace()
        super(ReportingPeriod, self).save(*args, **kwargs)

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



@receiver(post_save, sender=Institute)
def create_institute_admin_group(sender, **kwargs):
    if kwargs['created']:
        group_name = "inst_%s_admin" % kwargs['instance'].id
        Group.objects.create(name=group_name)


@receiver(post_delete, sender=Institute)
def delete_institute_admin_group(sender, **kwargs):
    group_name = "inst_%s_admin" % kwargs['instance'].id
    Group.objects.get(name=group_name).delete()


@receiver(post_save, sender=InstituteAdmin)
def assign_institute_admin_to_group(sender, **kwargs):
    if kwargs['created']:
        try:
            g = Group.objects.get(name='InstituteAdmin')
        except exceptions.ObjectDoesNotExist:
            # Move this to migrations file
            g = Group.objects.create(name='InstituteAdmin')
            admin_permissions = [
                'add_projectleader', 'delete_projectleader, change_projectleader',
                'add_faculty', 'delete_faculty', 'change_faculty',
                'add_reportingperiod', 'change_reportingperiod', 'delete_reportingperiod'
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

