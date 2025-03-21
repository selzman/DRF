# Generated by Django 4.2 on 2024-09-10 08:44

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('Moribit_Module', '0027_alter_chatbot_datetime'),
    ]

    operations = [
        migrations.RenameField(
            model_name='chatbot',
            old_name='datetime',
            new_name='time',
        ),
        migrations.AddField(
            model_name='chatbot',
            name='date',
            field=models.DateField(auto_now_add=True, default=django.utils.timezone.now),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='chatbot',
            name='is_pin',
            field=models.BooleanField(default=False),
        ),
    ]
