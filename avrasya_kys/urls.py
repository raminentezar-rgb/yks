from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

# Rektörlük ve Başkanlık İçin Özelleştirilmiş Admin Panel Başlıkları
admin.site.site_header = "AVRASYA ÜNİVERSİTESİ - KYS YÖNETİCİ VE DENETİM PORTALI"
admin.site.site_title = "Avrasya KYS Yönetim"
admin.site.index_title = "Merkez Karargah, Akreditasyon ve Süreç Denetim Paneli"

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('core.urls')),
    path('documents/', include('documents.urls')),
    path('processes/', include('processes.urls')),
    path('feedback/', include('feedback.urls')),
    path('dif/', include('dif.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
