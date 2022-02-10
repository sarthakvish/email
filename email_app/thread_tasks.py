import threading
import time

from smtplib import SMTPException

from django.core.mail import EmailMessage, BadHeaderError


class EmailThread(threading.Thread):
    def __init__(self, email_message, *args, **kwargs):
        super(EmailThread, self).__init__(*args, **kwargs)
        self._stop_event = threading.Event()
        self.email_message = email_message
        threading.Thread.__init__(self)

    def run(self):
        print(threading.currentThread().getName())
        self.email_message.send()
        print(threading.currentThread().getName())
        print('thread work is done')
        print(self.email_message.to)
        # try:
        #
        # except BadHeaderError:  # If mail's Subject is not properly formatted.
        #     print('Invalid header found.')
        # except SMTPException as e:  # It will catch other errors related to SMTP.
        #     print('There was an error sending an email.' + e)
        # except:  # It will catch All other possible errors.
        #     print("Mail Sending Failed!")

    def stop(self):
        self._stop_event.set()

    def stopped(self):
        return self._stop_event.is_set()


