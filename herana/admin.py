from datetime import date
from copy import deepcopy

from django import forms
from django.contrib import admin
from django.contrib.admin.options import InlineModelAdmin
from django.utils.translation import ugettext_lazy as _
from django.forms import CheckboxSelectMultiple
from django.db import models

from django.contrib.auth import get_permission_codename
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.forms import UserCreationForm

from models import (
    Institute,
    OrgLevel1,
    OrgLevel2,
    OrgLevel3,
    ReportingPeriod,
    InstituteAdmin,
    StrategicObjective,
    ProjectLeader,
    ProjectDetail,
    ProjectFunding,
    PHDStudent,
    ProjectOutput,
    NewCourseDetail,
    CourseReqDetail,
    Collaborators,
    CustomUser,
    ResearchTeamMember
)

from forms import ProjectDetailForm, ProjectDetailAdminForm


ORG_LEVEL_FIELDS = ["org_level_1", "org_level_2", "org_level_3"]

# Disable bulk delete action across the site.
admin.site.disable_action('delete_selected')

# ------------------------------------------------------------------------------
# General utility classes and functions
# ------------------------------------------------------------------------------

class ReadOnlyMixin(InlineModelAdmin):
    def get_readonly_fields(self, request, obj=None):
        """
        If a user has a view only permission,
        add all inline form fields to readonly_fields
        """
        if user_has_perm(request, self.opts, 'view'):
            result = list(set(
                [field.name for field in self.opts.local_fields] +
                [field.name for field in self.opts.local_many_to_many]
            ))
            result.remove('id')
            return result
        return super(ReadOnlyMixin, self).get_readonly_fields(request, obj=obj)

    def has_add_permission(self, request):
        # Global admin and institute admin have view permissions assigned
        if user_has_perm(request, self.opts, 'view'):
            return False
        return True

    def has_delete_permission(self, request, obj=None):
        # Global admin and institute admin have view permissions assigned
        if user_has_perm(request, self.opts, 'view'):
            return False
        return True


def user_has_perm(request, opts, perm_type):
    """
    Return True if user has the permission to perform specific action
        param obj request: Current request object
        param obj opts: options for current ModelAdmin instance
        param str perm_type: type of permission to check for
    """
    codename = get_permission_codename(perm_type, opts)
    return request.user.has_perm("%s.%s" % (opts.app_label, codename))


def invert_flagged(obj):
    # Inverts the icon, so it makes more sense when viewing i.e.
    # Red:   Flagged
    # Green: Not Flagged
    return not obj.is_flagged

invert_flagged.boolean = True
invert_flagged.short_description = 'Good / Flagged'


def invert_deleted(obj):
    # Inverts the icon, so it makes more sense when viewing i.e.
    # Red:   Flagged
    # Green: Not Flagged
    return not obj.is_deleted

invert_deleted.boolean = True
invert_deleted.short_description = 'Active / Deleted'

def invert_rejected(obj):
    # Inverts the icon, so it makes more sense when viewing i.e.
    # Red:   Rejected
    # Green: Not rejected
    return not obj.is_rejected

invert_rejected.boolean = True
invert_rejected.short_description = 'Accepted / Rejected'

# ------------------------------------------------------------------------------
# Formsets
# ------------------------------------------------------------------------------

class InlineValidationFormSet(forms.models.BaseInlineFormSet):
    def is_valid(self):
        return super(InlineValidationFormSet, self).is_valid() and \
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


"""
The following clean methods ensure that further detail is provided
where the project leader selected "Yes" for the related formset fields.
"""

class PHDStudentFormSet(InlineValidationFormSet):
    def clean(self):
        if self.instance.phd_research == 'Y':
            error_msg = 'Please enter the PhD student\'s name.'
            super(PHDStudentFormSet, self).clean(error_msg)


class NewCourseDetailFormSet(InlineValidationFormSet):
    def clean(self):
        if self.instance.new_courses == 'Y':
            error_msg = 'Please enter the course\'s details.'
            super(NewCourseDetailFormSet, self).clean(error_msg)


class CourseReqDetailFormSet(InlineValidationFormSet):
    def clean(self):
        if self.instance.course_requirement == 'Y':
            error_msg = 'Please enter the course\'s details.'
            super(CourseReqDetailFormSet, self).clean(error_msg)


class CollaboratorsFormSet(InlineValidationFormSet):
    def clean(self):
        if self.instance.external_collaboration == 'Y':
            error_msg = 'Please enter the collaborator\'s details.'
            super(CollaboratorsFormSet, self).clean(error_msg)


