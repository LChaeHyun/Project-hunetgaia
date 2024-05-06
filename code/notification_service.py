import smtplib
from email.message import EmailMessage


def send_email(subject,reciver,cctv):
    smtp = smtplib.SMTP_SSL('smtp.gmail.com', 465)
    EMAIL_ADDR = 'testhunetgaia@gmail.com'
    smtp.login(EMAIL_ADDR, 'kfzxrsvnqitwnrab')
    message = EmailMessage()
    message.set_content(cctv)
    message["Subject"] = subject
    message["From"] = EMAIL_ADDR  
    message["To"] = reciver
    smtp.send_message(message)
    smtp.quit()

send_email('[화재감지]','받는 이메일 주소','화재가 발생하였습니다')