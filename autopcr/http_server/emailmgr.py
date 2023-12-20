import aiosmtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.header import Header

class EmailManager:
    def __init__(self, smtp_server, smtp_port, username, password, use_tls=True):
        self.smtp_server = smtp_server
        self.smtp_port = smtp_port
        self.username = username
        self.password = password
        self.use_tls = use_tls

    async def send_email(self, to, subject, body):
        message = MIMEMultipart()
        message['From'] = self.username
        message['To'] = to
        message['Subject'] = Header(subject, 'utf-8')

        text = MIMEText(body, 'plain', 'utf-8')
        message.attach(text)

        try:
            async with aiosmtplib.SMTP(
                host=self.smtp_server,
                port=self.smtp_port,
                use_tls=self.use_tls,
                start_tls=self.use_tls
            ) as server:
                await server.login(self.username, self.password)
                await server.sendmail(self.username, to, message.as_string())

            print("Email sent successfully")
        except Exception as e:
            raise ValueError(f"Failed to send email: {str(e)}")

instance = EmailManager("", "", "", "")
