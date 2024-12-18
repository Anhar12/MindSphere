# Generated by Django 5.1.3 on 2024-11-21 20:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('PsychologyTest', '0003_testschedules_image'),
    ]

    operations = [
        migrations.AddField(
            model_name='results',
            name='IsDone',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='results',
            name='ResultNumber',
            field=models.CharField(blank=True, max_length=255, null=True, unique=True),
        ),
        migrations.AlterField(
            model_name='results',
            name='Summary',
            field=models.TextField(default="You're not complete this test"),
        ),
    ]
