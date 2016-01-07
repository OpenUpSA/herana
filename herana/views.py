import json
import StringIO
from datetime import date
from collections import OrderedDict, Mapping
import xlsxwriter

from django.shortcuts import render
from django.views.generic import View
from django.http import HttpResponse

from models import Institute, ProjectDetail


def home(request):
    return render(request, 'index.html')


class ResultsView(View):
    template_name = 'results.html'

    def get_projects(self, active=False, institute=None):
        projects = ProjectDetail.objects.filter(
            record_status=2,
            is_rejected=False,
            is_deleted=False,
            reporting_period__is_active=active)
        if institute:
            projects.filter(institute=institute)
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
                    institute=user_institute)
                data['user_institute'] =  user_institute.as_dict()

        data['projects'].extend([p.as_dict() for p in active_projects])

        context = {
          "data": json.dumps(data),
        }

        return render(
            request,
            self.template_name,
            context=context)

    def post(self, request, *args, **kwargs):
        institute = Institute.objects.get(id=int(request.POST.get('institute_id')))

        if request.user.is_authenticated():
            if request.user.is_superuser:
                projects = self.get_projects(active=True, institute=institute)
            else:
                if request.user.get_user_institute() == institute:
                    projects = self.get_projects(active=True, institute=institute)
                else:
                    projects = self.get_projects(institute=institute)
        else:
            projects = self.get_projects(institute=institute)

        xlsx = build_xlsx(institute, [p.as_dict() for p in projects])

        filename = 'Herana results - : %s - %s' % (institute.name, date.today())

        response = HttpResponse(xlsx, content_type='application/vnd.ms-excel')
        response['Content-Disposition'] = 'attachment; filename=%s.xlsx' % filename

        return response


def write_values(ws, col, projects, key, parent_key=None):
    row = 1
    for proj in projects:
        if not parent_key:
            ws.write(row, col, proj[key])
        else:
            ws.write(row, col, proj[parent_key][key])
        row += 1


def build_xlsx(institute, projects):
    output = StringIO.StringIO()
    workbook = xlsxwriter.Workbook(output)

    ws = workbook.add_worksheet('Results')

    col = 0
    sheet_headings = create_report_headings(institute)

    for k, v in sheet_headings.iteritems():
        row = 0
        if not isinstance(v, OrderedDict):
            ws.write(row, col, v)
            write_values(ws, col, projects, k)
            col += 1
        else:
            for child_k, child_v in v.iteritems():
                ws.write(row, col, child_v)
                write_values(ws, col, projects, child_k, parent_key=k)
                col += 1

    workbook.close()
    output.seek(0)

    return output.read()

def create_report_headings(institute):
    return OrderedDict([
        ('name', 'Project Name'),
        ('org_level_1', institute.org_level_1_name if institute.org_level_1_name else None),
        ('duration', 'Duration'),
        ('score', OrderedDict([
            ('a_1', 'Alignment of objectives'),
            ('y', 'Articulation Total')
        ]))
    ])
