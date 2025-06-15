# email 생성 함수
def send_email(to, subject, body):
    from email.utils import formatdate
    from email.mime.multipart import MIMEMultipart
    from email.header import Header
    # 메일 제목과 내용을 설정하는 모듈
    from email.mime.text import MIMEText
    
    msg = MIMEMultipart()

    port = 465  # For SSL
    smtp_server = "smtp.gmail.com"
    sender_email = "xxcompany@xxx.com" 
    receiver_email = to

    msg['From'] = sender_email 
    msg['To'] = receiver_email 
    msg['Date'] = formatdate(localtime=True)

    msg['Subject'] = Header(s=subject, charset='utf-8')
    body = MIMEText(body, _charset='utf-8')
    msg.attach(body)
        
    return f"{to} 에게 성공적으로 메일 발송"