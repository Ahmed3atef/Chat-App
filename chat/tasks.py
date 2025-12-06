from time import sleep
from django.core.mail import send_mail, BadHeaderError
from celery import shared_task

@shared_task
def notify_customers(message):
    print("Sending 10k emails...")
    print(message)
    for i in range(10):
        try:
            send_mail('subject', message, 'info@email.com',['targe@email.com'])
        except BadHeaderError:
            pass
    print('Email were successfully sent!')