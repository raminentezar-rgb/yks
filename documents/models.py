from django.db import models

class DocumentCategory(models.Model):
    name = models.CharField(max_length=100, verbose_name="Kategori Adı")
    code = models.CharField(max_length=20, unique=True, verbose_name="Kategori Kodu", help_text="Örn: FR, PR, TAL")
    description = models.TextField(blank=True, null=True, verbose_name="Açıklama")
    icon = models.CharField(max_length=50, default="fa-folder-open", verbose_name="İkon")

    class Meta:
        verbose_name = "Doküman Kategorisi"
        verbose_name_plural = "Doküman Kategorileri"
        ordering = ['name']

    def __str__(self):
        return self.name


class Document(models.Model):
    category = models.ForeignKey(DocumentCategory, on_delete=models.CASCADE, related_name="documents", verbose_name="Kategori")
    code = models.CharField(max_length=50, unique=True, verbose_name="Doküman Kodu", help_text="Örn: PP.1.2.FR.0033")
    title = models.CharField(max_length=255, verbose_name="Doküman Adı")
    unit = models.CharField(max_length=150, verbose_name="Sorumlu Birim", default="Avrasya Rektörlüğü")
    file = models.FileField(upload_to="documents/%Y/", blank=True, null=True, verbose_name="Dosya")
    file_url = models.CharField(max_length=500, blank=True, null=True, verbose_name="Harici Dosya Bağlantısı (İsteğe Bağlı)")
    revision_number = models.CharField(max_length=20, default="Rev. 00", verbose_name="Revizyon No")
    revision_date = models.DateField(auto_now=True, verbose_name="Son Revizyon Tarihi")
    download_count = models.IntegerField(default=0, verbose_name="İndirme Sayısı")
    is_active = models.BooleanField(default=True, verbose_name="Yayında")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Yüklenme Tarihi")

    class Meta:
        verbose_name = "Doküman"
        verbose_name_plural = "Dokümanlar"
        ordering = ['-download_count', '-created_at']

    def __str__(self):
        return f"{self.code} - {self.title}"
