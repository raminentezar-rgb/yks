import uuid
from django.db import models

def generate_tracking_code():
    return uuid.uuid4().hex[:8].upper()

class Feedback(models.Model):
    TYPE_CHOICES = [
        ('öneri', 'Öneri / Tavsiye'),
        ('şikayet', 'Şikayet / Memnuniyetsizlik'),
        ('takdir', 'Takdir / Teşekkür'),
        ('diğer', 'Diğer Kalite Bildirimi'),
    ]
    
    USER_TYPE_CHOICES = [
        ('öğrenci', 'Öğrenci'),
        ('akademik', 'Akademik Personel'),
        ('idari', 'İdari Personel'),
        ('dış', 'Dış Paydaş / Ziyaretçi'),
    ]
    
    STATUS_CHOICES = [
        ('beklemede', 'Beklemede / İçe aktarıldı'),
        ('islemde', 'Değerlendirme Aşamasında'),
        ('cozuldu', 'Çözüldü / Sonuçlandı'),
    ]

    tracking_code = models.CharField(max_length=15, unique=True, default=generate_tracking_code, verbose_name="Takip Kodu")
    feedback_type = models.CharField(max_length=20, choices=TYPE_CHOICES, default='öneri', verbose_name="Bildirim Türü")
    user_type = models.CharField(max_length=20, choices=USER_TYPE_CHOICES, default='öğrenci', verbose_name="Paydaş Türü")
    unit = models.CharField(max_length=150, verbose_name="İlgili Birim / Fakülte", default="Avrasya Üniversitesi Genel")
    name_surname = models.CharField(max_length=100, blank=True, null=True, default="Anonim Paydaş", verbose_name="Ad Soyad")
    email = models.EmailField(blank=True, null=True, verbose_name="E-Posta")
    subject = models.CharField(max_length=200, verbose_name="Konu")
    message = models.TextField(verbose_name="Bildirim Detayı / Mesaj")
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='beklemede', verbose_name="Durum")
    admin_response = models.TextField(blank=True, null=True, verbose_name="Birim / Kalite Koordinatörlüğü Cevabı")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Oluşturulma Tarihi")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Son Güncelleme")

    class Meta:
        verbose_name = "Geri Bildirim"
        verbose_name_plural = "Geri Bildirimler"
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.tracking_code} - {self.subject} ({self.get_status_display()})"
