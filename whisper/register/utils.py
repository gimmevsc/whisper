import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from random import randint
from datetime import timedelta
from re import match
from django.db.models.signals import pre_delete
from django.utils import timezone
from django.dispatch import receiver
from django.contrib.auth.models import User 

def send_verification_code(email, email_goal, email_main):
    sender_email = 'noreply.whispercode@gmail.com'
    sender_password = 'jhbi pzln sxbo nozu'
    smtp_server = 'smtp.gmail.com'
    smtp_port = 587
    
    code = str(str(randint(0,9))+str(randint(0,9))+str(randint(0,9))+str(randint(0,9))+str(randint(0,9))+str(randint(0,9)))
    
    
    with open('register/email.html', 'r') as file:
        html_template = file.read()

    # Replace the placeholder with the actual code
    html_message = html_template.replace('{{ code }}', code).replace('{{ email_goal }}', email_goal).replace('{{ email_main }}', email_main)
    

    # Email subject and message
    subject = 'Verification Code'
    plain_message = f'Your verification code is: {code}'

    msg = MIMEMultipart('alternative')
    msg['From'] = sender_email
    msg['To'] = email
    msg['Subject'] = subject

    # Attach both plain text and HTML versions
    msg.attach(MIMEText(plain_message, 'plain'))
    msg.attach(MIMEText(html_message, 'html'))

    try:
        with smtplib.SMTP(smtp_server, smtp_port) as server:
            server.starttls()
            server.login(sender_email, sender_password)
            server.sendmail(sender_email, email, msg.as_string())
    except Exception as e:
        print(f"Failed to send email: {e}")
        return None

    return code


def is_valid_email_funct(email):
    regex = r'^.+@.+$'
    if match(regex, email):
        return True
    return False



def is_code_expired(created_at):
    expiration_time = created_at + timedelta(minutes=5) 
    return timezone.now() > expiration_time



def user_profile_picture_path(instance, filename):

    # user_id = instance.user_id
    
    username = instance.username
    
    ext = filename.split('.')[-1]

    # Construct the upload path: profile_pictures/user_id/filename.ext
    return f'profile_pictures/{username}/{username}.{ext}'


@receiver(pre_delete, sender=User)
def delete_profile_picture(sender, instance, **kwargs):
    # Check if profile_picture field exists on the User model
    if hasattr(instance, 'profile_picture'):
        # Delete the profile picture file from storage
        if instance.profile_picture:
            instance.profile_picture.delete(save=False)