class ProjectLeaderFormset(InlineValidationFormSet):
    def clean(self):
        if self.instance:
            error_msg = 'Please enter the project leader\'s details.'
            super(ProjectLeaderFormset, self).clean(error_msg)


class InstituteAdminFormSet(InlineValidationFormSet):
    def clean(self):
        """
        This is the only thing I could think of to ensure either a
        project leader or institute admin is created when the global
        admin creates a user
        If project leader details are not entered, give an error when InstituteAdmin
        is not created.
        """
        if self.instance and not self.data.get('project_leader-0-institute'):
            error_msg = 'Please enter the institute admin\'s details.'
            super(InstituteAdminFormSet, self).clean(error_msg)

# ------------------------------------------------------------------------------
# Inlines
# ------------------------------------------------------------------------------

"""
Two generic classes to be used for inlines within the ProjectDetail form.
"""
class ProjectTabularInline(admin.TabularInline):
    extra = 1
    inline_classes = ('grp-collapse grp-open',)


class ProjectStackedInline(admin.StackedInline):
    extra = 1
    inline_classes = ('grp-collapse grp-open',)


class ProjectFundingInline(ReadOnlyMixin, ProjectTabularInline):
    model = ProjectFunding
    verbose_name = _('funding source')
    verbose_name_plural = _('6.1: Please list sources of project funding, the number of years for which funding has been secured, and the amount of funding (in US$).')


class PHDStudentInline(ReadOnlyMixin, ProjectTabularInline):
    model = PHDStudent
    formset = PHDStudentFormSet
    verbose_name = _('student')
    verbose_name_plural = _('7.2.1: If yes, please provide their names.')


class ProjectOutputInline(ReadOnlyMixin, ProjectStackedInline):
    model = ProjectOutput
    verbose_name = _('Project output')
    verbose_name_plural = _('8.1: Please add the completed publications and other outputs for this project.')


class NewCourseDetailInline(ReadOnlyMixin, ProjectTabularInline):
    model = NewCourseDetail
    formset = NewCourseDetailFormSet
    verbose_name = _('new course')
    verbose_name_plural = _('9.2.1: If yes, please provide the new course details')


class CourseReqDetailInline(ReadOnlyMixin, ProjectTabularInline):
    model = CourseReqDetail
    formset = CourseReqDetailFormSet
    verbose_name = _('required course')
    verbose_name_plural = _('9.5.1: If yes, please provide the course details.')


class CollaboratorsInline(ReadOnlyMixin, ProjectTabularInline):
    model = Collaborators
    formset = CollaboratorsFormSet
    verbose_name = _('collaborator')
    verbose_name_plural = _('10.1.1: If yes, please provide the collaborator details.')


class InstituteAdminInline(admin.TabularInline):
    model = InstituteAdmin
    can_delete = False
    formset = InstituteAdminFormSet


class ProjectLeaderInline(admin.StackedInline):
    model = ProjectLeader
    can_delete = False
    inline_classes = ('grp-collapse grp-open',)
    verbose_name = _('Project Leader')
    extra = 1


class InstituteAdminProjectLeaderInline(ProjectLeaderInline):
    formset = ProjectLeaderFormset

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == 'institute':
            kwargs["queryset"] = Institute.objects.filter(
                id=request.user.get_user_institute().id)
        if db_field.name in ORG_LEVEL_FIELDS:
                kwargs["queryset"] = db_field.related_model.objects.filter(
                    institute=request.user.get_user_institute())
        return super(InstituteAdminProjectLeaderInline, self).formfield_for_foreignkey(
            db_field, request, **kwargs)


class GlobalAdminProjectLeaderInline(ProjectLeaderInline):
    """
    Only enable autocomplete for the global admin user (super user)
    due to grappelli not easily enabling limiting results.

    The select boxes are filtered by institutes for the institute admin users.
    """
    raw_id_fields = ('org_level_1', 'org_level_2', 'org_level_3')
    autocomplete_lookup_fields = {
        'fk': ['org_level_1', 'org_level_2', 'org_level_3'],
        'm2m': [],
    }

class StrategicObjectiveInline(admin.TabularInline):
    model = StrategicObjective
    inline_classes = ('grp-collapse grp-open',)
    extra = 7
    verbose_name = _('Strategic objectives of the Institute')
    verbose_name_plural = _('Strategic Objectives')


class OrgLevelInline(admin.TabularInline):
    inline_classes = ('grp-collapse grp-open',)
    extra = 2

