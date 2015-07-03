from datetime import date

from django import forms
from django.contrib import admin
from django.core.exceptions import ObjectDoesNotExist
from django.utils.translation import ugettext_lazy as _
from django.forms import CheckboxSelectMultiple
from django.db import models

from django.contrib.auth import get_permission_codename
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User, Group

from guardian import shortcuts
from guardian.admin import GuardedModelAdmin

from models import (
    Institute,
    Faculty,
    ReportingPeriod,
    InstituteAdmin,
    StrategicObjective,
    ProjectLeader,
    ProjectDetail,
    FocusArea,
    ProjectFunding,
    PHDStudent,
    NewCourseDetail,
    CourseReqDetail,
    Collaborators
)

from forms import ProjectDetailForm

# ------------------------------------------------------------------------------
# General utility functions
# ------------------------------------------------------------------------------

def user_has_perm(request, opts, perm_type):
    """
    Return True if user has the permission to perform specific action
        param obj request: Current request object
        param obj opts: options for current ModelAdmin instance
        param str perm_type: type of permission to check for
    """
    codename = get_permission_codename(perm_type, opts)
    return request.user.has_perm("%s.%s" % (opts.app_label, codename))

def get_user_institute(user):
    """
    Return the institute to which the user belongs
    """
    try:
        if user.project_leader:
            return user.project_leader.institute
    except ObjectDoesNotExist:
        return user.institute_admin.institute

# ------------------------------------------------------------------------------
# Formsets
# ------------------------------------------------------------------------------

class ProjectDetailFormSet(forms.models.BaseInlineFormSet):
    def is_valid(self):
        return super(ProjectDetailFormSet, self).is_valid() and \
                    not any([bool(e) for e in self.errors])

    def clean(self, error_msg):
        count = 0
        for form in self.forms:
            try:
                if form.cleaned_data and not form.cleaned_data.get('DELETE', False):
                    count += 1
            except AttributeError:
                # annoyingly, if a subform is invalid Django explicity raises
                # an AttributeError for cleaned_data
                pass
        if count < 1:
            raise forms.ValidationError(error_msg)


class PHDStudentFormSet(ProjectDetailFormSet):
    def clean(self):
        if self.instance.phd_research == 'Y':
            error_msg = 'Please enter the PhD student\'s name.'
            super(PHDStudentFormSet, self).clean(error_msg)


class NewCourseDetailFormSet(ProjectDetailFormSet):
    def clean(self):
        if self.instance.new_courses == 'Y':
            error_msg = 'Please enter the course\'s details.'
            super(NewCourseDetailFormSet, self).clean(error_msg)


class CourseReqDetailFormSet(ProjectDetailFormSet):
    def clean(self):
        if self.instance.course_requirement == 'Y':
            error_msg = 'Please enter the course\'s details.'
            super(CourseReqDetailFormSet, self).clean(error_msg)


class CollaboratorsFormSet(ProjectDetailFormSet):
    def clean(self):
        if self.instance.external_collaboration == 'Y':
            error_msg = 'Please enter the collaborator\'s details.'
            super(CollaboratorsFormSet, self).clean(error_msg)


# ------------------------------------------------------------------------------
# Inlines
# ------------------------------------------------------------------------------

class ProjectFundingInline(admin.TabularInline):
    model = ProjectFunding
    extra = 1
    inline_classes = ('grp-collapse grp-open',)
    verbose_name = _('funding source')
    verbose_name_plural = _('Please list sources of project funding, the number of years for which funding has been secured, and the amount of funding (in US$).')


class PHDStudentInline(admin.TabularInline):
    model = PHDStudent
    formset = PHDStudentFormSet
    extra = 1
    inline_classes = ('grp-collapse grp-open',)
    verbose_name = _('student')
    verbose_name_plural = _('If yes, please provide their names.')


class NewCourseDetailInline(admin.TabularInline):
    model = NewCourseDetail
    # formset = NewCourseDetailFormSet
    extra = 1
    inline_classes = ('grp-collapse grp-open',)
    verbose_name = _('new course')
    verbose_name_plural = _('If yes, please provide the new course details')


