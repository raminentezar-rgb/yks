from django.db import models

class Announcement(models.Model):
    CATEGORY_CHOICES = [
        ('görev', 'Yeni Görev Tanımı'),
        ('doküman', 'Güncellenen Dokümanlar'),
        ('yeni_doküman', 'Yeni Yayınlanan Dokümanlar'),
        ('genel', 'Genel Duyuru'),
    ]
    
    title = models.CharField(max_length=255, verbose_name="Duyuru Başlığı")
    content = models.TextField(verbose_name="Duyuru İçeriği")
    category = models.CharField(max_length=50, choices=CATEGORY_CHOICES, default='genel', verbose_name="Kategori")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Yayın Tarihi")
    link = models.CharField(max_length=255, blank=True, null=True, verbose_name="İlgili Bağlantı")

    class Meta:
        verbose_name = "Duyuru"
        verbose_name_plural = "Duyurular"
        ordering = ['-created_at']

    def __str__(self):
        return self.title


class SystemStat(models.Model):
    """Holds custom statistics to showcase live university activity on dashboard"""
    key = models.CharField(max_length=50, unique=True, verbose_name="İstatistik Anahtarı")
    label = models.CharField(max_length=100, verbose_name="Başlık")
    count = models.IntegerField(default=0, verbose_name="Toplam Sayı")
    new_count = models.IntegerField(default=0, verbose_name="Yeni Eklenen (Bu Ay)")
    icon = models.CharField(max_length=50, default="fa-user", verbose_name="FontAwesome İkonu")
    color_class = models.CharField(max_length=50, default="icon-blue", verbose_name="Renk Sınıfı")

    class Meta:
        verbose_name = "Sistem İstatistiği"
        verbose_name_plural = "Sistem İstatistikleri"

    def __str__(self):
        return f"{self.label}: {self.count}"
