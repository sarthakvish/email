import threading
import time

from django.core.mail import EmailMessage


class EmailThread(threading.Thread):
    # countVar = []

    def __init__(self, email_message):
        self.email_message = email_message
        # EmailThread.countVar = []
        threading.Thread.__init__(self)

    def run(self):
        self.email_message.send()
        # self.countVar.append(1)


def send_mail_thread(email_message):
    email_message.send()
    time.sleep(3)
    print("sent")
