# Generated by Django 4.2 on 2024-07-27 09:51

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Moribit_Module', '0017_alter_dailybnonuseuser_date_time'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='dailybnonuseuser',
            name='is_active',
        ),
    ]
