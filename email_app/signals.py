from django.db.models.signals import pre_save, post_delete
from django.contrib.auth.models import User
from email_app.models.user_models import StaffUsers
from django.dispatch import receiver


# @receiver(pre_save, sender=User)
# def updateUser(sender, instance, **kwargs):
#     user = instance
#     if user != '':
#         user.username = user.email
#
# # pre_save.connect(updateUser, sender=User)


@receiver(post_delete, sender=StaffUsers)
def auto_delete_publish_info_with_book(sender, instance, *args, **kwargs):
    instance.user.delete()
