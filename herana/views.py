import json

from django.shortcuts import render
from django.views.generic import View
from models import Institute, ProjectDetail
from forms import SelectInstituteForm, SelectOrgLevelForm

def home(request):
    return render(request, 'index.html')


class ResultsView(View):
    template_name = 'results.html'

    def get_projects(self, active=False, user_institute=None):
        projects = ProjectDetail.objects.filter(
            record_status=2,
            is_rejected=False,
            is_deleted=False,
            reporting_period__is_active=active)
        if user_institute:
            projects.filter(institute=user_institute)
        return projects


    def get(self, request, *args, **kwargs):
        projects = self.get_projects()
        # institutes = {proj.institute for proj in projects}
        institutes = Institute.objects.filter(reporting_period__isnull=False)

        data = {}

        data['institutes'] = [i.as_dict() for i in institutes]
        data['projects'] = [p.as_dict() for p in projects]

        active_projects = []
        if request.user.is_authenticated():
            if request.user.is_superuser:
                active_projects = self.get_projects(active=True)
            else:
                user_institute = request.user.get_user_institute()
                active_projects = self.get_projects(
                    active=True,
                    user_institute=user_institute)
                data['user_institute'] =  user_institute.as_dict()

        data['projects'].extend([p.as_dict() for p in active_projects])

        context = {
          "data": json.dumps(data),
        }

        return render(
            request,
            self.template_name,
            context=context)
