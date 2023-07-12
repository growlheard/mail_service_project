import time

import schedule
from django.core.management import BaseCommand

from users.management.commands.tasks import start_mailing_scheduler


class Command(BaseCommand):

    def handle(self, *args, **options):
        start_mailing_scheduler()
        while True:
            schedule.run_pending()
            time.sleep(1)
