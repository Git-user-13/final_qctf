# Generated by Django 4.2.3 on 2023-09-05 06:12

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app1', '0015_flag_quest'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='flag',
            name='quest',
        ),
    ]
