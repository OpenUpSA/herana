import json

from django.shortcuts import render
from django.views.generic import View
from models import Institute, ProjectDetail
from forms import SelectInstituteForm, SelectOrgLevelForm

def home(request):
    return render(request, 'index.html')


class ResultsView(View):
    template_name = 'results.html'

    def get(self, request, *args, **kwargs):
        institutes = Institute.objects.all()
        projects = ProjectDetail.objects.filter(
            record_status=2,
            is_rejected=False,
            is_deleted=False)

        data = {}

        data['projects'] = [p.as_dict() for p in projects]
        data['institutes'] = [i.as_dict() for i in institutes]

        context = {
          "data": json.dumps(data),
        }

        return render(
            request,
            self.template_name,
            context=context)
