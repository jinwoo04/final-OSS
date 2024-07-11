import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders
import os
from dotenv import load_dotenv


def send_email(filename, send_mail):
    load_dotenv()
    DIR_PATH = 'upload'

    # 이메일 아이디 비밀번호
    send_email = ''.join(os.environ.get('ID'))
    send_pwd = os.environ.get('PW')
    recv_email = ''.join(send_mail)

    # 네이버 포트번호
    smtp_name = "smtp.naver.com"
    smtp_port = 587

    # 멘트 (내용)
    text = "금일 지역별 날씨 입니다."

    # 제목 (타이틀)
    msg = MIMEMultipart()
    msg['Subject'] = "지역별 날씨 데이터 메일"
    msg['From'] = send_email
    msg['To'] = recv_email

    # 이메일 파일 첨부 해서 보내는 코드
    msg.attach(MIMEText(text, 'plain', 'utf-8'))

    # 파일 읽기 및 첨부
    attachment = open(filename, 'rb')
    part = MIMEBase('application', 'octet-stream')
    part.set_payload(attachment.read())
    encoders.encode_base64(part)
    part.add_header('Content-Disposition', f"attachment; filename=weather.zip")
    msg.attach(part)

    email_string = msg.as_string()

    # 이메일 보내기
    s = smtplib.SMTP(smtp_name, smtp_port)
    s.starttls()
    s.login(send_email, send_pwd)
    s.sendmail(send_email, recv_email, email_string)
    s.quit()