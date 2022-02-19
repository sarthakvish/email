import threading
import time
from smtplib import SMTPException
from django.core.mail import EmailMessage, BadHeaderError
from email_app.models.subscribers_models import CampaignsLogSubscriber, CampaignsLogs


class EmailThread(threading.Thread):
    def __init__(self, email_message, campaign_log, *args, **kwargs):
        super(EmailThread, self).__init__(*args, **kwargs)
        self._stop_event = threading.Event()
        self.email_message = email_message
        self.campaign_log = campaign_log
        threading.Thread.__init__(self)

    def run(self):
        try:
            print(threading.currentThread().getName())
            self.email_message.send()
            print(threading.currentThread().getName())
            print('thread work is done')
            print(self.email_message.to)
            campaign_log_subscriber = CampaignsLogSubscriber(campaign_log=self.campaign_log,
                                                             subscriber_email=self.email_message.to[0], is_sent=True)
            campaign_log_subscriber.save()
            print("iddd", self.campaign_log.id)
            campaign_log_obj = CampaignsLogs.objects.get(id=self.campaign_log.id)
            subscriber_count = campaign_log_obj.campaignslogsubscriber_set.all().count()
            print("subcount", subscriber_count)
            print('emailcount', campaign_log_obj.email_count)
            if campaign_log_obj.email_count == subscriber_count:
                campaign_log_obj.is_completed = True
                campaign_log_obj.save()

        except BadHeaderError:  # If mail's Subject is not properly formatted.
            print('Invalid header found.')
        except SMTPException as e:  # It will catch other errors related to SMTP.
            print('There was an error sending an email.' + e)
        except Exception as e:  # It will catch All other possible errors.
            print("Mail Sending Failed!")
            print(e)
            campaign_log_subscriber = CampaignsLogSubscriber(campaign_log=self.campaign_log,
                                                             subscriber_email=self.email_message.to[0], is_sent=False)
            campaign_log_subscriber.save()
            print("iddd", self.campaign_log.id)
            campaign_log_obj = CampaignsLogs.objects.get(id=self.campaign_log.id)
            subscriber_count = campaign_log_obj.campaignslogsubscriber_set.all().count()
            print("subcount", subscriber_count)
            print('emailcount', campaign_log_obj.email_count)
            if campaign_log_obj.email_count == subscriber_count:
                campaign_log_obj.is_completed = True
                campaign_log_obj.save()

    def stop(self):
        self._stop_event.set()

    def stopped(self):
        return self._stop_event.is_set()
