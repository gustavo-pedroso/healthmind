import json
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from project_utils import *


class EmailUtil:

    def __init__(self, email_info_json, json_api_info):
        self.json_api_info = json_api_info

        with open(email_info_json) as fp:
            self.email_info_json = json.load(fp)

    def send_email(self, msg, sentiment):
        try:
            message = MIMEMultipart()
            message["From"] = self.email_info_json['from']
            message["To"] = self.email_info_json['to']
            message["Subject"] = f"{self.email_info_json['subject']} - ({sentiment})"
            message.attach(MIMEText(msg, "plain"))
            message.attach(MIMEText(get_room_readings_message(), "plain"))
            message.attach(MIMEText(get_local_weather(self.json_api_info), "plain"))
            message.attach(MIMEText(get_last_reboot_log_message(), "plain"))

            server = smtplib.SMTP('smtp.office365.com', 587)
            server.ehlo()
            server.starttls()
            server.login(self.email_info_json['login'], self.email_info_json['password'])
            server.sendmail(self.email_info_json['from'], self.email_info_json['to'], message.as_string())
            server.quit()
        except Exception as e:
            print(e)
