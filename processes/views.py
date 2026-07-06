from django.shortcuts import render
from django.db.models import Q
from .models import ProcessCard, JobDefinition

def process_list(request):
    tab = request.GET.get('tab', 'processes')
    query = request.GET.get('q', '').strip()
    
    processes = ProcessCard.objects.all()
    jobs = JobDefinition.objects.all()
    
    if query:
        processes = processes.filter(Q(name__icontains=query) | Q(code__icontains=query) | Q(owner__icontains=query))
        jobs = jobs.filter(Q(title__icontains=query) | Q(code__icontains=query) | Q(department__icontains=query))
        
    context = {
        'tab': tab,
        'processes': processes,
        'jobs': jobs,
        'query': query,
    }
    return render(request, 'processes/process_list.html', context)
