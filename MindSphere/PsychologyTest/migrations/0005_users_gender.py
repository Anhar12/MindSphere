# Generated by Django 5.1.3 on 2024-11-21 20:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('PsychologyTest', '0004_results_isdone_alter_results_resultnumber_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='users',
            name='gender',
            field=models.CharField(blank=True, choices=[('Male', 'Male'), ('Female', 'Female')], max_length=10, null=True),
        ),
    ]
