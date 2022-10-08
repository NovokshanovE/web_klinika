import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.image import MIMEImage
def send_massege(addr_to, time, day, user, doctor):
    addr_from = "testtesttest80@bk.ru"
    password  = "Fuckgg123"

    msg = MIMEMultipart()
    msg['From']    = addr_from
    msg['To']      = addr_to
    msg['Subject'] = 'Запись на прием'

    body = f"Уважаемый, {user}! Вы записаны на прием к {doctor} на {time} {day}"
    msg.attach(MIMEText(body, 'plain'))


    smtpObj = smtplib.SMTP_SSL('smtp.mail.ru', 465)
    smtpObj.login(addr_from, password)
    smtpObj.send_message(msg)

