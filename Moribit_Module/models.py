from django.db import models
from django.contrib.auth.models import AbstractUser
import random
import string
from django.utils import timezone
class User(AbstractUser):
    email = models.EmailField(unique=True, blank=False, null=False)
    referral_code = models.BigIntegerField(unique=True, blank=True, null=True)
    referred_by = models.ForeignKey('User', on_delete=models.CASCADE, null=True, blank=True, related_name='referrals')
    level = models.BigIntegerField(default=1)
    level_xp = models.BigIntegerField(default=0)
    blue_tick = models.BooleanField(default=False)
    coin = models.BigIntegerField(default=100000)
    wallet = models.CharField(max_length=500, default='', blank=True, null=True)
    ads = models.BigIntegerField(default=0)

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email']

    def __str__(self):
        return f'{self.username} {self.email}'

    def generate_unique_referral_code(self):
        while True:
            code = random.randint(1, 9999999999999)
            if not User.objects.filter(referral_code=code).exists():
                return code

    def generate_random_string(self, length=32):
        characters = string.ascii_letters + string.digits
        return ''.join(random.choice(characters) for i in range(length))

    def count_referrals(self):
        return self.referrals.count()

    def save(self, *args, **kwargs):
        if not self.referral_code:
            self.referral_code = self.generate_unique_referral_code()
        super().save(*args, **kwargs)


class ReferralGift(models.Model):
    referral_coin_amount = models.BigIntegerField(default=100)

    def __str__(self):
        return f'Referral Coin Amount: {self.referral_coin_amount}'


class VideoGiftCoin(models.Model):
    coin_amount = models.BigIntegerField(default=100)


class VideoSentForCheck(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    date_time = models.DateTimeField(auto_now_add=True)
    link = models.URLField(max_length=500)
    is_active = models.BooleanField(default=False)

    def __str__(self):
        return f'{self.user} {self.date_time}'


class GiftCode(models.Model):
    user = models.ManyToManyField(User, blank=True)
    code = models.CharField(max_length=100, unique=True)
    gift = models.BigIntegerField(default=0)

    def __str__(self):
        return f'{self.code} {self.gift}'




class Moriaigiftcoin(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    code = models.CharField(max_length=100)
    redeemed_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'code')

    def __str__(self):
        return f'{self.user.username} redeemed {self.code} on {self.redeemed_at}'






class webappusercode(models.Model):
    code = models.CharField(max_length=100, unique=True)
    gift =models.IntegerField(default=0)
    is_used = models.BooleanField(default=False)

    def __str__(self):
        return f'{self.code} {self.gift}'




class userdaily(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    jack_pot=models.IntegerField(default=20)
    turbo=models.IntegerField(default=3)
    energy=models.IntegerField(default=6)











class chatbot(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    message = models.TextField(null=True, blank=True, default='')
    time=models.TimeField(auto_now_add=True)
    date=models.DateField(auto_now_add=True)
    is_pin=models.BooleanField(default=False)

    def __str__(self):
        return self.user.email





