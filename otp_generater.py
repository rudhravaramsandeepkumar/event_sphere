import smtplib
from email.message import EmailMessage
import email
import os
import random
import re
import string
from datetime import datetime
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText


# def get_random_characters(string_length=3):
#     return ''.join(random.choice(string.ascii_letters) for x in range(string_length))


def get_random_numbers(string_length=3):
    return ''.join(random.choice(string.digits) for x in range(string_length))


def send_email_fun(from_='', to_=None, name_='', otp='', start_time='', end_time='5 Min'):
    if not to_ or not isinstance(to_, list):
        raise ValueError("Recipient list is empty or not a list")

    msg = EmailMessage()
    msg['Subject'] = 'UNT!'
    msg['From'] = from_
    msg['To'] = ', '.join(to_)

    msg.set_content('This is a plain text email')

    l = f'<!DOCTYPE html> <html lang="en"> <head> <meta charset="utf8"> <meta http-equiv="x-ua-compatible" content="ie=edge"> <meta name="viewport" content="width=device-width,initial-scale=1"> <meta name="x-apple-disable-message-reformatting"> <title>Your reservation is now confirmed</title> <link href="https://fonts.googleapis.com/css?family=Roboto" rel="stylesheet"> <!--  <xml>--> <!--    <o:OfficeDocumentSettings>--> <!--      <o:PixelsPerInch>96</o:PixelsPerInch>--> <!--    </o:OfficeDocumentSettings>--> <!--  </xml>--> <style> '
    l += '''table {border-collapse: collapse;} td,th,div,p,a,h1,h2,h3,h4,h5,h6 {font-family: "Segoe UI", sans-serif; mso-line-height-rule: exactly;} </style> <![endif]--> <style>'''
    l += '@media screen { img { max-width: 100%; } td, th { box-sizing: border-box; } u~div .wrapper { min-width: 100vw; } a[x-apple-data-detectors] { color: inherit; text-decoration: none; } .all-font-roboto { font-family: Roboto, -apple-system, "Segoe UI", sans-serif !important; } .all-font-sans { font-family: -apple-system, "Segoe UI", sans-serif !important; } } @media (max-width: 600px) { .sm-inline-block { display: inline-block !important; } .sm-hidden { display: none !important; } .sm-leading-32 { line-height: 32px !important; } .sm-p-20 { padding: 20px !important; } .sm-py-12 { padding-top: 12px !important; padding-bottom: 12px !important; } .sm-text-center { text-align: center !important; } .sm-text-xs { font-size: 12px !important; } .sm-text-lg { font-size: 18px !important; } .sm-w-1-4 { width: 25% !important; } .sm-w-3-4 { width: 75% !important; } .sm-w-full { width: 100% !important; } } </style> <style> @media (max-width: 600px) { .sm-dui17-b-t { border: solid #4299e1; border-width: 4px 0 0; } } </style> <style> .container_forj { display: grid; grid-template-columns: repeat(2, 1fr); gap: 1.6rem; } </style> </head>'
    l += f'<body> <div class="container_forj" style="background-color: #f5dbce ;"> <div style="padding: 20px 20px; flex: 1 1 auto; position: relative;"> <div align="left" class="sm-p-20 sm-dui17-b-t" style="border-radius: 10px; padding: 40px; position: relative; box-shadow: 0 10px 15px -3px rgba(0, 0, 0, .1), 0 4px 6px -2px rgba(0, 0, 0, .05); vertical-align: top; z-index: 50;background-color: #ffffff ;margin-right: 200px;margin-left:260px;" valign="top"> <table width="100%" cellpadding="0" cellspacing="0" role="presentation"> <tr> <td width="80%"> <h1 class="sm-text-lg all-font-roboto" style="font-weight: 700; line-height: 100%; margin: 0; margin-bottom: 4px; font-size: 24px;">Reset Password Details</h1> <p class="sm-text-xs" style="margin: 0; color: #a0aec0; font-size: 14px;">Your one time passcode details</p> </td> <td style="text-align: right;" width="20%" align="right"> <a href="https://raw.githubusercontent.com/fuelquote/images/23ecd25db8bfe11cb4010e9ee4bf0a6bc53e75d4/petroleum-svgrepo-com.svg" target="_blank" style="text-decoration: none;"> <img src="https://raw.githubusercontent.com/fuelquote/images/main/petroleum-svgrepo-com.png" alt="Download PDF" style="border: 0; line-height: 100%; vertical-align: middle; font-size: 12px;" width="40"> </a> </td> </tr> </table> <div style="line-height: 32px;">&zwnj;</div> <table class="sm-leading-32" style="line-height: 28px; font-size: 14px;" width="100%" cellpadding="0" cellspacing="0" role="presentation"> <tr> <td class="sm-inline-block" style="color: #718096;" width="50%">User Name</td> <td class="sm-inline-block" style="font-weight: 600; text-align: right;" width="50%" align="right">{str(name_)}</td> </tr> <tr> <td class="sm-inline-block" style="color: #718096;" width="50%">Gmail</td> <td class="sm-inline-block" style="font-weight: 600; text-align: right;" width="50%" align="right">{to_}</td> </tr> <tr> <td class="sm-w-1-4 sm-inline-block" style="color: #718096;" width="50%">OTP</td> <td class="sm-w-3-4 sm-inline-block" style="font-weight: 600; text-align: right;" width="50%" align="right">{str(otp)}</td> </tr> </table> <table width="100%" cellpadding="0" cellspacing="0" role="presentation"> <tr> <td style="padding-top: 24px; padding-bottom: 24px;"> <div style="background-color: #edf2f7; height: 2px; line-height: 2px;">&zwnj;</div> </td> </tr> </table> <table style="font-size: 14px;" width="100%" cellpadding="0" cellspacing="0" role="presentation"> <tr> <td class="sm-w-full sm-inline-block sm-text-center" width="40%"> <p class="all-font-roboto" style="margin: 0; margin-bottom: 4px; color: #a0aec0; font-size: 10px; text-transform: uppercase; letter-spacing: 1px;">Otp Valid From</p> <p class="all-font-roboto" style="font-weight: 600; margin: 0; color: #000000;">{str(start_time)}</p> </td> <td class="sm-w-full sm-inline-block sm-py-12" style="font-family: Menlo, Consolas, monospace; font-weight: 600; text-align: center; color: #cbd5e0; font-size: 18px; letter-spacing: -1px;" width="20%" align="center">&gt;&gt;&gt;</td> <td class="sm-w-full sm-inline-block sm-text-center" style="text-align: right;" width="40%" align="right"> <p class="all-font-roboto" style="margin: 0; margin-bottom: 4px; color: #a0aec0; font-size: 10px; text-transform: uppercase; letter-spacing: 1px;">Otp Valid Upto</p> <p class="all-font-roboto" style="font-weight: 600; margin: 0; color: #000000;">{str(end_time)}</p> </td> </tr> </table> <table width="100%" cellpadding="0" cellspacing="0" role="presentation"> <tr> <td style="padding-top: 24px; padding-bottom: 24px;"> <div style="background-color: #edf2f7; height: 2px; line-height: 2px;">&zwnj;</div> <div style="font-weight: 600; padding-top: 32px; text-align: center; color: #000000; font-size: 20px;" width="50%" align="center"">Current Prices</div> </td> </tr> </table> <table style="line-height: 28px; font-size: 14px;" width="100%" cellpadding="0" cellspacing="0" role="presentation"> <tr> <td style="color: #718096;" width="50%">Diesel Per Gallon</td> <td style="font-weight: 600; text-align: right;" width="50%" align="right">$1.50</td> </tr> <tr> <td style="font-weight: 600; padding-top: 32px; color: #000000; font-size: 20px;" width="50%"></td> <td style="font-weight: 600; padding-top: 32px; text-align: right; color: #68d391; font-size: 20px;" width="50%" align="right"></td> </tr> </table> </div> </div> </div> </body> </html>'

    msg.add_alternative(l, subtype='html')
    # msg.attach(html_part)
    # Rest of your HTML email construction code...

    with smtplib.SMTP('smtp.office365.com', 587) as smtp:
        smtp.starttls()
        smtp.login(from_, 'EventSp1234567890')  # Provide your Outlook password here or use a secure method
        smtp.send_message(msg)


def generate_otp():
    rand_ = datetime.now().strftime("%d%m%Y%H%M%S") + get_random_numbers(5)
    otp_ = rand_[9:16]
    return otp_


otp_ = generate_otp()

send_email_fun("EventSpherealerts@outlook.com", ["sandeepkumarrudhravaram0996@gmail.com","AkhilaChintham@my.unt.edu"], "", otp_, "", "")
