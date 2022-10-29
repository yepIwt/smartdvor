# Generated by Django 4.1.2 on 2022-10-29 15:22

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0005_service'),
    ]

    operations = [
        migrations.AddField(
            model_name='service',
            name='pub_date',
            field=models.DateField(default=datetime.date.today, verbose_name='Дата запроса'),
        ),
    ]