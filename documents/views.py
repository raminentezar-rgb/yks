from django.shortcuts import render, get_object_or_404, redirect
from django.db.models import Q
from django.http import HttpResponse, Http404
from .models import Document, DocumentCategory

def document_list(request):
    categories = DocumentCategory.objects.all()
    documents = Document.objects.filter(is_active=True)
    
    # Search query
    query = request.GET.get('q', '').strip()
    if query:
        documents = documents.filter(
            Q(title__icontains=query) |
            Q(code__icontains=query) |
            Q(unit__icontains=query)
        )
    
    # Category filter
    cat_code = request.GET.get('category')
    selected_category = None
    if cat_code:
        documents = documents.filter(category__code=cat_code)
        selected_category = get_object_or_404(DocumentCategory, code=cat_code)
        
    context = {
        'categories': categories,
        'documents': documents,
        'query': query,
        'selected_category': selected_category,
    }
    return render(request, 'documents/document_list.html', context)


def document_download(request, doc_id):
    doc = get_object_or_404(Document, id=doc_id, is_active=True)
    doc.download_count += 1
    doc.save(update_fields=['download_count'])
    
    if doc.file and doc.file.url:
        return redirect(doc.file.url)
    elif doc.file_url:
        return redirect(doc.file_url)
    else:
        # If no physical file is uploaded in seed data, generate a sample text response
        response = HttpResponse(f"Avrasya KYS - {doc.code}\nDoküman: {doc.title}\nSorumlu Birim: {doc.unit}\nRevizyon: {doc.revision_number}\nBu dosya Avrasya Üniversitesi Kalite Yönetim Sistemi üzerinden indirildi.", content_type="text/plain; charset=utf-8")
        response['Content-Disposition'] = f'attachment; filename="{doc.code}.txt"'
        return response
