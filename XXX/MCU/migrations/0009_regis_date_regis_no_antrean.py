# Generated by Django 5.1.1 on 2024-09-22 02:28

import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('MCU', '0008_remove_regis_date_remove_regis_no_antrean'),
    ]

    operations = [
        migrations.AddField(
            model_name='regis',
            name='date',
            field=models.DateField(default=django.utils.timezone.now),
        ),
        migrations.AddField(
            model_name='regis',
            name='no_antrean',
            field=models.IntegerField(default=1),
        ),
    ]
