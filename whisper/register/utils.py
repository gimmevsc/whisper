import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from random import randint

def send_verification_code(email):
    sender_email = 'noreply.whispercode@gmail.com'
    sender_password = 'jhbi pzln sxbo nozu'
    smtp_server = 'smtp.gmail.com'
    smtp_port = 587
    code = int(str(randint(0,9))+str(randint(0,9))+str(randint(0,9))+str(randint(0,9))+str(randint(0,9))+str(randint(0,9)))
    
    subject = 'Verification Code'
    message = f'Your verification code is: {code}'
    
    msg = MIMEMultipart()
    msg['From'] = 'Whisper'
    msg['To'] = email
    msg['Subject'] = subject
    msg.attach(MIMEText(message, 'plain'))
    
    with smtplib.SMTP(smtp_server, smtp_port) as server:
        server.starttls()
        server.login(sender_email, sender_password)
        server.sendmail(sender_email, email, msg.as_string())
    
    print(code)
    
    return code

