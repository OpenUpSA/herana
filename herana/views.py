import json

from django.shortcuts import render
from models import Institute, ProjectDetail
from forms import SelectInstituteForm

def home(request):
    return render(request, 'index.html')

def results(request):
    results = []
    if request.method == 'POST':
        form = SelectInstituteForm(request.POST)
        if form.is_valid():
            institute = form.cleaned_data['institute']
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
                results.append({
                    'x': x,
                    'y': y,
                    'r': duration
                })
    else:
        form = SelectInstituteForm()

    context = {
      "form": form,
      "results": json.dumps(results)
    }

    return render(
      request,
      'results.html',
      context=context)
