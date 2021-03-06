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
        """
        Return a queryset of projects.
        :: active => Only return results for active reporting period if True
        :: institute => Return queryset filtered by institute.
        """
        projects = ProjectDetail.objects\
            .filter(
                record_status=2,
                is_rejected=False,
                is_deleted=False,
                reporting_period__is_active=active)\
            .prefetch_related('institute', 'strategic_objectives', 'student_nature', 'student_types',
                              'org_level_1', 'org_level_2', 'org_level_3',
                              'org_level_1__institute', 'org_level_2__institute', 'org_level_3__institute',
                              'adv_group_rep', 'team_members', 'focus_area')
        if institute:
            projects = projects.filter(institute=institute)
        return projects


    def get(self, request, *args, **kwargs):
        # Get projects for closed reporting periods
        projects = self.get_projects()
        # Get unique instances of institutes for these projects
        institutes = {proj.institute for proj in projects}

        data = {}

        data['projects'] = [p.as_dict() for p in projects]

        active_projects = []
        if request.user.is_authenticated():
            if request.user.is_superuser:
                # Get active period projects for all institutes
                active_projects = self.get_projects(active=True)
            else:
                # Only get active period projects for current user institute
                user_institute = request.user.get_user_institute()
                active_projects = self.get_projects(
                    active=True,
                    institute=user_institute)
                data['user_institute'] =  user_institute.as_dict()

        # Add institutes for active period projects
        institutes.update([proj.institute for proj in active_projects])

        data['institutes'] = [
            i.as_dict(user=request.user, add_reporting_periods=True)
            for i in institutes
        ]
        data['projects'].extend([p.as_dict() for p in active_projects])

        has_results = True if data['institutes'] else False

        context = {
          "data": json.dumps(data),
          "has_results": has_results
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

        filename = 'Herana results - %s - %s' % (institute.name, date.today())

        response = HttpResponse(xlsx, content_type='application/vnd.ms-excel')
        response['Content-Disposition'] = 'attachment; filename=%s.xlsx' % filename

        return response


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


def write_values(ws, col, projects, key, parent_key=None):
    row = 1
    for proj in projects:
        if not parent_key:
            if key == 'reporting_period':
                ws.write(row, col, proj[key]['name'])
            elif key == 'duration':
                ws.write(row, col, DURATION[proj[key]])
            elif key == 'status':
                ws.write(row, col, STATUS[proj[key]])
            elif key == 'institute':
                ws.write(row, col, proj['institute']['name'])
            else:
                ws.write(row, col, proj[key])
        else:
            ws.write(row, col, proj[parent_key][key])
        row += 1


def create_report_headings(institute):
    return OrderedDict([
        ('institute', 'Institute'),
        ('name', 'Project Name'),
        ('org_level_1', '1 - %s' % (institute.org_level_1_name if institute.org_level_1_name else '')),
        ('org_level_2', '2 - %s' % (institute.org_level_2_name if institute.org_level_2_name else '')),
        ('org_level_3', '3 - %s' % (institute.org_level_3_name if institute.org_level_3_name else '')),
        ('reporting_period', 'Period captured'),
        ('duration', 'Duration'),
        ('status', 'Status'),
        ('score', OrderedDict([
            ('a_1', 'Alignment of objectives'),
            ('a_2', 'Initiation/agenda-setting'),
            ('a_3', 'External stakeholders'),
            ('a_4', 'Funding'),
            ('y', 'Articulation Total'),
            ('c_1', 'Generates new knowledge or product'),
            ('c_2', 'Dissemination'),
            ('c_3_a', 'Teaching/curriculum development'),
            ('c_3_b', 'Formal teaching/learning of students'),
            ('c_4', 'Links to academic network'),
            ('x', 'Academic Core Total')
        ]))
    ])

DURATION = {
    0: '0-1.99',
    1: '2-2.99',
    2: '3-3.99',
    3: '4-4.99',
    4: '5+'}

STATUS = {
    1: 'Complete',
    2: 'Ongoing'}
