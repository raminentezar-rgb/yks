from django.db import models

class ProcessCard(models.Model):
    code = models.CharField(max_length=50, unique=True, verbose_name="Süreç Kodu", help_text="Örn: SR.01")
    name = models.CharField(max_length=200, verbose_name="Süreç Adı")
    owner = models.CharField(max_length=150, verbose_name="Süreç Sorumlusu", default="Rektör Yardımcısı")
    purpose = models.TextField(verbose_name="Süreç Amacı")
    inputs = models.TextField(verbose_name="Süreç Girdileri", help_text="Virgülle veya satırla ayırabilirsiniz")
    outputs = models.TextField(verbose_name="Süreç Çıktıları")
    kpi = models.TextField(verbose_name="Performans Göstergeleri (KPI)")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Oluşturulma Tarihi")

    class Meta:
        verbose_name = "Süreç Kartı"
        verbose_name_plural = "Süreç Kartları"
        ordering = ['code']

    def __str__(self):
        return f"{self.code} - {self.name}"


class JobDefinition(models.Model):
    code = models.CharField(max_length=50, unique=True, verbose_name="Görev Tanım Kodu", help_text="Örn: PP.2.3.GT.0583")
    title = models.CharField(max_length=200, verbose_name="Görev Unvanı")
    department = models.CharField(max_length=150, verbose_name="Bağlı Olduğu Birim")
    responsibilities = models.TextField(verbose_name="Temel Görev ve Sorumluluklar")
    qualifications = models.TextField(verbose_name="Aranan Nitelikler")
    updated_at = models.DateField(auto_now=True, verbose_name="Son Güncelleme")

    class Meta:
        verbose_name = "Görev Tanımı"
        verbose_name_plural = "Görev Tanımları"
        ordering = ['code']

    def __str__(self):
        return f"{self.code} - {self.title}"
