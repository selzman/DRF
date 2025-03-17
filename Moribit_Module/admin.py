from django.contrib import admin
from . import models
from django.utils.html import format_html
from django.utils import timezone
from django.contrib import admin
@admin.register(models.User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('username', 'email', 'coin', 'is_active', 'blue_tick', 'date_joined',)
    list_editable = ('is_active', 'blue_tick',)
    search_fields = ('username', 'email', 'blue_tick',)
    ordering = ('-coin',)




@admin.register(models.VideoSentForCheck)
class VideoSentForCheck(admin.ModelAdmin):
    list_display = ('user','link','date_time','is_active',)
    search_fields = ('user','link','date_time','is_active',)
    list_editable = ('is_active',)
    ordering = ('-date_time',)


@admin.register(models.ReferralGift)
class ReferralSettingsAdmin(admin.ModelAdmin):
    list_display = ('referral_coin_amount',)





@admin.register(models.GiftCode)
class GiftCodeAdmin(admin.ModelAdmin):
    list_display = ('code','gift',)






@admin.register(models.VideoGiftCoin)
class GiftCodeAdmin(admin.ModelAdmin):
    list_display = ('coin_amount',)







@admin.register(models.webappusercode)
class WebappUserCodeAdmin(admin.ModelAdmin):
    list_display = ('code','gift','is_used',)
    search_fields = ('code','gift','is_used',)
    list_editable = ('is_used',)
    list_filter = ('code','gift','is_used',)



@admin.register(models.userdaily)
class UserDailyAdmin(admin.ModelAdmin):
    list_display = ('user','jack_pot','turbo','energy')
    search_fields = ('user',)








@admin.register(models.chatbot)
class ChatbotAdmin(admin.ModelAdmin):
    list_display = ('user','message','is_pin','time','date',)
    ordering = ('-date',)
    search_fields = ('user','message','time','date','is_pin',)
    list_editable = ('is_pin',)
    list_filter = ('user','time')







