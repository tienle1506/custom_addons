from odoo import models, fields, api
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.header import Header


class MyMailSender(models.Model):
    _name = 'my.mail.sender'

    def send_mail_to_customer(self, email_sent, header, mail_content):
        # Cấu hình thông tin email
        email = 'nhatnt1008@gmail.com'
        password = 'llorhubemcmuidsi'
        smtp_server = 'smtp.gmail.com'
        smtp_port = 587

        # Kết nối đến máy chủ SMTP
        with smtplib.SMTP(smtp_server, smtp_port) as session:
            session.starttls()
            session.login(email, password)

            for recipient_email in email_sent:
                # Tạo đối tượng MIMEMultipart
                msg = MIMEMultipart()

                # Thêm tiêu đề email
                msg['From'] = email
                msg['To'] = recipient_email
                msg['Subject'] = Header(header, 'utf-8')

                # Thêm nội dung email
                body = MIMEText(mail_content, 'plain', 'utf-8')
                msg.attach(body)

                # Gửi email
                session.send_message(msg)

        print("Email sent successfully!")