from django.shortcuts import render
from django.db.models import Q
from .models import DifRecord

def dif_list(request):
    records = DifRecord.objects.all()
    
    # Status filter
    status_filter = request.GET.get('status')
    if status_filter:
        records = records.filter(status=status_filter)
        
    # Search query
    query = request.GET.get('q', '').strip()
    if query:
        records = records.filter(
            Q(code__icontains=query) |
            Q(title__icontains=query) |
            Q(unit__icontains=query) |
            Q(responsible_person__icontains=query)
        )
        
    context = {
        'records': records,
        'status_filter': status_filter,
        'query': query,
    }
    return render(request, 'dif/dif_list.html', context)
