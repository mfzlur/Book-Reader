from celery import shared_task
from send_email import send_email, send_month_email
import time

from datetime import datetime, timedelta




# celery test function
@shared_task(ignore_result=False)
def send_email_using_celery(name, email):
    print("celery task initiated")
    time.sleep(10)
    output = send_email(name, email)
    
    return output

# celery beat function
@shared_task(ignore_result=False)
def auto_book_return():
    from app import db, Request
    all_requests = Request.query.all()
    for req in all_requests:
        if req.status == 'approved':
            if datetime.now() - req.date_requested > timedelta(days=7):
                req.status = 'revoked'
                db.session.commit()

    return "Task Executed Successfully"


@shared_task(ignore_result=False)
def send_monthly_report():
    print("celery task initiated")
    time.sleep(10)
    output = send_month_email()
    
    return output




