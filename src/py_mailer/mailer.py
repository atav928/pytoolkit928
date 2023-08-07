"""mailer"""

import smtplib
import re
import base64
from email import encoders
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email.mime.text import MIMEText

_default_to = ['adam@example.com']
_default_from = 'python-script@example.com'
_default_cc = ['']
_default_bcc = ['']
_encoding = 'utf-8'


def send_mail(smtp_server: str, msg: str = "EMPTY", subject: str = "Python Script", mail_to: list = _default_to,
              mail_from: str = _default_from, mail_cc: list = _default_cc, mail_bcc: list = _default_bcc,
              msg_html: str = None, attachment: str = None, port: int = 25):
    """Send Mail

    :param smtp_server: _description_
    :type smtp_server: str
    :param msg: _description_, defaults to "EMPTY"
    :type msg: str, optional
    :param subject: _description_, defaults to "Python Script"
    :type subject: str, optional
    :param mail_to: _description_, defaults to _default_to
    :type mail_to: list, optional
    :param mail_from: _description_, defaults to _default_from
    :type mail_from: str, optional
    :param mail_cc: _description_, defaults to _default_cc
    :type mail_cc: list, optional
    :param mail_bcc: _description_, defaults to _default_bcc
    :type mail_bcc: list, optional
    :param msg_html: _description_, defaults to None
    :type msg_html: str, optional
    :param attachment: _description_, defaults to None
    :type attachment: str, optional
    :param port: _description_, defaults to 25
    :type port: int, optional
    :return: _description_
    :rtype: _type_
    """
    

    # Handle if a string is passed
    if not isinstance(mail_to, list):
        mail_to = [mail_to]
    if not isinstance(mail_cc, list):
        mail_cc = [mail_cc]
    if not isinstance(mail_bcc, list):
        mail_bcc = [mail_bcc]

    message = MIMEMultipart('alternative')
    message['Subject'] = subject
    message['From'] = mail_from
    message['To'] = ", ".join(mail_to)
    message['cc'] = ", ".join(mail_cc)
    message['bcc'] = ", ".join(mail_bcc)

    try:
        if attachment and isinstance(attachment, list):
            for a in attachment:
                with open(a, 'rb', encoding=_encoding) as attach:
                    # add file as application/octet-stream
                    # email client can usually downlaoad this automatically as an attachemment
                    part = MIMEBase('application', 'octet-stream')
                    part.set_payload(attach.read())
                    # encode
                    encoders.encode_base64(part)
                # Get Filename
                split = re.findall(r"[\w']+", a)
                filename = f'{split[-2]}.{split[-1]}'
                # Add header as key/value pair to attach part
                part.add_header(
                    "Content-Disposition",
                    f"attachment; filename={filename}",
                )
                # Add attachment to message and convert message to string
                message.attach(part)
        if msg_html:
            html_email_message = MIMEText(msg_html, 'html')
            message.attach(html_email_message)
        else:
            plaintext_email_message = MIMEText(msg, 'plain')
            message.attach(plaintext_email_message)
        # Send Email
        with smtplib.SMTP(smtp_server, port) as server:
            server.ehlo()
            server.send_message(message)
            server.quit()
        return "Success"
    except (smtplib.SMTPConnectError, smtplib.SMTPDataError, smtplib.SMTPAuthenticationError, smtplib.SMTPHeloError, smtplib.SMTPServerDisconnected) as err:
        return f"SMTP Connection Error: {str(err)}"
    except (smtplib.SMTPException, smtplib.SMTPSenderRefused, smtplib.SMTPNotSupportedError, smtplib.SMTPResponseException, smtplib.SMTPRecipientsRefused) as err:
        return f"SMTP Communication Error: {str(err)}"
    except Exception:
        return "SMTP Unknown Error"


def convert_to_base64(filename):
    with open(filename, 'rb') as img_file:
        my_string = base64.b64decode(img_file.read())
    return my_string
