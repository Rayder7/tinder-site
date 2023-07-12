import os
import random
import smtplib
import string
from email.mime.text import MIMEText

from PIL import Image

from tinder_site.settings import MEDIA_ROOT


def add_watermark_image(file):
    image = Image.open(file)
    watermarked_image = Image.open(MEDIA_ROOT + '/watermark.jpg')
    watermarked_image = watermarked_image.resize(image.size, Image.NEAREST)
    my_img = Image.blend(image, watermarked_image, 0.3)
    filename_prefix = ''.join(random.choices(string.ascii_uppercase, k=16))
    new_filename = f'/avatars/{filename_prefix}-{file.name}'
    my_img.save(MEDIA_ROOT + new_filename)

    return new_filename


def send_message(follower, followed):
    msg = MIMEText(
        f'Вы понравились {followed.first_name}!'
        f' Почта участника: {followed.email}')
    msg['Subject'] = 'Вы понравились!'
    msg['From'] = os.getenv('SMTP_LOGIN')
    msg['To'] = follower.email
    server = smtplib.SMTP(os.getenv('SMTP_HOST'), os.getenv('SMTP_PORT'))
    server.ehlo()
    server.starttls()
    server.ehlo()
    server.login(msg['From'], os.getenv('SMTP_PASSWORD'))
    server.sendmail(msg['From'], [msg['To']], msg.as_string())
    server.quit()
