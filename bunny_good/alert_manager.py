import smtplib
from email.mime.text import MIMEText
import ssl

from bunny_good.config import Config


class AlertManager:
    def __init__(self):
        self.__server = smtplib.SMTP_SSL(
            host="smtp.gmail.com",
            port=465,
            context=ssl.create_default_context(),
            timeout=10,
        )
        self.__server.login(Config.GMAIL_MAIL, Config.GMAIL_API_KEY)
        self.from_mail = Config.GMAIL_MAIL
        self.alert_to = Config.GMAIL_ALERT_TO
        self.title_prfix = "[BUNNY ALERT]"

    def __del__(self):
        pass
        # self.__server.quit()

    def send_alert(self, title: str, content: str) -> bool:
        msg = MIMEText(content, "plain")
        msg["Subject"] = f"{self.title_prfix} {title}"
        msg["To"] = self.alert_to
        msg["From"] = self.from_mail
        result = self.__server.send_message(msg)
        if result:
            return False
        else:
            return True
