# Generated by Django 3.2.6 on 2021-09-07 05:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('food_app', '0002_restaurant_review'),
    ]

    operations = [
        migrations.AddField(
            model_name='restaurant',
            name='address',
            field=models.CharField(default='Sunnyvale,CA', max_length=255),
            preserve_default=False,
        ),
    ]
