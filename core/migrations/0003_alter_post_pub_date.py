# Generated by Django 4.1.2 on 2022-10-29 13:51

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0002_post_postcomment'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='pub_date',
            field=models.DateField(default=datetime.date.today, verbose_name='Дата создания поста'),
        ),
    ]
