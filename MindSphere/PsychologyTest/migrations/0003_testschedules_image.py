# Generated by Django 5.1.3 on 2024-11-20 05:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('PsychologyTest', '0002_alter_registrations_participantnumber'),
    ]

    operations = [
        migrations.AddField(
            model_name='testschedules',
            name='Image',
            field=models.ImageField(blank=True, null=True, upload_to='test_schedules/'),
        ),
    ]
