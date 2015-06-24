from datetime import date

from django.utils.translation import ugettext_lazy as _
from django.contrib import admin

from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User

from guardian import shortcuts
from guardian.admin import GuardedModelAdmin

import models


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
    def has_module_permission(self, request):
        # if request.user.is_superuser:
        #     return True
        # return False
        return True


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
            return True
        return True

    def has_delete_permission(self, request, obj=None):
        if not request.user.is_superuser:
            if obj:
                if request.user.institute_admin.institute == obj.institute:
                    return True
                return False
            # Should faculties be deleted by InstituteAdmins?
            return True
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
        if not self.model.objects.filter(is_active=True):
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
        import ipdb; ipdb.set_trace()
        if obj and obj.is_active == False:
            return self.readonly_fields + ('is_active',)
        return self.readonly_fields




admin.site.register(models.Institute, InstituteAdmin)
# admin.site.register(models.InstituteAdmin, InstituteAdminUserAdmin)
admin.site.register(models.Faculty, FacultyAdmin)
admin.site.register(models.ReportingPeriod, ReportingPeriodAdmin)
admin.site.register(models.ProjectLeader)
admin.site.register(models.StrategicObjective)
admin.site.register(models.InstituteAdmin)
admin.site.register(models.ProjectHeader)
admin.site.register(models.ProjectDetail)

admin.site.unregister(User)
admin.site.register(User, InstituteAdminUserAdmin)
