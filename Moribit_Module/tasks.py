

from celery import shared_task
from .models import userdaily
from django.utils import timezone
from datetime import timedelta
from .models import chatbot
@shared_task
def reset_user_daily():

    userdaily.objects.all().update(jack_pot=20, turbo=3, energy=6)



@shared_task
def delete_old_chats():
    thirty_days_ago = timezone.now() - timedelta(days=30)
    chatbot.objects.filter(datetime__lt=thirty_days_ago).delete()








