# Generated by Django 2.2.3 on 2019-07-28 08:19

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('extractvacancy', '0003_vacancy_created_at'),
    ]

    operations = [
        migrations.AlterField(
            model_name='vacancy',
            name='created_at',
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
    ]