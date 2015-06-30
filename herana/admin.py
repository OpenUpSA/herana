from datetime import date

from django.core.exceptions import ObjectDoesNotExist
from django.utils.translation import ugettext_lazy as _
from django.contrib import admin

from django.contrib.auth import get_permission_codename
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User, Group

from guardian import shortcuts
from guardian.admin import GuardedModelAdmin

import models
from forms import ProjectDetailForm


def user_has_perm(request, opts, perm_type):
    """
    Return True if user has the permission to perform specific action
        param obj request: Current request object
        param obj opts: options for current ModelAdmin instance
        param str perm_type: type of permission to check for
    """
    codename = get_permission_codename(perm_type, opts)
    return request.user.has_perm("%s.%s" % (opts.app_label, codename))

def get_user_institute(request):
    """
    Return the institute to which the user belongs
    """
    try:
        if request.user.project_leader:
            return request.user.project_leader.institute
    except ObjectDoesNotExist:
        return request.user.institute_admin.institute


class PermsAdmin(GuardedModelAdmin):
    def save_model(self, request, obj, form, change):
        super(PermsAdmin, self).save_model(request, obj, form, change)
        self.assign_permissions(request.user, obj)

    def perms_queryset(self, request, perm):
        if request.user.is_superuser:
            return super(PermsAdmin, self).get_queryset(request)
        return shortcuts.get_objects_for_user(request.user, [perm])

    def get_queryset(self, request):
        return self.perms_queryset(request, 'herana.change_%s' % self.permcode)

    def assign_permissions(self, user, obj):
        shortcuts.assign_perm('herana.change_%s' % self.permcode, user, obj)


class InstituteAdminInline(admin.TabularInline):
    model = models.InstituteAdmin
    can_delete = False


class StrategicObjectiveInline(admin.TabularInline):
    model = models.StrategicObjective
    inline_classes = ('grp-collapse grp-open',)
    extra = 7
    verbose_name_plural = _('Strategic Objectives')
    verbose_name = _('Strategic objectives of the Institute')


class InstituteAdmin(GuardedModelAdmin):
    inlines = [StrategicObjectiveInline]


class InstituteAdminUserAdmin(UserAdmin):
    inlines = (InstituteAdminInline,)
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
        return self.model.objects.filter(institute=request.user.institute_admin.institute)


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


class ProjectHeaderAdmin(admin.ModelAdmin):
    fields = ('name', 'is_flagship', 'is_leader')

    def save_model(self, request, obj, form, change):
        obj.proj_leader = request.user.project_leader
        obj.faculty = request.user.project_leader.faculty
        obj.save()

class ReportingPeriodFilter(admin.SimpleListFilter):
    title = "Reporting Period"
    parameter_name = 'reporting_period'

    def lookups(self, request, model_admin):
        reporting_periods = list(models.ReportingPeriod.objects.filter(institute=get_user_institute(request)))

        return [(rp.id, rp.name) for rp in reporting_periods]

    def queryset(self, request, queryset):
        if self.value():
            return queryset.filter(reporting_period=self.value())
        else:
            return queryset

class ProjectDetailAdmin(admin.ModelAdmin):
    list_display = ('__unicode__', 'record_status',)
    readonly_fields = ('reporting_period',)
    list_filter = (ReportingPeriodFilter, 'record_status')
    form = ProjectDetailForm
    save_as = True

    def has_add_permission(self, request, obj=None):
        if not request.user.is_superuser:
            if user_has_perm(request, self.opts, 'add'):
                # Can only add if a reporting period is open
                institute = request.user.project_leader.institute
                if models.ReportingPeriod.objects\
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
        if user_has_perm(request, self.opts, 'view'):
            return self.model.objects\
                .filter(header__proj_leader__institute=get_user_institute(request))\
                .exclude(record_status=1)
        if user_has_perm(request, self.opts, 'change'):
            return self.model.objects\
                .filter(header__proj_leader__institute=get_user_institute(request))\

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
        # This assumes that only one reporting period can be active at a time for a given Institute.
        reporting_period = request.user.project_leader.institute.reporting_period.get(is_active=True)
        if not change:
            obj.reporting_period = reporting_period
            if request.POST['_draft']:
                obj.record_status = 1
            else:
                obj.record_status = 2
        obj.save()

admin.site.register(models.Institute, InstituteAdmin)
# admin.site.register(models.InstituteAdmin, InstituteAdminUserAdmin)
admin.site.register(models.Faculty, FacultyAdmin)
admin.site.register(models.ReportingPeriod, ReportingPeriodAdmin)
admin.site.register(models.InstituteAdmin)
admin.site.register(models.ProjectLeader)
admin.site.register(models.ProjectHeader, ProjectHeaderAdmin)
admin.site.register(models.ProjectDetail, ProjectDetailAdmin)

admin.site.register(models.FocusArea)

admin.site.unregister(User)
admin.site.register(User, InstituteAdminUserAdmin)