class CourseReqDetailInline(admin.TabularInline):
    model = CourseReqDetail
    formset = CourseReqDetailFormSet
    extra = 1
    inline_classes = ('grp-collapse grp-open',)
    verbose_name = _('required course')
    verbose_name_plural = _('If yes, please provide the course details.')


class CollaboratorsInline(admin.TabularInline):
    model = Collaborators
    formset = CollaboratorsFormSet
    extra = 1
    inline_classes = ('grp-collapse grp-open',)
    verbose_name = _('collaborator')
    verbose_name_plural = _('If yes, please provide the collaborator details.')


class InstituteAdminInline(admin.TabularInline):
    model = InstituteAdmin
    can_delete = False


class StrategicObjectiveInline(admin.TabularInline):
    model = StrategicObjective
    inline_classes = ('grp-collapse grp-open',)
    extra = 7
    verbose_name = _('Strategic objectives of the Institute')
    verbose_name_plural = _('Strategic Objectives')


# ------------------------------------------------------------------------------
# Filters
# ------------------------------------------------------------------------------

class ReportingPeriodFilter(admin.SimpleListFilter):
    title = "Reporting Period"
    parameter_name = 'reporting_period'

    def lookups(self, request, model_admin):
        reporting_periods = list(ReportingPeriod.objects.filter(
            institute=get_user_institute(request.user)))

        return [(rp.id, rp.name) for rp in reporting_periods]

    def queryset(self, request, queryset):
        if self.value():
            return queryset.filter(reporting_period=self.value())
        else:
            return queryset


# ------------------------------------------------------------------------------
# ModelAdmins
# ------------------------------------------------------------------------------

class InstitutionAdmin(admin.ModelAdmin):
    inlines = [StrategicObjectiveInline]


class InstituteAdminUserAdmin(UserAdmin):
    inlines = [InstituteAdminInline]
    list_display = ('username', 'email', 'first_name', 'last_name', 'is_staff')

    def has_module_permission(self, request):
        if request.user.is_superuser:
            return True
        return False


class FacultyAdmin(admin.ModelAdmin):
    fields = ('name',)

    def save_model(self, request, obj, form, change):
        obj.institute = request.user.institute_admin.institute
        obj.save()

    def has_change_permission(self, request, obj=None):
        if not request.user.is_superuser:
            if obj:
                if request.user.institute_admin.institute == obj.institute:
                    return True
                return False

            opts = self.opts
            codename = get_permission_codename('change', opts)
            return request.user.has_perm("%s.%s" % (opts.app_label, codename))

        return True

    def has_delete_permission(self, request, obj=None):
        if not request.user.is_superuser:
            if obj:
                if request.user.institute_admin.institute == obj.institute:
                    return True
                return False
            # Should faculties be deleted by InstituteAdmins?

            opts = self.opts
            codename = get_permission_codename('change', opts)
            return request.user.has_perm("%s.%s" % (opts.app_label, codename))

        return True

    def get_queryset(self, request):
        if request.user.is_superuser:
            return super(FacultyAdmin, self).get_queryset(request)
        return self.model.objects.filter(institute=get_user_institute(request.user))


class ReportingPeriodAdmin(admin.ModelAdmin):
    fields = ('name', 'description', 'is_active', 'open_date', 'close_date')
    readonly_fields = ('open_date', 'close_date')
    list_display = ('name', 'description', 'open_date', 'close_date', 'is_active')

    # actions = ['close_reporting_period']

    def get_queryset(self, request):
        return self.model.objects\
                .filter(institute=request.user.institute_admin.institute)

    def has_add_permission(self, request, obj=None):
        # Can only be added if all existing reporting periods are closed.
        if not request.user.is_superuser:
            if user_has_perm(request, self.opts, 'add'):
                institute = request.user.institute_admin.institute
                if self.model.objects\
                                .filter(institute=institute)\
                                .filter(is_active=True):
                    return False
                return True
        return False

    def save_model(self, request, obj, form, change):
        if not change:
            obj.institute = request.user.institute_admin.institute
            obj.save()
        else:
            if obj.is_active == False:
                obj.close_date = date.today()
                obj.save()

    def get_readonly_fields(self, request, obj=None):
        if obj and obj.is_active == False:
            return self.readonly_fields + ('is_active',)
        return self.readonly_fields


