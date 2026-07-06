from django.db import models

class DifRecord(models.Model):
    FINDING_CHOICES = [
        ('iç_tetkik', 'İç Kalite Tetkiki'),
        ('dış_tetkik', 'YÖKAK / Dış Değerlendirme'),
        ('paydaş', 'Paydaş Geri Bildirimi'),
        ('risk', 'Kurumsal Risk Değerlendirmesi'),
    ]

    STATUS_CHOICES = [
        ('acik', 'Açık / İşlem Bekliyor'),
        ('devam', 'Düzeltici Faaliyet Devam Ediyor'),
        ('dogrulama', 'Etkinlik Doğrulama Aşamasında'),
        ('kapali', 'Başarıyla Kapatıldı'),
    ]

    code = models.CharField(max_length=50, unique=True, verbose_name="DİF Numarası", help_text="Örn: DİF.2026.001")
    title = models.CharField(max_length=255, verbose_name="Uygunsuzluk / Gelişme Alanı Başlığı")
    unit = models.CharField(max_length=150, verbose_name="Sorumlu Birim", default="Avrasya Üniversitesi Genel")
    finding_type = models.CharField(max_length=30, choices=FINDING_CHOICES, default='iç_tetkik', verbose_name="Tespit Kaynağı")
    root_cause = models.TextField(verbose_name="Kök Neden Analizi")
    action_plan = models.TextField(verbose_name="Planlanan Düzeltici / Önleyici Faaliyetler")
    responsible_person = models.CharField(max_length=150, verbose_name="Faaliyet Sorumlusu")
    target_date = models.DateField(verbose_name="Hedef Kapatma Tarihi")
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='acik', verbose_name="DİF Durumu")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Açılış Tarihi")
    closed_at = models.DateField(blank=True, null=True, verbose_name="Kapanış Tarihi")

    class Meta:
        verbose_name = "DİF Kaydı"
        verbose_name_plural = "DİF Kayıtları"
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.code} - {self.title} ({self.get_status_display()})"
