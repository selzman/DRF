# Generated by Django 4.2 on 2024-09-10 08:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Moribit_Module', '0026_alter_chatbot_message'),
    ]

    operations = [
        migrations.AlterField(
            model_name='chatbot',
            name='datetime',
            field=models.TimeField(auto_now_add=True),
        ),
    ]
