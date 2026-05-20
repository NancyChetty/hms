import json
import smtplib
from email.mime.text import MIMEText


SENDER_EMAIL = "yourgmail@gmail.com"
SENDER_PASSWORD = "yourapppassword"


def send_email(event, context):

    body = json.loads(event['body'])

    email_type = body.get('type')
    receiver_email = body.get('email')

    if email_type == 'SIGNUP_WELCOME':
        subject = 'Welcome to HMS'
        message = f"Welcome {body.get('username')}"

    elif email_type == 'BOOKING_CONFIRMATION':
        subject = 'Booking Confirmed'
        message = f"Appointment booked with Dr. {body.get('doctor')} at {body.get('time')}"

    else:
        subject = 'Notification'
        message = 'Unknown event'

    msg = MIMEText(message)
    msg['Subject'] = subject
    msg['From'] = SENDER_EMAIL
    msg['To'] = receiver_email

    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.starttls()
    server.login(SENDER_EMAIL, SENDER_PASSWORD)

    server.sendmail(
        SENDER_EMAIL,
        receiver_email,
        msg.as_string()
    )

    server.quit()

    return {
        'statusCode': 200,
        'body': json.dumps('Email sent successfully')
    }