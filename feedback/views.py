from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.core.mail import send_mail
from django.conf import settings
from .models import Feedback

def feedback_create(request):
    if request.method == 'POST':
        feedback_type = request.POST.get('feedback_type', 'öneri')
        user_type = request.POST.get('user_type', 'öğrenci')
        unit = request.POST.get('unit', 'Genel')
        name_surname = request.POST.get('name_surname', 'Anonim Paydaş') or 'Anonim Paydaş'
        email = request.POST.get('email', '')
        subject = request.POST.get('subject', '')
        message_text = request.POST.get('message', '')
        
        if subject and message_text:
            fb = Feedback.objects.create(
                feedback_type=feedback_type,
                user_type=user_type,
                unit=unit,
                name_surname=name_surname,
                email=email,
                subject=subject,
                message=message_text
            )
            
            # ------------------------------------------------------------------
            # Office 365 SMTP ile Otomatik E-Posta Bildirimlerinin Gönderilmesi
            # ------------------------------------------------------------------
            try:
                sender_email = getattr(settings, 'DEFAULT_FROM_EMAIL', 'ramin.entezar@avrasya.edu.tr')
                site_url = getattr(settings, 'SITE_URL', 'https://www.avrasya.edu.tr')
                
                # 1. Yöneticiye / Kalite Koordinatörüne Bildirim E-Postası (ramin.entezar@avrasya.edu.tr)
                admin_subject = f"[YENİ KYS BİLDİRİMİ] {fb.get_feedback_type_display().upper()} - {subject}"
                admin_message = (
                    f"Sayın Kalite Koordinatörü,\n\n"
                    f"Avrasya Üniversitesi KYS Portalına yeni bir paydaş bildirimi ulaşmıştır.\n\n"
                    f"📌 Takip Kodu: {fb.tracking_code}\n"
                    f"🏷️ Bildirim Türü: {fb.get_feedback_type_display()}\n"
                    f"👤 Paydaş: {name_surname} ({fb.get_user_type_display()})\n"
                    f"🏢 İlgili Birim: {unit}\n"
                    f"📧 E-Posta: {email or 'Belirtilmedi'}\n"
                    f"📋 Konu Başlığı: {subject}\n\n"
                    f"💬 Mesaj Detayı:\n{message_text}\n\n"
                    f"Yönetici Panelinden İncelemek ve Durumunu Değiştirmek İçin:\n"
                    f"http://127.0.0.1:8000/admin/feedback/feedback/{fb.id}/change/\n\n"
                    f"-----------------------------------------\n"
                    f"Avrasya Üniversitesi Kalite Yönetim Sistemi (v2.0)\n"
                    f"{site_url}"
                )
                send_mail(
                    subject=admin_subject,
                    message=admin_message,
                    from_email=sender_email,
                    recipient_list=[sender_email],
                    fail_silently=True
                )
                
                # 2. Paydaşa (Geri Bildirim Sahibine) Alındı / Takip E-Postası
                if email:
                    user_subject = f"[Avrasya KYS] Geri Bildiriminiz Alındı - Takip No: {fb.tracking_code}"
                    user_message = (
                        f"Sayın {name_surname},\n\n"
                        f"Avrasya Üniversitesi Kalite Yönetim Sistemi (KYS) paydaş geri bildirim formunu doldurduğunuz için teşekkür ederiz.\n"
                        f"Görüş, öneri veya şikayetiniz başarıyla sistemimize kaydedilmiş olup, ilgili kalite komisyonu tarafından incelenecektir.\n\n"
                        f"🏷️ Bildirim Türü: {fb.get_feedback_type_display()}\n"
                        f"📌 Takip Kodunuz: {fb.tracking_code}\n"
                        f"📋 Konu: {subject}\n\n"
                        f"Bildiriminizi ve çözüm durumunu aşağıdaki bağlantıdan anlık olarak takip edebilirsiniz:\n"
                        f"http://127.0.0.1:8000/feedback/track/?code={fb.tracking_code}\n\n"
                        f"Katkılarınız için teşekkür eder, iyi günler dileriz.\n\n"
                        f"Saygılarımızla,\n"
                        f"Avrasya Üniversitesi Kalite Koordinatörlüğü\n"
                        f"{site_url}"
                    )
                    send_mail(
                        subject=user_subject,
                        message=user_message,
                        from_email=sender_email,
                        recipient_list=[email],
                        fail_silently=True
                    )
            except Exception:
                # Olası SMTP bağlantı veya ağ hataları kullanıcının kayıt akışını engellememeli
                pass

            return redirect('feedback_success', tracking_code=fb.tracking_code)
            
    return render(request, 'feedback/feedback_create.html')


def feedback_success(request, tracking_code):
    fb = get_object_or_404(Feedback, tracking_code=tracking_code)
    return render(request, 'feedback/feedback_success.html', {'feedback': fb})


def feedback_track(request):
    code = request.GET.get('code', '').strip().upper()
    feedback = None
    searched = False
    
    if code:
        searched = True
        feedback = Feedback.objects.filter(tracking_code=code).first()
        
    return render(request, 'feedback/feedback_track.html', {
        'code': code,
        'feedback': feedback,
        'searched': searched,
    })
