from django.contrib import admin
from . import models
# Register your models here.


@admin.register(models.AppConfing)
class AppConfing(admin.ModelAdmin):

    list_display = ('deactivate_date','count','is_active', 'is_mint_on',)
    list_editable = ('is_active', 'is_mint_on',)





@admin.register(models.News)
class NewsAdmin(admin.ModelAdmin):
    list_display = ('content', 'DateTime', 'is_published',)
    list_editable = ('is_published',)
    ordering = ('-DateTime',)



@admin.register(models.Dailybonus)
class DailybonusAdmin(admin.ModelAdmin):

    list_display = ('title', 'gift_coin','is_active')
    list_editable = ('is_active',)
    ordering = ('-gift_coin',)



@admin.register(models.tasks)
class TasksAdmin(admin.ModelAdmin):
    list_display = ('title', 'gift_coin','link')
    list_editable = ('gift_coin','link',)
    ordering = ('-gift_coin',)


@admin.register(models.Adminalert)
class AdminalertAdmin(admin.ModelAdmin):
    list_display = ('user', 'errorText','datetime')
    ordering = ('-datetime',)






