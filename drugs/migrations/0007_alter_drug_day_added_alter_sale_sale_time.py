# Generated by Django 4.0.3 on 2024-03-05 13:14

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('drugs', '0006_drug_cost_price_alter_drug_day_added'),
    ]

    operations = [
        migrations.AlterField(
            model_name='drug',
            name='day_added',
            field=models.DateField(default='2024-03-05'),
        ),
        migrations.AlterField(
            model_name='sale',
            name='sale_time',
            field=models.DateTimeField(default=datetime.time(13, 14, 21, 735296)),
        ),
    ]
