# Generated by Django 4.2 on 2024-09-05 14:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Moribit_Module', '0025_chatbot'),
    ]

    operations = [
        migrations.AlterField(
            model_name='chatbot',
            name='message',
            field=models.TextField(blank=True, default='', null=True),
        ),
    ]