class OrgLevel1Inline(OrgLevelInline):
    model = OrgLevel1
    verbose_name = _('Org Level 1')
    verbose_name_plural = _('Org Level 1')


class OrgLevel2Inline(OrgLevelInline):
    model = OrgLevel2
    verbose_name = _('Org Level 2')
    verbose_name_plural = _('Org Level 2')

    raw_id_fields = ('parent',)
    autocomplete_lookup_fields = {
        'fk': ['parent'],
        'm2m': [],
    }

class OrgLevel3Inline(OrgLevelInline):
    model = OrgLevel3
    verbose_name = _('Org Level 3')
    verbose_name_plural = _('Org Level 3')

    raw_id_fields = ('parent',)
    autocomplete_lookup_fields = {
        'fk': ['parent'],
        'm2m': [],
    }

# ------------------------------------------------------------------------------
# Filters
# ------------------------------------------------------------------------------

class ReportingPeriodFilter(admin.SimpleListFilter):
    title = "Reporting Period"
    parameter_name = 'reporting_period'

    def lookups(self, request, model_admin):
        reporting_periods = []
        if not request.user.is_superuser:
            reporting_periods = list(ReportingPeriod.objects.filter(
                institute=request.user.get_user_institute()))

        return [(rp.id, rp.name) for rp in reporting_periods]

    def queryset(self, request, queryset):
        if self.value():
            return queryset.filter(reporting_period=self.value())
        else:
            return queryset

class UserInstituteFilter(admin.SimpleListFilter):
    title = 'Institute'
    parameter_name = 'institute'

    def lookups(self, request,  model_admin):
        return ((i.id, i.name) for i in Institute.objects.all())

    def queryset(self, request, queryset):
        if self.value():
            filtered_user_ids = []
            for user in queryset:
                if user.get_user_institute() and user.get_user_institute().id == int(self.value()):
                    filtered_user_ids.append(user.id)
            return queryset.filter(id__in=filtered_user_ids)
        return queryset

# ------------------------------------------------------------------------------
# Custom User Admin
# ------------------------------------------------------------------------------

class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = CustomUser
        fields = ("email",)


class CustomUserAdmin(UserAdmin):
    add_form = CustomUserCreationForm

    list_display = ('email', 'first_name', 'last_name', 'is_active')

    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        (_('Personal info'), {'fields': ('first_name', 'last_name')}),
        (_('Permissions'), {'fields': ('is_active', 'is_staff', 'is_superuser',
                                       'groups', 'user_permissions')}),
        (_('Important dates'), {'fields': ('last_login', 'date_joined')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('first_name', 'last_name', 'email', 'password1', 'password2'),
        }),
    )

    search_fields = ('email', 'first_name', 'last_name')
    ordering = ('email',)

    def get_queryset(self, request):
        if not request.user.is_superuser:
            return self.model.objects.filter(
                project_leader__institute=request.user.get_user_institute())
        else:
            return super(CustomUserAdmin, self).get_queryset(request)

    def get_fieldsets(self, request, obj=None):
        fieldsets = super(CustomUserAdmin, self).get_fieldsets(request, obj=obj)
        if obj and not request.user.is_superuser:
            fieldsets = (
                (None, {'fields': ('email', 'password')}),
                (_('Personal info'), {'fields': ('first_name', 'last_name')})
            )
        return fieldsets

    def get_list_filter(self, request):
        self.list_filter = []
        if request.user.is_superuser:
            self.list_filter.extend(['groups', UserInstituteFilter])
        return super(CustomUserAdmin, self).get_list_filter(request)

    def get_inline_instances(self, request, obj=None):
        if request.user.is_superuser:
            self.inlines = [InstituteAdminInline, GlobalAdminProjectLeaderInline]
        else:
            self.inlines = [InstituteAdminProjectLeaderInline]
        return super(CustomUserAdmin, self).get_inline_instances(request)

    def save_model(self, request, obj, form, change):
        """
        This is to ensure the user gets created when Save and Email is selected.
        """
        if request.POST.get('_save_email'):
            request.POST.__setitem__('_save', 'Save')
        super(CustomUserAdmin, self).save_model(request, obj, form, change)

# ------------------------------------------------------------------------------
# ModelAdmins
# ------------------------------------------------------------------------------

class InstituteModelAdmin(admin.ModelAdmin):
    inlines = [
        StrategicObjectiveInline,
        OrgLevel1Inline,
        OrgLevel2Inline,
        OrgLevel3Inline]


