# Generated by Django 4.2 on 2024-07-09 11:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Moribit_Module', '0002_rename_referralsettings_referralgift'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='wallet',
            field=models.CharField(blank=True, default='', max_length=500, null=True),
        ),
    ]