class ProjectDetailAdmin(admin.ModelAdmin):
    list_display = ('__unicode__', 'record_status',)
    list_filter = (ReportingPeriodFilter, 'record_status')
    form = ProjectDetailForm
    # save_as = True
    formfield_overrides = {
        models.ManyToManyField: {'widget': CheckboxSelectMultiple},
    }

    inlines = [
        ProjectFundingInline,
        PHDStudentInline,
        NewCourseDetailInline,
        CourseReqDetailInline,
        CollaboratorsInline,
    ]

    radio_fields = {
        'is_leader': admin.HORIZONTAL,
        'is_flagship': admin.HORIZONTAL,
        'project_status': admin.HORIZONTAL,
        'multi_faculty': admin.HORIZONTAL,
        'classification': admin.VERTICAL,
        'initiation': admin.VERTICAL,
        'authors': admin.HORIZONTAL,
        'amendments_permitted': admin.HORIZONTAL,
        'public_domain': admin.HORIZONTAL,
        'adv_group': admin.HORIZONTAL,
        'adv_group_freq': admin.VERTICAL,
        'new_initiative': admin.HORIZONTAL,
        'new_initiative_party': admin.VERTICAL,
        'research': admin.VERTICAL,
        'phd_research': admin.HORIZONTAL,
        'curriculum_changes': admin.HORIZONTAL,
        'new_courses': admin.HORIZONTAL,
        'students_involved': admin.HORIZONTAL,
        'course_requirement': admin.HORIZONTAL,
        'external_collaboration': admin.HORIZONTAL
    }

    class Media:
        js = ('javascript/app.js',)

    def has_add_permission(self, request, obj=None):
        if not request.user.is_superuser:
            if user_has_perm(request, self.opts, 'add'):
                # Can only add if a reporting period is open
                institute = request.user.project_leader.institute
                if ReportingPeriod.objects\
                            .filter(institute=institute)\
                            .filter(is_active=True):
                    return True
        return False

    def has_change_permission(self, request, obj=None):
        if not request.user.is_superuser:
            if user_has_perm(request, self.opts, 'change'):
                return True
            if user_has_perm(request, self.opts, 'view'):
                return True
        return False

    def get_queryset(self, request):
        qs = self.model.objects\
                .filter(proj_leader__institute=get_user_institute(request.user))
        if user_has_perm(request, self.opts, 'view'):
            # Don't include draft records
            return qs.exclude(record_status=1)
        if user_has_perm(request, self.opts, 'change'):
            return qs

    def get_readonly_fields(self, request, obj=None):
        # For users with view access, all fields are readonly
        if user_has_perm(request, self.opts, 'view'):
            readonly_fields = []
            for field in self.form.base_fields.keys():
                if field not in self.form.Meta.exclude:
                    readonly_fields.append(field)
            return readonly_fields
        return self.readonly_fields

    def save_model(self, request, obj, form, change):
        # This assumes that only one reporting period can be active at a time
        # for a given Institute.
        institute = get_user_institute(request.user)
        reporting_period = institute.reporting_period.get(is_active=True)
        if not change:
            obj.reporting_period = reporting_period
            if request.POST['_draft']:
                obj.record_status = 1
            else:
                obj.record_status = 2
        obj.proj_leader = request.user.project_leader
        obj.save()

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == "faculty":
            kwargs["queryset"] = Faculty.objects.filter(
                institute=get_user_institute(request.user))
        return super(ProjectDetailAdmin, self).formfield_for_foreignkey(
            db_field, request, **kwargs)

    def formfield_for_manytomany(self, db_field, request, **kwargs):
        if db_field.name == "strategic_objectives":
            kwargs["queryset"] = StrategicObjective.objects.filter(
                institute=get_user_institute(request.user))
        return super(ProjectDetailAdmin, self).formfield_for_manytomany(
            db_field, request, **kwargs)


admin.site.register(Institute, InstitutionAdmin)
admin.site.register(Faculty, FacultyAdmin)
admin.site.register(ReportingPeriod, ReportingPeriodAdmin)
admin.site.register(InstituteAdmin)
admin.site.register(ProjectLeader)
admin.site.register(ProjectDetail, ProjectDetailAdmin)

admin.site.unregister(User)
admin.site.register(User, InstituteAdminUserAdmin)
