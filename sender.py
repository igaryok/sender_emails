import json
import smtplib
import time
from email.message import EmailMessage
from typing import Dict, List


def init_configs(file_name: str) -> Dict:
    with open(file_name) as file_config:
        config = json.load(file_config)

    return config


def setup_text(file_name: str) -> str:
    with open(file_name) as file_text:
        init_message = file_text.read()

    return init_message


class Sender:
    def __init__(self, config_file: str, message_file: str):
        """Initialise Sender.

            Keyword arguments:
            config_files -- file name with json initialise for smtp server
            message_file -- file name with text message
            """
        config = init_configs(config_file)

        self.smtp_server: str = config['server_config']['smtp_server']
        self.smtp_port: int = config['server_config']['smtp_port']
        self.email_sender: str = config['server_config']['sender_email']
        self.email_password: str = config['server_config']['sender_password']
        self.message: str = setup_text(message_file)
        self.subject: str = config['message_config']['subject']
        self.msg = EmailMessage()
        self.__createMessageObject()

    def __createMessageObject(self):
        self.msg['From'] = self.email_sender
        self.msg['Subject'] = self.subject
        self.msg.set_content(self.message)

    def sendMessage(self, receivers_file: str = './in/emails.txt', delay: int = 5, log_file: str = 'email_log.txt'):
        """Method for sending messages.

            Keyword arguments:
            receivers_file -- string with filename which consists from emails separated by coma
            delay -- delay between sending emails
            log_file - file name for logging
            """
        msg = EmailMessage()
        msg['From'] = self.email_sender
        msg['Subject'] = self.subject
        msg.set_content(f'{self.message}')
        receivers: List[str] = setup_text(receivers_file).strip().split(',')
        # connect to the email server
        server = smtplib.SMTP(self.smtp_server, self.smtp_port)
        server.starttls()

        # auth on the server
        server.login(self.email_sender, self.email_password)

        # send emails.txt
        with open(log_file, 'a') as f:
            count = 0
            for email in receivers:
                count += 1
                try:
                    # send
                    msg['To'] = f'{email.strip()}'
                    server.send_message(msg)
                    f.write(f'Email {count}: of {len(receivers)} Successfully sent email to {email.strip()}\n')
                    print(f'Email {count}: of {len(receivers)} Successfully sent email to {email.strip()}\n')
                except Exception as e:
                    f.write(f'Email {count}: of {len(receivers)}Error sending email to {email.strip()}: {str(e)}\n')
                    print(f'Email {count}: of {len(receivers)} Error sending email to {email.strip()}: {str(e)}\n')

                del msg['To']
                # delay between in second
                if count < len(receivers):
                    time.sleep(delay)

        # close server's connection
        print('Sending complete!')
        server.quit()
