from django.shortcuts import render, get_object_or_404
from .models import Announcement, SystemStat

def dashboard_view(request):
    announcements = Announcement.objects.all()[:6]
    stats = SystemStat.objects.all()
    
    # Try to load top downloaded documents if available
    top_documents = []
    try:
        from documents.models import Document
        top_documents = Document.objects.order_by('-download_count')[:8]
    except Exception:
        pass

    # If no stats exist yet in DB, provide fallback stats for UI presentation
    if not stats.exists():
        fallback_stats = [
            {'label': 'Kullanıcı Sayısı', 'count': 5240, 'new_count': 74, 'icon': 'fa-users', 'color_class': 'icon-blue', 'trend': 'up'},
            {'label': 'Birim Sayısı', 'count': 1420, 'new_count': 5, 'icon': 'fa-building-columns', 'color_class': 'icon-gold', 'trend': 'up'},
            {'label': 'Doküman Sayısı', 'count': 1850, 'new_count': 23, 'icon': 'fa-file-lines', 'color_class': 'icon-green', 'trend': 'up'},
            {'label': 'Geri Bildirim Sayısı', 'count': 41200, 'new_count': 310, 'icon': 'fa-comments', 'color_class': 'icon-purple', 'trend': 'up'},
            {'label': 'DİF Kayıtları', 'count': 3240, 'new_count': 12, 'icon': 'fa-shield-halved', 'color_class': 'icon-indigo', 'trend': 'up'},
            {'label': 'İyileştirme & Revizyon', 'count': 3480, 'new_count': 18, 'icon': 'fa-wrench', 'color_class': 'icon-red', 'trend': 'up'},
        ]
    else:
        fallback_stats = stats

    context = {
        'announcements': announcements,
        'stats': fallback_stats,
        'top_documents': top_documents,
    }
    return render(request, 'core/dashboard.html', context)


def announcement_list_view(request):
    announcements = Announcement.objects.all()
    
    category = request.GET.get('category')
    if category and category != 'all':
        announcements = announcements.filter(category=category)
        
    q = request.GET.get('q')
    if q:
        announcements = announcements.filter(title__icontains=q) | announcements.filter(content__icontains=q)
        announcements = announcements.distinct()

    context = {
        'announcements': announcements,
        'selected_category': category or 'all',
        'search_query': q or '',
        'category_choices': Announcement.CATEGORY_CHOICES,
    }
    return render(request, 'core/announcement_list.html', context)


def announcement_detail_view(request, pk):
    announcement = get_object_or_404(Announcement, pk=pk)
    recent_announcements = Announcement.objects.exclude(pk=pk)[:5]
    
    context = {
        'announcement': announcement,
        'recent_announcements': recent_announcements,
    }
    return render(request, 'core/announcement_detail.html', context)
