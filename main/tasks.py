from celery import shared_task
from django.core.mail import send_mail
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string


@shared_task
def send_mail_to_email(user, email, favor, content):
    data = {
        'user': user,
        "email": email,
        'content': content,
        'favor': favor,
        # 'phone_number': phone_number
    }
    html_body = render_to_string('h.html', data)
    msg = EmailMultiAlternatives(subject='Вашей услугой заинтересовались!', to=[email])
    msg.attach_alternative(html_body, 'text/html')
    msg.send()
    print(msg)
 
    #send_mail(subject=full_name,
    #message=f'{message}\n\n{phone_number}',
    #recipient_list=[email, ],
    #from_email=None)