class OrgLevelAdmin(admin.ModelAdmin):
    list_filter = ('institute',)


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

    def has_change_permission(self, request, obj=None):
        if not request.user.is_superuser:
            if user_has_perm(request, self.opts, 'change'):
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
    save_as = True
    list_display = ('__unicode__', 'record_status', 'reporting_period', invert_rejected)
    list_display_links = ('__unicode__',)
    form = ProjectDetailForm
    formfield_overrides = {
        models.ManyToManyField: {'widget': CheckboxSelectMultiple},
    }

    inlines = [
        ProjectFundingInline,
        PHDStudentInline,
        ProjectOutputInline,
        NewCourseDetailInline,
        CourseReqDetailInline,
        CollaboratorsInline,
    ]

    radio_fields = {
        'is_leader': admin.HORIZONTAL,
        'is_flagship': admin.HORIZONTAL,
        'project_status': admin.HORIZONTAL,
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

    fieldsets = (
        (None, {
            'fields': ('name', 'is_leader', 'is_flagship'),
            'description': ''
        }),
        (None, {
            'fields': ('org_level_1',),
            'description': '1.4 Please indicate where the project is located.'
        }),
        (None, {
            'fields': ('project_status', 'start_date', 'end_date', 'description', 'focus_area',
                'focus_area_text', 'classification'),
            'description': ''
        }),
        (None, {
            'fields': ('strategic_objectives', 'outcomes', 'beneficiaries'),
            'description': ''
        }),
        (None, {
            'fields': ('initiation', 'authors', 'amendments_permitted', 'public_domain', 'public_domain_url', 'adv_group',
                'adv_group_rep', 'adv_group_freq'),
            'description': ''
        }),
        (None, {
            'fields': ('team_members', 'team_members_text', 'new_initiative', 'new_initiative_text',
                'new_initiative_party', 'new_initiative_party_text'),
            'description': ''
        }),
        (None, {
            'fields': ('research', 'research_text', 'phd_research'),
            'description': ''
        }),
        (None, {
            'fields': ('curriculum_changes', 'curriculum_changes_text', 'new_courses', 'students_involved', 'student_types',
                'student_nature', 'student_nature_text'),
            'description': ''
        }),
        (None, {
            'fields': ('course_requirement', 'external_collaboration'),
            'description': ''
        }),
        # Placeholder for admin user fields displyed in readonly view
        (None, {
            'fields': (),
            'description': ''
        }),
    )

    class Media:
        js = ('javascript/app.js',)

    def has_add_permission(self, request, obj=None):
        if request.user.is_proj_leader:
            if request.user.get_user_institute().has_active_reporting_period:
                return True
        return False

    def has_change_permission(self, request, obj=None):
        # Project leaders cannot make changes to projects if no reporting period is active.
        if request.user.is_proj_leader:
            if not request.user.get_user_institute().has_active_reporting_period:
                return False
        return True

    def has_delete_permission(self, request, obj=None):
        return False

    def get_list_display(self, request):
        """
        Only show is_flagged field to admin users
        """
        if request.user.is_institute_admin or request.user.is_superuser:
            list_display = self.list_display + (invert_flagged, invert_deleted)
            return list_display
        return self.list_display

    def get_list_filter(self, request):
        self.list_filter = []
        if request.user.is_superuser:
            self.list_filter.append('institute')
        else:
            self.list_filter.append(ReportingPeriodFilter)
        return super(ProjectDetailAdmin, self).get_list_filter(request)

    def get_queryset(self, request):
        if not request.user.is_superuser:
            qs = self.model.objects.filter(is_deleted=False)
            if request.user.is_institute_admin:
                return qs \
                    .filter(proj_leader__institute=request.user.get_user_institute()) \
                    .exclude(record_status=1) # Don't include draft records
            if request.user.is_proj_leader:
                return qs.filter(proj_leader=request.user.project_leader)
        return super(ProjectDetailAdmin, self).get_queryset(request)

    def get_readonly_fields(self, request, obj=None):
        if user_has_perm(request, self.opts, 'view'):
            readonly_fields = []
            for field in self.form.base_fields.keys():
                # Don't display fields which should be excluded
                if field not in self.form.Meta.exclude:
                    if field not in self.form.Meta.admin_editable:
                        readonly_fields.append(field)
            return readonly_fields
        return super(ProjectDetailAdmin, self).get_readonly_fields(request, obj=obj)

    def get_form(self, request, obj=None, **kwargs):
        # Global and institute admin have readonly views and are able to reject or flag a project
        if request.user.is_institute_admin or request.user.is_superuser:
            self.form = ProjectDetailAdminForm
        else:
            self.form = ProjectDetailForm
        return super(ProjectDetailAdmin, self).get_form(request, obj=obj, **kwargs)

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name in ORG_LEVEL_FIELDS:
            kwargs["queryset"] = db_field.related_model.objects.filter(
                institute=request.user.get_user_institute())
        return super(ProjectDetailAdmin, self).formfield_for_foreignkey(
            db_field, request, **kwargs)

    def formfield_for_manytomany(self, db_field, request, **kwargs):
        if db_field.name == "strategic_objectives":
            kwargs["queryset"] = StrategicObjective.objects.filter(
                institute=request.user.get_user_institute())
        return super(ProjectDetailAdmin, self).formfield_for_manytomany(
            db_field, request, **kwargs)

    def get_fieldsets(self, request, obj=None):
        fieldsets = deepcopy(super(ProjectDetailAdmin, self).get_fieldsets(request, obj=obj))
        if not request.user.is_superuser:
            # Org levels may vary.
            # Only include levels which have been set up.
            institute = request.user.get_user_institute()
            org_level_fields = []
            for field in ORG_LEVEL_FIELDS:
                if getattr(institute, '%s_name' % field):
                    org_level_fields.append(field)
            fieldsets[1][1]['fields'] = tuple(org_level_fields)

        if user_has_perm(request, self.opts, 'view'):
            # add the fiedls to the empty fieldset
            # Global + institute admin
            fieldsets[-1][1]['fields'] = ('is_rejected', 'rejected_detail', 'is_flagged')
        return fieldsets

    def render_change_form(self, request, context, add=False, change=False, form_url='', obj=None):
        form = context['adminform'].form
        if form.fields.get('org_level_1', False):
            if add:
                institute = request.user.get_user_institute()
            elif change:
                institute = obj.institute

            for field in ORG_LEVEL_FIELDS:
                level_name = getattr(institute, '%s_name' % field)
                if level_name != '':
                    # If level_name is empty, formset doesn't have the fields included
                    # See get_fieldsets() above
                    form.fields[field].label = level_name

        return super(ProjectDetailAdmin, self).render_change_form(
            request, context, add=False, change=False, form_url='', obj=obj)

    def save_model(self, request, obj, form, change):
        """
        This assumes that only one reporting period can be active at a time
        for a given Institute.
        RECORD_STATUS:
            1: Draft -> _draft
            2: Final -> _save
        """
        if request.user.is_superuser:
            institute = obj.institute
        else:
            institute = request.user.get_user_institute()

        reporting_period = institute.reporting_period.filter(is_active=True).first()
        if reporting_period:
            if not change:
                # New project being saved
                obj.reporting_period = reporting_period
                if request.POST.get('_draft'):
                    obj.record_status = 1
                else:
                    obj.record_status = 2
                obj.institute = request.user.get_user_institute()
                obj.proj_leader = request.user.project_leader

            else:
                if request.POST.get('_delete'):
                    # mark object as deleted
                    obj.is_deleted = True

                if request.POST.get('_draft'):
                    # Updating an old draft in a new reporting period
                    if obj.reporting_period != reporting_period:
                        obj.reporting_period = reporting_period

                elif request.POST.get('_save'):
                    # For project leaders:
                    #  - If draft project is being submitted as final: update record status
                    #  - Update reporting period if we're in a new reporting period:
                    if request.user.is_proj_leader:
                        if obj.record_status == 1:
                            obj.record_status = 2
                            if obj.reporting_period != reporting_period:
                                obj.reporting_period = reporting_period

                elif request.POST.get('_saveasnew'):
                    # Create a copy of the object if a final object is being saved,
                    # as a copy in a new reporting period
                    if obj.reporting_period != reporting_period:
                        obj.reporting_period = reporting_period

        # Flag as suspect if other academics is the only chosen team member
        # 7: Other academics
        other_academics = ResearchTeamMember.objects.get(id=7)
        if form.cleaned_data.get('team_members'):
            if other_academics in form.cleaned_data.get('team_members') and len(form.cleaned_data.get('team_members')) == 1:
                obj.is_flagged = True

        super(ProjectDetailAdmin, self).save_model(request, obj, form, change)


admin.site.register(Institute, InstituteModelAdmin)
admin.site.register(OrgLevel1, OrgLevelAdmin)
admin.site.register(OrgLevel2, OrgLevelAdmin)
admin.site.register(OrgLevel3, OrgLevelAdmin)
admin.site.register(ReportingPeriod, ReportingPeriodAdmin)
admin.site.register(ProjectDetail, ProjectDetailAdmin)
admin.site.register(CustomUser, CustomUserAdmin)
