import threading
import time
from smtplib import SMTPException

from django.core.mail import EmailMessage, BadHeaderError


class EmailThread(threading.Thread):
    # countVar = []

    def __init__(self, email_message):
        self.email_message = email_message
        # EmailThread.countVar = []
        threading.Thread.__init__(self)

    def run(self):
        try:
            print(threading.currentThread().getName())
            self.email_message.send()
            thread_list = threading.enumerate()
            print('thread list', len(thread_list))
            # self.countVar.append(1)
        except BadHeaderError:  # If mail's Subject is not properly formatted.
            print('Invalid header found.')
        except SMTPException as e:  # It will catch other errors related to SMTP.
            print('There was an error sending an email.' + e)
        except:  # It will catch All other possible errors.
            print("Mail Sending Failed!")


def send_mail_thread(email_message):
    email_message.send()
    time.sleep(3)
    print("sent")
