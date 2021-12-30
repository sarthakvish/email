from django.db.models.signals import pre_save, post_delete
from django.contrib.auth.models import User
from email_app.models.user_models import StaffUsers
from django.dispatch import receiver


@receiver(pre_save, sender=User)
def updateUser(sender, instance, **kwargs):
    user = instance
    if user != '':
        user.username = user.email


# pre_save.connect(updateUser, sender=User)


@receiver(post_delete, sender=StaffUsers)
def auto_delete_publish_info_with_book(sender, instance, *args, **kwargs):
    instance.user.delete()


from django_ses.signals import send_received
from django.dispatch import receiver


@receiver(send_received)
def send_handler(sender, mail_obj, raw_message, *args, **kwargs):
    print('signal triggered')
    print(sender)
    print(mail_obj)
    print(raw_message)
    return
