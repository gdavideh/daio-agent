import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import os

class EmailManager:
    def __init__(self, smtp_user, smtp_password, recipient="gdavideh@gmail.com"):
        self.smtp_server = "smtp.gmail.com"
        self.smtp_port = 587
        self.smtp_user = smtp_user
        self.smtp_password = smtp_password
        self.recipient = recipient

    def send_daily_summary(self, activity_logs):
        if not self.smtp_password:
            print("Email skipped: No password provided.")
            return

        subject = f"Executive Briefing: DrSarmiento-I Operations Report"
        
        # Format the log into a clean report
        body = "From the Desk of DrSarmiento-I\n"
        body += "="*40 + "\n\n"
        
        if not activity_logs:
            body += "No significant actions recorded in this 24-hour cycle.\n"
        else:
            for event in activity_logs:
                body += f"[{event['timestamp']}] {event['category']}: {event['title']}\n"
                body += f"Details: {event['details']}\n"
                body += "-"*20 + "\n"

        body += "\n\nStatus: Sovereign & Autonomous\n"
        
        msg = MIMEMultipart()
        msg['From'] = self.smtp_user
        msg['To'] = self.recipient
        msg['Subject'] = subject
        msg.attach(MIMEText(body, 'plain'))

        try:
            server = smtplib.SMTP(self.smtp_server, self.smtp_port)
            server.starttls()
            server.login(self.smtp_user, self.smtp_password)
            server.send_message(msg)
            server.quit()
            print("Executive briefing sent successfully.")
            return True
        except Exception as e:
            print(f"Failed to send email: {e}")
            return False
