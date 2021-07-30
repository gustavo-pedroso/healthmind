import json
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText


class EmailUtil:

    def __init__(self, email_info_json):
        with open(email_info_json) as fp:
            print(email_info_json)
            self.email_info_json = json.load(fp)

    def send_email(self, msg):
        try:
            message = MIMEMultipart()
            message["From"] = self.email_info_json['from']
            message["To"] = self.email_info_json['to']
            message["Subject"] = self.email_info_json['subject']
            message.attach(MIMEText(msg, "plain"))

            server = smtplib.SMTP('smtp.office365.com', 587)
            server.ehlo()
            server.starttls()
            server.login(self.email_info_json['login'], self.email_info_json['password'])
            server.sendmail(self.email_info_json['from'], self.email_info_json['to'], message.as_string())
            server.quit()
        except Exception as e:
            print(e)
