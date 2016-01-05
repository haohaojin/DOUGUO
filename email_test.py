import smtplib
from email.mime.text import MIMEText

msg = MIMEText("The body of the email is here")
msg['Subject'] = "An Email Alert"
msg['From'] = "python@breadmum.com"
msg['To'] = "hao.jin@outlook.com"
s = smtplib.SMTP('mail.breadmum.com')
s.login('python@breadmum.com','python')
s.send_message(msg)
s.quit()