from email.mime.image import MIMEImage
import smtplib
import ssl
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.application import MIMEApplication
from os.path import basename
import time
port = 465
stmp_host = "smtp.gmail.com"
password = "1234567@A"
sender_mail = "mprcashflow@gmail.com"


def send_mail(receiver, msg):
    receiver_mail = [receiver]
    message = MIMEMultipart("alternative")
    message["Subject"] = "Forgot Password"
    message["From"] = sender_mail
    s = msg
    # html_message = f"""
    #             <html>
    #                 <body>
    #                 You have forgotten your password,this is the key : {s}
    #                 </body>
    #             </html>
    #         """
    html_message = f"{s}\n\nSent on {time.ctime()}"
    with open('capture.jpg', 'rb') as f:
        image_data = f.read()
    image = MIMEImage(image_data, name=basename('saved_img'))
    mimeHTML = MIMEText(html_message, "html")
    message.attach(mimeHTML)
    message.attach(image)
    context = ssl.create_default_context()
    with smtplib.SMTP_SSL(stmp_host, port, context=context) as server:
        server.login(sender_mail, password)
        for receiver in receiver_mail:
            message["To"] = receiver
            server.sendmail(sender_mail, receiver, message.as_string())
            print(f"mail sent to: {receiver}")
            server.close()

def send_text(receiver,msg):
    receiver_mail = [receiver]
    message = MIMEMultipart("alternative")
    message["Subject"] = "You have exceeded your montly limit!"
    message["From"] = sender_mail
    s = msg
    html_message = f"{s}\n\nSent on {time.ctime()}"
    mimeHTML = MIMEText(html_message, "html")
    message.attach(mimeHTML)
    context = ssl.create_default_context()
    with smtplib.SMTP_SSL(stmp_host, port, context=context) as server:
        server.login(sender_mail, password)
        for receiver in receiver_mail:
            message["To"] = receiver
            server.sendmail(sender_mail, receiver, message.as_string())
            print(f"mail sent to: {receiver}")
            server.close()

def forgot_password(email,key):
    msg = f"Your access key is : {key}"
    receiver_mail = [email]
    message = MIMEMultipart("alternative")
    message["Subject"] = "Forgot Password"
    message["From"] = sender_mail
    s = msg
    html_message = f"{s}\n\nSent on {time.ctime()}"
    mimeHTML = MIMEText(html_message, "html")
    message.attach(mimeHTML)
    context = ssl.create_default_context()
    with smtplib.SMTP_SSL(stmp_host, port, context=context) as server:
        server.login(sender_mail, password)
        for receiver in receiver_mail:
            message["To"] = receiver
            server.sendmail(sender_mail, receiver, message.as_string())
    print("mail sent")
    server.close()
# send_mail('mskasan30@gmail.com', 'hello')
