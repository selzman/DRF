from django.db import models
from Moribit_Module.models import User
from django.utils import timezone
from django.db.models.signals import pre_save ,post_save
from django.dispatch import receiver


class News(models.Model):
    title = models.CharField(max_length=100,null=True,blank=True)
    content = models.TextField(max_length=1000,null=True,blank=True)
    image = models.ImageField(upload_to="images/", null=True, blank=True)
    link = models.URLField(null=True, blank=True)
    DateTime=models.DateTimeField(auto_now_add=True)
    is_published = models.BooleanField(default=False)

    def __str__(self):
        return self.title



class AppConfigManager(models.Manager):
    def get_queryset(self):

        queryset = super().get_queryset()

        today = timezone.now().date()
        for config in queryset:
            if config.deactivate_date:
                delta = (config.deactivate_date - today).days

                if delta >= 0:
                    config.count = delta
                else:
                    config.count = 0
                    config.is_active = False
                    config.is_mint_on = False

                config.save()

        return queryset

class AppConfing(models.Model):
    is_active = models.BooleanField(default=True)
    is_mint_on = models.BooleanField(default=False)
    count = models.BigIntegerField(default=0)
    deactivate_date = models.DateField(null=True, blank=True)
    app_version=models.CharField(max_length=100,null=True,blank=True)

    objects = AppConfigManager()

    def save(self, *args, **kwargs):

        if self.deactivate_date:
            today = timezone.now().date()
            delta = (self.deactivate_date - today).days

            if delta >= 0:
                self.count = delta
            else:
                self.count = 0
                self.is_active = False
                self.is_mint_on = False

        super(AppConfing, self).save(*args, **kwargs)







class DailybonusManager(models.Manager):
    def get_queryset(self):
        queryset = super().get_queryset()

        today = timezone.now().date()
        for bonus in queryset:
            if bonus.deactivate_date:
                delta = (bonus.deactivate_date - today).days

                if delta >= 0:
                    bonus.is_active = True
                    bonus.count = delta
                else:
                    bonus.is_active = False
                    bonus.count = 0

                # Save the updated bonus
                bonus.save()

        return queryset

class Dailybonus(models.Model):
    user = models.ManyToManyField(User, blank=True)
    is_active = models.BooleanField(default=True)
    link = models.URLField(null=True, blank=True)
    gift_coin = models.IntegerField(default=0)
    title = models.CharField(max_length=100, null=True, blank=True)
    image = models.ImageField(upload_to="images/", null=True, blank=True)
    deactivate_date = models.DateField(null=True, blank=True)

    objects = DailybonusManager()

    def save(self, *args, **kwargs):
        if self.deactivate_date:
            today = timezone.now().date()
            delta = (self.deactivate_date - today).days

            if delta >= 0:
                self.is_active = True
            else:
                self.is_active = False

        super(Dailybonus, self).save(*args, **kwargs)







class tasks(models.Model):
    user = models.ManyToManyField(User,blank=True)
    title = models.CharField(max_length=100, null=True, blank=True)
    gift_coin = models.IntegerField(default=50000)
    link = models.URLField(null=True, blank=True)



class Adminalert(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    errorText=models.TextField(null=True, blank=True,default='no error')
    datetime=models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.errorText



