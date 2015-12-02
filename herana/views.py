import json

from django.shortcuts import render
from django.views.generic import View
from models import ProjectDetail
from forms import SelectInstituteForm, SelectOrgLevelForm

def home(request):
    return render(request, 'index.html')


class ResultsView(View):
    template_name = 'results.html'

    def get(self, request, *args, **kwargs):
        projects = ProjectDetail.objects.filter(
            record_status=2,
            is_rejected=False,
            is_deleted=False)

        data = json.dumps([p.as_dict() for p in projects])
        import ipdb; ipdb.set_trace()
        context = {
          "data": data,
        }

        return render(
            request,
            self.template_name,
            context=context)


    def post(self, request, *args, **kwargs):
        institute = None
        org_level_form = None
        results = []

        if 'get_institute' in request.POST:
            institute_form = SelectInstituteForm(request.POST)
        elif 'get_org_level' in request.POST:
            form = SelectOrgLevelForm(request.POST)

        if institute_form.is_valid():
            level = 1
            institute = institute_form.cleaned_data['institute']
            org_level_form = SelectOrgLevelForm(institute=institute)

            # Get all projects for the institute which are:
            # Final, not rejected, and not marked as deleted
            projects = ProjectDetail.objects.filter(
                institute=institute,
                record_status=2,
                is_rejected=False,
                is_deleted=False)

            results = []
            for project in projects:
                x, y = project.calc_score()
                duration = project.calc_duration()
                unit_id = project.__getattribute__('org_level_%s' % level).id
                results.append({
                    'x': x,
                    'y': y,
                    'r': duration,
                    'unit_id': unit_id,
                })

            results = json.dumps(results)

        context = {
            "institute": institute,
            "institute_form": institute_form,
            "org_level_form": org_level_form,
            "results": results
        }

        return render(
            request,
            self.template_name,
            context=context)
