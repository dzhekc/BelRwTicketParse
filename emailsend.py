from email.message import EmailMessage
from pydantic import EmailStr


def create_email_massage(tickets: dict, email_to: EmailStr):
    email_massage = EmailMessage()
    email_massage['Subject'] = 'Доступен билет'
    email_massage['From'] = email_to
    email_massage['To'] = email_to


    email_massage.set_content(

    )

    return email_massage