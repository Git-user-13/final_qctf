# Generated by Django 4.2.2 on 2023-09-28 09:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("app1", "0025_alter_flag_h1"),
    ]

    operations = [
        migrations.AlterField(
            model_name="flags",
            name="h1",
            field=models.CharField(blank=True, max_length=2000),
        ),
    ]
