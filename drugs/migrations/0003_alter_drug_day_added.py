# Generated by Django 4.0.3 on 2024-01-11 08:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('drugs', '0002_alter_drug_day_added'),
    ]

    operations = [
        migrations.AlterField(
            model_name='drug',
            name='day_added',
            field=models.DateField(default='2024-01-11'),
        ),
    ]