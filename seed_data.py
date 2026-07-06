import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'avrasya_kys.settings')
django.setup()

from datetime import date
from core.models import Announcement, SystemStat
from documents.models import DocumentCategory, Document
from processes.models import ProcessCard, JobDefinition
from feedback.models import Feedback
from dif.models import DifRecord
from django.contrib.auth.models import User

def run_seed():
    print(">>> Avrasya KYS v2.0 - Örnek Veri Yükleme (Seeding) Başlıyor...")

    # 0. Create Superusers for Admin Access
    u1, _ = User.objects.get_or_create(username='admin', defaults={'email': 'admin@avrasya.edu.tr'})
    u1.set_password('admin123')
    u1.is_superuser = True; u1.is_staff = True; u1.save()
    
    u2, _ = User.objects.get_or_create(username='avrasya', defaults={'email': 'kalite@avrasya.edu.tr'})
    u2.set_password('avrasya123')
    u2.is_superuser = True; u2.is_staff = True; u2.save()
    print("  [+] Yönetici (Admin) hesapları hazırlandı: admin/admin123 & avrasya/avrasya123")

    # 1. System Stats
    SystemStat.objects.all().delete()
    stats_data = [
        {'key': 'users', 'label': 'Kullanıcı Sayısı', 'count': 5240, 'new_count': 74, 'icon': 'fa-users', 'color_class': 'icon-blue'},
        {'key': 'units', 'label': 'Birim Sayısı', 'count': 1420, 'new_count': 5, 'icon': 'fa-building-columns', 'color_class': 'icon-gold'},
        {'key': 'docs', 'label': 'Doküman Sayısı', 'count': 1850, 'new_count': 23, 'icon': 'fa-file-lines', 'color_class': 'icon-green'},
        {'key': 'feedbacks', 'label': 'Geri Bildirim Sayısı', 'count': 41200, 'new_count': 310, 'icon': 'fa-comments', 'color_class': 'icon-purple'},
        {'key': 'difs', 'label': 'DİF Kayıtları', 'count': 3240, 'new_count': 12, 'icon': 'fa-shield-halved', 'color_class': 'icon-indigo'},
        {'key': 'revs', 'label': 'İyileştirme & Revizyon', 'count': 3480, 'new_count': 18, 'icon': 'fa-wrench', 'color_class': 'icon-red'},
    ]
    for s in stats_data:
        SystemStat.objects.create(**s)
    print("  [+] SystemStat verileri eklendi (6 adet).")

    # 2. Announcements
    Announcement.objects.all().delete()
    ann_data = [
        {
            'title': 'Avrasya KYS v2.0 Platformu Yayında!',
            'content': 'YÖKAK kalite ölçütlerine ve ISO 9001 standartlarına tam uyumlu yeni dijital kalite yönetim portalımız hizmete girmiştir. Tüm paydaşlarımız sisteme giriş yapabilir.',
            'category': 'genel',
        },
        {
            'title': 'PP.2.3.GT.0583 Bilimsel Araştırma Projeleri Birim Sorumlusu Görev Tanımı',
            'content': 'BAPKOB Birim Sorumlusu revize edilmiş görev tanımı ve iş akış şemaları sisteme yüklenmiştir. İlgili personelin incelemesi rica olunur.',
            'category': 'görev',
        },
        {
            'title': 'PP.5.2.TAL.0003 Doküman Oluşturma Talimatı Revizyonu',
            'content': 'Kalite güvence sistemi kapsamında doküman hazırlama, taslak kontrolü ve onaylama talimatı güncellendi (Rev. 03).',
            'category': 'doküman',
        },
        {
            'title': 'YÖKAK Kurumsal İç Değerlendirme Raporu (KİDR) Hazırlık Toplantısı',
            'content': '2026-2027 akademik yılı KİDR hazırlıkları kapsamında tüm birim kalite komisyonu başkanları ile Rektörlük Senato Salonunda toplantı gerçekleştirilecektir.',
            'category': 'genel',
        },
        {
            'title': 'ISO 9001:2015 Kalite Yönetim Sistemi İç Tetkik Takvimi Yayınlandı',
            'content': 'Üniversitemiz fakülte, enstitü ve idari birimlerinde gerçekleştirilecek yıllık iç tetkik takvimi ve denetçi listeleri Dokümanlar modülüne eklenmiştir.',
            'category': 'yeni_doküman',
        },
    ]
    for a in ann_data:
        Announcement.objects.create(**a)
    print("  [+] Announcement verileri eklendi (5 adet).")

    # 3. Document Categories & Documents
    Document.objects.all().delete()
    DocumentCategory.objects.all().delete()
    
    cats = {
        'PR': DocumentCategory.objects.create(name="Prosedürler", code="PR", icon="fa-diagram-project", description="Temel kurumsal işleyiş ve kalite güvence prosedürleri"),
        'TAL': DocumentCategory.objects.create(name="Talimatlar", code="TAL", icon="fa-list-check", description="Cihaz kullanım, iş güvenliği ve operasyonel uygulama talimatları"),
        'FR': DocumentCategory.objects.create(name="Formlar", code="FR", icon="fa-file-lines", description="Akademik ve idari başvuru, talep ve bildirim formları"),
        'YN': DocumentCategory.objects.create(name="Yönerge ve Yönetmelikler", code="YN", icon="fa-scale-balanced", description="Üniversite senatosu ve YÖK tarafından onaylanan yasal düzenlemeler"),
        'SA': DocumentCategory.objects.create(name="Süreç Akış Şemaları", code="SA", icon="fa-sitemap", description="Adım adım operasyonel iş akış şemaları ve sorumluluk matrisleri"),
    }
    print("  [+] DocumentCategory verileri eklendi (5 adet).")

    docs_data = [
        {'code': 'PP.1.2.FR.0033', 'title': 'Tez Konusu Öneri Formu (Lisansüstü)', 'unit': 'Lisansüstü Eğitim Enstitüsü', 'cat': 'FR', 'rev': 'Rev. 02', 'downloads': 1420},
        {'code': 'PP.2.1.PR.0001', 'title': 'Eğitim Öğretim Kalite Güvence Prosedürü', 'unit': 'Kalite Koordinatörlüğü', 'cat': 'PR', 'rev': 'Rev. 04', 'downloads': 1250},
        {'code': 'PP.4.1.YN.0005', 'title': 'Bilimsel Araştırma Projeleri Uygulama Yönergesi', 'unit': 'BAPKOB', 'cat': 'YN', 'rev': 'Rev. 01', 'downloads': 1120},
        {'code': 'PP.1.2.FR.0021', 'title': 'Zorunlu / Gönüllü Staj Başvuru ve Kabul Formu', 'unit': 'Mühendislik Fakültesi', 'cat': 'FR', 'rev': 'Rev. 03', 'downloads': 980},
        {'code': 'PP.1.2.FR.0085', 'title': 'Ek Ders Ücreti Bildirim Formu (Akademik)', 'unit': 'Personel Daire Başkanlığı', 'cat': 'FR', 'rev': 'Rev. 01', 'downloads': 850},
        {'code': 'PP.1.2.FR.0041', 'title': 'Ders Muafiyet ve İntibak Başvuru Formu', 'unit': 'Öğrenci İşleri Daire Başkanlığı', 'cat': 'FR', 'rev': 'Rev. 02', 'downloads': 740},
        {'code': 'PP.1.3.FR.0053', 'title': 'Mezuniyet Talep ve İlişik Kesme Belgesi', 'unit': 'Öğrenci İşleri', 'cat': 'FR', 'rev': 'Rev. 05', 'downloads': 690},
        {'code': 'PP.3.4.TAL.0012', 'title': 'Laboratuvar Güvenlik ve Cihaz Kullanım Talimatı', 'unit': 'Mühendislik Fakültesi', 'cat': 'TAL', 'rev': 'Rev. 01', 'downloads': 540},
        {'code': 'PP.5.1.SA.0008', 'title': 'Öğrenci Disiplin Soruşturması Akış Şeması', 'unit': 'Hukuk Müşavirliği', 'cat': 'SA', 'rev': 'Rev. 00', 'downloads': 420},
    ]
    for d in docs_data:
        Document.objects.create(
            category=cats[d['cat']],
            code=d['code'],
            title=d['title'],
            unit=d['unit'],
            revision_number=d['rev'],
            download_count=d['downloads'],
            file_url="https://www.w3.org/WAI/ER/tests/xhtml/testfiles/resources/pdf/dummy.pdf"
        )
    print("  [+] Document verileri eklendi (9 adet).")

    # 4. Process Cards & Job Definitions
    ProcessCard.objects.all().delete()
    JobDefinition.objects.all().delete()

    proc_data = [
        {
            'code': 'SR.01',
            'name': 'Eğitim ve Öğretim Yönetim Süreci',
            'owner': 'Rektör Yardımcısı (Eğitim)',
            'purpose': 'Öğrenci odaklı, akredite ve YÖKAK standartlarına uygun lisans ve lisansüstü eğitim verilmesini sağlamak.',
            'inputs': 'YÖK Mevzuatı, Öğrenci Talepleri, Sektör İhtiyaçları, Akreditasyon Kriterleri',
            'outputs': 'Donanımlı Mezun Yetkinlikleri, Diploma, Akreditasyon Belgeleri, Ders Bilgi Paketleri',
            'kpi': 'Mezun İstihdam Oranı (%85), Öğrenci Memnuniyet Endeksi (4.2 / 5.0)',
        },
        {
            'code': 'SR.02',
            'name': 'Araştırma ve Geliştirme (Ar-Ge) Süreci',
            'owner': 'Rektör Yardımcısı (Ar-Ge & Proje)',
            'purpose': 'Üniversitenin bilimsel proje, uluslararası yayın ve patent kapasitesinin artırılması ve toplumsal katkı sağlanması.',
            'inputs': 'BAP Bütçesi, TÜBİTAK/AB Çağrıları, Araştırmacı Fikirleri, Sanayi İşbirliği Talepleri',
            'outputs': 'Uluslararası Bilimsel Makale (Q1/Q2), Patent, Faydalı Model, Proje Raporları',
            'kpi': 'Öğretim Üyesi Başına Düşen Yayın Sayısı (1.8), Dış Kaynaklı Proje Sayısı (45)',
        },
        {
            'code': 'SR.03',
            'name': 'Kalite Güvence ve PUKÖ Döngüsü Süreci',
            'owner': 'Kalite Koordinatörü',
            'purpose': 'Kurumsal değerlendirme, iç tetkik, risk yönetimi ve sürekli iyileştirme mekanizmalarının etkin şekilde işletilmesi.',
            'inputs': 'İç Değerlendirme Raporları, Paydaş Geri Bildirimleri, DİF Kayıtları, YÖKAK Geri Bildirim Raporu',
            'outputs': 'KİDR Raporu, İyileştirme Eylem Planları, ISO 9001 Belgesi, Kalite Kültürü',
            'kpi': 'DİF Kapatma Süresi (<20 gün), Birim Kalite Memnuniyet Endeksi (%92)',
        },
        {
            'code': 'SR.04',
            'name': 'Toplumsal Katkı ve Sosyal Sorumluluk Süreci',
            'owner': 'Toplumsal Katkı Koordinatörü',
            'purpose': 'Üniversitenin bilgi birikimi ve kaynaklarının bölge ve toplum yararına sosyal sorumluluk projeleriyle sunulması.',
            'inputs': 'Bölgesel İhtiyaçlar, STK Talepleri, Belediye İşbirlikleri, Gönüllü Öğrenci Kulüpleri',
            'outputs': 'Sosyal Sorumluluk Projeleri, Halk Açık Konferanslar, Sertifika Programları',
            'kpi': 'Yıllık Gerçekleştirilen Sosyal Proje Sayısı (35), Katılımcı Sayısı (5,000+)',
        },
    ]
    for p in proc_data:
        ProcessCard.objects.create(**p)
    print("  [+] ProcessCard verileri eklendi (4 adet).")

    job_data = [
        {
            'code': 'PP.2.3.GT.0583',
            'title': 'BAPKOB Birim Sorumlusu Görev Tanımı',
            'department': 'Bilimsel Araştırma Projeleri Koordinasyon Birimi',
            'responsibilities': 'BAP projelerinin başvuru, hakem değerlendirme ve satın alma süreçlerini yönetmek; komisyon kararlarını takip etmek ve raporlamak.',
            'qualifications': 'En az lisans mezunu olmak, üniversite mevzuatına ve 4734 sayılı kamu ihale kanununa hakim olmak, 5 yıl idari tecrübe.',
        },
        {
            'code': 'PP.1.1.GT.0102',
            'title': 'Fakülte Kalite Elçisi ve Komisyon Başkanı',
            'department': 'Fakülte Dekanlıkları',
            'responsibilities': 'Fakülte içi kalite çalışmalarını koordine etmek, akreditasyon belgelerini hazırlamak ve Kalite Koordinatörlüğü ile iletişimi sağlamak.',
            'qualifications': 'Fakülte bünyesinde tam zamanlı öğretim üyesi (Dr. Öğr. Üyesi, Doçent veya Profesör) olmak.',
        },
        {
            'code': 'PP.4.2.GT.0210',
            'title': 'Doküman Kontrol ve Arşiv Sorumlusu',
            'department': 'Kalite Koordinatörlüğü',
            'responsibilities': 'Sisteme yüklenen tüm prosedür, talimat ve formların standartlara uygunluğunu denetlemek, kodlamak ve revizyon numaralarını takip etmek.',
            'qualifications': 'Kalite yönetim sistemleri ve ISO 9001 konusunda sertifikalı eğitim almış olmak, büro yönetimi tecrübesi.',
        },
    ]
    for j in job_data:
        JobDefinition.objects.create(**j)
    print("  [+] JobDefinition verileri eklendi (3 adet).")

    # 5. Feedbacks
    Feedback.objects.all().delete()
    fb_data = [
        {
            'tracking_code': 'AVR2026A',
            'feedback_type': 'öneri',
            'user_type': 'öğrenci',
            'unit': 'Kütüphane ve Dokümantasyon Daire Başkanlığı',
            'name_surname': 'Merve Aydın (Bilgisayar Müh. 3. Sınıf)',
            'subject': 'Merkez Kütüphane Çalışma Saatlerinin Vize/Final Dönemlerinde 7/24 Yapılması',
            'message': 'Yaklaşan sınav dönemlerinde öğrencilerin sessiz çalışma ortamı bulabilmesi için merkez kütüphanenin 7/24 açık olmasını ve gece çorba ikramı yapılmasını önermekteyiz.',
            'status': 'cozuldu',
            'admin_response': 'Sayın Öğrencimiz, öneriniz Kalite Koordinatörlüğü ve Kütüphane Daire Başkanlığı tarafından değerlendirilmiş olup; Senato kararıyla sınav haftalarında 7/24 açık kütüphane uygulamasına geçilmiştir. Katkınız için teşekkür ederiz.',
        },
        {
            'tracking_code': 'AVR2026B',
            'feedback_type': 'şikayet',
            'user_type': 'akademik',
            'unit': 'Bilgi İşlem Daire Başkanlığı',
            'name_surname': 'Dr. Öğr. Üyesi K. Y.',
            'subject': 'Mühendislik Fakültesi B Blok Wi-Fi ve Eduroam Bağlantı Kopmaları',
            'message': 'B Blok 2. kat dersliklerinde eduroam kablosuz ağ bağlantısı sık sık kopmaktadır. Ders esnasında çevrimiçi sunum yaparken aksaklık yaşanmaktadır.',
            'status': 'islemde',
            'admin_response': 'Sayın Hocam, bildiriminiz alınmıştır. Bilgi İşlem teknik ekibimiz B Blok 2. kat erişim noktalarında (Access Point) sinyal ölçümü yapmakta olup, ek cihaz montajı planlanmıştır.',
        },
        {
            'tracking_code': 'AVR2026C',
            'feedback_type': 'takdir',
            'user_type': 'dış',
            'unit': 'Öğrenci İşleri Daire Başkanlığı',
            'name_surname': 'Ahmet K. (Mezun)',
            'subject': 'E-Devlet Üzerinden Diploma Eki ve Transkript Alma Kolaylığı',
            'message': 'Yurtdışı yüksek lisans başvurum için acil ihtiyaç duyduğum İngilizce transkript ve diploma ekini e-devlet entegrasyonu sayesinde saniyeler içinde aldım. Emeği geçen personele teşekkür ederim.',
            'status': 'cozuldu',
            'admin_response': 'Sayın Mezunumuz, güzel düşünceleriniz ve takdiriniz için teşekkür eder, eğitim ve kariyer hayatınızda başarılar dileriz.',
        },
    ]
    for f in fb_data:
        Feedback.objects.create(**f)
    print("  [+] Feedback verileri eklendi (3 adet, takip kodları: AVR2026A, AVR2026B, AVR2026C).")

    # 6. DIF Records
    DifRecord.objects.all().delete()
    dif_data = [
        {
            'code': 'DİF.2026.001',
            'title': 'Laboratuvar İş Güvenliği Levhaları ve Acil Göz Yıkama İstasyonu Eksikliği',
            'unit': 'Mühendislik ve Mimarlık Fakültesi',
            'finding_type': 'iç_tetkik',
            'root_cause': 'Yıllık bütçe planlamasında sarf malzeme ve uyarı levhalarının revizyonunun gözden kaçırılması.',
            'action_plan': 'Tüm laboratuvarlar için ISO standartlarına uygun iş güvenliği uyarı levhalarının asılması ve acil müdahale göz duşu istasyonlarının periyodik bakımlarının tamamlanması.',
            'responsible_person': 'Prof. Dr. Ahmet Yılmaz (Dekan Yrd.)',
            'target_date': date(2026, 8, 15),
            'status': 'devam',
        },
        {
            'code': 'DİF.2026.002',
            'title': 'Kütüphane Dijital Veritabanı Kampüs Dışı Uzaktan Erişim Ağ Sorunları',
            'unit': 'Kütüphane ve Dokümantasyon Daire Başkanlığı',
            'finding_type': 'paydaş',
            'root_cause': 'Proxy sunucu SSL sertifikasının zaman aşımına uğraması ve eşzamanlı VPN tünel limitlerinin dolması.',
            'action_plan': 'Yeni nesil EzProxy sınırsız kullanıcı lisansının alınması ve videolu uzaktan erişim kılavuzunun yayınlanması.',
            'responsible_person': 'Ömer Faruk Kaya (Daire Başkanı)',
            'target_date': date(2026, 6, 30),
            'status': 'kapali',
            'closed_at': date(2026, 6, 25),
        },
        {
            'code': 'DİF.2026.003',
            'title': 'Atık Yönetim Planı ve Sıfır Atık Kutularının Katlarda Konumlandırılması',
            'unit': 'İdari ve Mali İşler Daire Başkanlığı',
            'finding_type': 'dış_tetkik',
            'root_cause': 'Eski binalarda geri dönüşüm ayrıştırma üniteleri için yeterli fiziki alan ayrılmaması.',
            'action_plan': 'Çevre ve Şehircilik Bakanlığı Sıfır Atık Yönetmeliğine uygun olarak 4lü ayrıştırma kutularının tüm koridorlara yerleştirilmesi ve personelin bilgilendirilmesi.',
            'responsible_person': 'Hakan Çelik (Destek Hizmetleri Şube Mdr.)',
            'target_date': date(2026, 9, 1),
            'status': 'dogrulama',
        },
    ]
    for dr in dif_data:
        DifRecord.objects.create(**dr)
    print("  [+] DifRecord verileri eklendi (3 adet).")

    print("\n>>> TEBRİKLER! Avrasya Üniversitesi Kalite Yönetim Sistemi (Avrasya KYS) veri yüklemesi başarıyla tamamlandı!")
    print(">>> Test İçin Önerilen Takip Kodları: AVR2026A, AVR2026B, AVR2026C")

if __name__ == '__main__':
    run_seed()
