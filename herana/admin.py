from django.utils.translation import ugettext_lazy as _
from django.contrib import admin

from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User

from guardian.admin import GuardedModelAdmin

import models


class PermsAdmin(GuardedModelAdmin):
    def assign_permissions():
        pass


class InstituteAdminInline(admin.TabularInline):
    model = models.InstituteAdmin
    can_delete = False


class InstituteAdmin(GuardedModelAdmin):
    pass


class InstituteAdminUserAdmin(UserAdmin):
    inlines = (InstituteAdminInline,)
    list_display = ('username', 'email', 'first_name', 'last_name', 'is_staff')


admin.site.register(models.Institute, InstituteAdmin)
# admin.site.register(models.InstituteAdmin, InstituteAdminUserAdmin)
admin.site.register(models.Faculty)
admin.site.register(models.StrategicObjective)
admin.site.register(models.InstituteAdmin)
admin.site.register(models.ProjectLeader)
admin.site.register(models.ReportingPeriod)
admin.site.register(models.ProjectHeader)
admin.site.register(models.ProjectDetail)

admin.site.unregister(User)
admin.site.register(User, InstituteAdminUserAdmin)
