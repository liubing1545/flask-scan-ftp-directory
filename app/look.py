from . import celery
import scan


@celery.task
def scan_async_ftp_folder():
    scan.send()


def send_email(to, subject, template, **kwargs):
   scan_async_ftp_folder.delay()