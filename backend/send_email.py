import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
from io import BytesIO
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas


# Email configuration
smtp_server = 'smtp.gmail.com'
smtp_port = 587
smtp_username = '23f1001897@ds.study.iitm.ac.in'
smtp_password = 'fxxk uaap stft mgaz'


def send_email(name, email):
    # Create the email message
    
    msg = MIMEMultipart()
    msg['From'] = smtp_username
    msg['To'] = email
    msg['Subject'] = f'Hey There {name}!'

    # Body of the email
    body = 'This is the body of the email.'
    msg.attach(MIMEText(body, 'plain'))



    # Send the email

    try:
        server = smtplib.SMTP(smtp_server, smtp_port)
        server.starttls()
        server.login(smtp_username, smtp_password)
        text = msg.as_string()
        server.sendmail(smtp_username, email, text)
        return "Email sent successfully!! Check your inbox"
    except Exception as e:
        return f"Failed to send email: {e}"
    finally:
        server.quit()



def send_month_email():
    # Fetch the counts from the database
    from app import User, Book, Request, Section
    total_books = Book.query.count()
    total_users = User.query.count()
    total_requests = Request.query.count()
    total_sections = Section.query.count()

    # Email content
    email_body = (
        f"Monthly Report\n\n"
        f"Total Books: {total_books}\n"
        f"Total Users: {total_users}\n"
        f"Total Requests: {total_requests}\n"
        f"Total Sections: {total_sections}\n"
    )

    # Create the email message
    msg = MIMEMultipart()
    msg['From'] = smtp_username
    msg['To'] = 'mfzlur@gmail.com'
    msg['Subject'] = 'Monthly Report'

    # Attach the body of the email
    msg.attach(MIMEText(email_body, 'plain'))

    # Generate PDF in memory
    pdf_buffer = BytesIO()
    c = canvas.Canvas(pdf_buffer, pagesize=letter)
    c.drawString(100, 750, "Monthly Report")
    c.drawString(100, 730, f"Total Books: {total_books}")
    c.drawString(100, 710, f"Total Users: {total_users}")
    c.drawString(100, 690, f"Total Requests: {total_requests}")
    c.drawString(100, 670, f"Total Sections: {total_sections}")
    c.save()

    # Move the buffer position to the beginning
    pdf_buffer.seek(0)

    # Attach PDF to email
    part = MIMEBase('application', 'octet-stream')
    part.set_payload(pdf_buffer.read())
    encoders.encode_base64(part)
    part.add_header('Content-Disposition', 'attachment; filename="Monthly_Report.pdf"')
    msg.attach(part)

    # Send the email
    try:
        server = smtplib.SMTP(smtp_server, smtp_port)
        server.starttls()
        server.login(smtp_username, smtp_password)
        text = msg.as_string()
        server.sendmail(smtp_username, 'mfzlur@gmail.com', text)
        return "Email sent successfully! Check your inbox."
    except Exception as e:
        return f"Failed to send email: {e}"
    finally:
        server.quit()
