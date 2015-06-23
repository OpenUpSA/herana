from django.utils.translation import ugettext_lazy as _
from django.contrib import admin

from guardian.admin import GuardedModelAdmin

import models


class PermsAdmin(GuardedModelAdmin):
    def assign_permissions():
        pass


class InstituteAdmin(GuardedModelAdmin):
    pass

admin.site.register(models.Institute, InstituteAdmin)
admin.site.register(models.Faculty)
admin.site.register(models.StrategicObjective)
admin.site.register(models.InstituteAdmin)
admin.site.register(models.ProjectLeader)
admin.site.register(models.ReportingPeriod)
admin.site.register(models.ProjectHeader)
admin.site.register(models.ProjectDetail)
