# Generated by Django 4.2 on 2024-07-09 12:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Moribit_Module', '0005_remove_user_last_activity'),
    ]

    operations = [
        migrations.AlterField(
            model_name='giftcode',
            name='gift',
            field=models.BigIntegerField(default=0),
        ),
    ]
