# Generated by Django 4.0.3 on 2022-11-14 10:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('drugs', '0013_alter_drug_day_added'),
    ]

    operations = [
        migrations.AddField(
            model_name='drug',
            name='purchase_amount',
            field=models.CharField(default=1000, max_length=30),
            preserve_default=False,
        ),
    ]
