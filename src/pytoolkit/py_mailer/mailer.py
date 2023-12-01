# pylint: disable=dangerous-default-value
"""Mailer."""

from typing import List, Union
import smtplib
import re

from email import encoders
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email.mime.text import MIMEText

from pytoolkit.utils import string_or_list
from pytoolkit.static import DEFAULT_TO, DEFAULT_FROM, DEFAULT_CC, DEFAULT_BCC, ENCODING


def send_mail(
    smtp_server: str,
    msg: str = "EMPTY",
    subject: str = "Python Script",
    mail_to: Union[list[str], str] = DEFAULT_TO,
    mail_from: str = DEFAULT_FROM,
    mail_cc: Union[list[str], str] = DEFAULT_CC,
    mail_bcc: Union[list[str], str] = DEFAULT_BCC,
    msg_html: Union[str, None] = None,
    attachment: Union[str, None] = None,
    port: int = 25,
) -> str:
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
    delimeters = ",| "
    mail_to: List[str] = string_or_list(value=mail_to, delimeters=delimeters)
    mail_cc: List[str] = string_or_list(value=mail_cc, delimeters=delimeters)
    mail_bcc: List[str] = string_or_list(value=mail_bcc, delimeters=delimeters)

    message = MIMEMultipart("alternative")
    message["Subject"] = subject
    message["From"] = mail_from
    message["To"] = ", ".join(mail_to)
    message["cc"] = ", ".join(mail_cc)
    message["bcc"] = ", ".join(mail_bcc)

    try:
        if attachment and isinstance(attachment, list):
            for attach in attachment:
                # add file as application/octet-stream
                # email client can usually downlaoad this automatically as an attachemment
                part = MIMEBase("application", "octet-stream")
                with open(attach, "rb", encoding=ENCODING) as a:
                    # Add encoded stream to MIMEBase app payload
                    part.set_payload(a.read())
                    # encode
                    encoders.encode_base64(part)
                # Get Filename
                split: list[str] = re.findall(r"[\w']+", attach)
                filename: str = f"{split[-2]}.{split[-1]}"
                # Add header as key/value pair to attach part
                part.add_header(
                    "Content-Disposition",
                    f"attachment; filename={filename}",
                )
                # Add attachment to message and convert message to string
                message.attach(part)
        if msg_html:
            html_email_message = MIMEText(msg_html, "html")
            message.attach(html_email_message)
        else:
            plaintext_email_message = MIMEText(msg, "plain")
            message.attach(plaintext_email_message)
        # Send Email
        with smtplib.SMTP(smtp_server, port) as server:
            server.ehlo()
            server.send_message(message)
            server.quit()
        return "Success"
    except (
        smtplib.SMTPConnectError,
        smtplib.SMTPDataError,
        smtplib.SMTPAuthenticationError,
        smtplib.SMTPHeloError,
        smtplib.SMTPServerDisconnected,
    ) as err:
        return f"SMTP Connection Error: {str(err)}"
    except (
        smtplib.SMTPException,
        smtplib.SMTPSenderRefused,
        smtplib.SMTPNotSupportedError,
        smtplib.SMTPResponseException,
        smtplib.SMTPRecipientsRefused,
    ) as err:
        return f"SMTP Communication Error: {str(err)}"
    except Exception:
        return "SMTP Unknown Error"


# TODO: Create an encoded function to allow encoded/embeded attachements
# TODO: Add basic templates that can be used for HTML notifications based off Jinja2 examples
