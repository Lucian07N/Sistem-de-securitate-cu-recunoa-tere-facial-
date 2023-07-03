import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders
import os
import glob
def send_video_email(sender_email, sender_password, receiver_email, video_directory):
 # Configurarea detaliilor de autentificare SMTP
 smtp_server = 'smtp.gmail.com'
 smtp_port = 587
 # Obținerea cel mai recent fișier video din directorul specificat
 video_files = glob.glob(os.path.join(video_directory, '*.mp4'))
 latest_video = max(video_files, key=os.path.getctime)
 # Crearea obiectului pentru mesajul e-mail
 msg = MIMEMultipart()
 msg['From'] = sender_email
 msg['To'] = receiver_email
 msg['Subject'] = ' INVADER '

 # Deschiderea fișierului video și atașarea acestuia la mesajul e-mail
 with open(latest_video, 'rb') as f:
   attachment = MIMEBase('application', 'octet-stream')
   attachment.set_payload(f.read())
   encoders.encode_base64(attachment)
   attachment.add_header('Content-Disposition', f'attachment; filename={latest_video}')
   msg.attach(attachment)
   
 # Inițializarea conexiunii SMTP și trimiterea mesajului
 try:
  server = smtplib.SMTP(smtp_server, smtp_port)
   server.starttls()
   server.login(sender_email, sender_password)
   server.sendmail(sender_email, receiver_email, msg.as_string())
   print('E-mail sent successfully!')
 except Exception as e:
   print(f'Error occurred while sending e-mail: {str(e)}')
 finally:
   server.quit()
   
# Datele de autentificare
sender_email = 'lucianraspberry07@gmail.com'
sender_password = '****************'
receiver_email = 'neagulucian1889@gmail.com'
video_directory = '/home/pi/Desktop/proiect_licenta/video'
send_video_email(sender_email, sender_password, receiver_email, video_directory)
