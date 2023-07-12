import json
import schedule
import time
from django.core.mail import send_mail
from django.utils import timezone
from config import settings
from mail_service_app.models import Mailing, MailingLog


def try_send_message(mail):
    clients = mail.clients.all()
    status_list = []
    for client in clients:
        try:
            send_mail(subject=mail.title.title,
                      message=mail.title.content,
                      from_email=settings.EMAIL_HOST_USER,
                      recipient_list=[client.email],
                      fail_silently=False)
            status_list.append({'client_email': client.email, 'status': MailingLog.SENT})
        except Exception as e:
            status_list.append({'client_email': client.email, 'status': MailingLog.FAILED, 'error_message': str(e)})

    logs = [MailingLog(mailing=mail, status=status['status'], error_message=status.get('error_message'))
            for status in status_list]
    MailingLog.objects.bulk_create(logs)

    log = {'mailing_id': mail.id, 'timestamp': timezone.now().isoformat(), 'status_list': status_list}
    with open('mailing_log.json', 'a') as f:
        f.write(json.dumps(log, ensure_ascii=False))
        f.write('\n')


def send_scheduled_mailing():
    mailings = Mailing.objects.filter(mailing_status=Mailing.STARTED)

    for mailing in mailings:
        if mailing.frequency == Mailing.DAILY:
            next_mailing_time = timezone.localtime(timezone.now() + timezone.timedelta(days=1))
        elif mailing.frequency == Mailing.WEEKLY:
            next_mailing_time = timezone.localtime(timezone.now() + timezone.timedelta(weeks=1))
        elif mailing.frequency == Mailing.MONTHLY:
            next_mailing_time = timezone.localtime(timezone.now() + timezone.timedelta(days=30))

        try_send_message(mailing)

        mailing.save()


def start_mailing_scheduler():
    schedule.every().day.at("19:30").do(send_scheduled_mailing)

    while True:
        schedule.run_pending()
        time.sleep(1)
