from django.utils.translation import ugettext_lazy as _
from django.core.urlresolvers import reverse

from grappelli.dashboard import modules, Dashboard
from grappelli.dashboard.utils import get_admin_site_name


class CustomIndexDashboard(Dashboard):
    """
    Custom index dashboard for www.
    """

    def init_with_context(self, context):
        site_name = get_admin_site_name(context)

        # append an app list module for "Administration"
        self.children.append(modules.ModelList(
            _('User Administration'),
            column=1,
            collapsible=False,
            models=(
                'django.contrib.*',
                'herana.models.InstituteAdmin',
                'herana.models.ProjectLeader',),
        ))

        self.children.append(modules.ModelList(
            _('Institute Administration'),
            column=1,
            collapsible=False,
            models=(
                'herana.models.Institute',
                'herana.models.Faculty',
                'herana.models.ReportingPeriod'
                ),
        ))

        self.children.append(modules.ModelList(
            _('Questionaire Administration'),
            column=1,
            collapsible=False,
            models=(
                'herana.models.FocusArea',
            ),
        ))

        self.children.append(modules.ModelList(
            _('Project Administration'),
            column=1,
            collapsible=False,
            models=(
                'herana.models.ProjectHeader',
                'herana.models.ProjectDetail'),
        ))

        # append a recent actions module
        self.children.append(modules.RecentActions(
            _('Recent Actions'),
            limit=5,
            collapsible=False,
            column=2,
        ))


