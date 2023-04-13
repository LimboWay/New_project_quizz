from datetime import timedelta
from celery import shared_task
from celery.utils.log import get_task_logger
from django.core.management import call_command
from django.utils import timezone
from prettytable import PrettyTable
from .models import Result

logger = get_task_logger(__name__)


@shared_task
def simple_task():
    logger.info('>>> SIMPLE TASK <<<')


@shared_task
def send_email_report():
    call_command('send_report')


@shared_task
def send_complete_checker():
    start = timezone.now() - timedelta(days=7)
    end = timezone.now() + timedelta(days=1)
    results = Result.objects.filter(create_timestamp__range=(start, end), state=0).order_by('user')

    if results:
        tab_fields = ['Test', 'Start Date']
        user_results = {}
        for result in results:
            user_results.setdefault(result.user, []).append([result.exam.title, result.create_timestamp.strftime('%Y-%m-%d %H:%M')])

        for user, results_ in user_results.items():
            tab = PrettyTable(field_names=tab_fields)
            tab.add_rows(rows=results_)

            subject = 'You have unfinished exams.'
            body = tab.get_string()
            user.email_user(subject=subject, message=body)

        logger.info('>>> Results was sent. <<<')

    else:
        logger.info('>>> Nothing to send. <<<')
