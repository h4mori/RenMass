import smtplib
from email.mime.text import MIMEText
from email.header import Header

def send(data: list, message: list, recipients: list) -> bool:
    try:
        msg = MIMEText(message[1], 'plain', 'utf-8')
        msg['Subject'] = Header(message[0], 'utf-8')
        msg['From'] = data[2]
        msg['To'] = ', '.join(recipients)
        if data[1] == 465:
            with smtplib.SMTP_SSL(data[0], data[1]) as server:
                server.login(data[2], data[3])
                server.sendmail(data[2], recipients, msg.as_string())
        else:
            with smtplib.SMTP(data[0], data[1]) as server:
                server.starttls()
                server.login(data[2], data[3])
                server.sendmail(data[2], recipients, msg.as_string())
        return True
    except Exception as e:
        print(f"Ошибка отправки: {e}")
        return False