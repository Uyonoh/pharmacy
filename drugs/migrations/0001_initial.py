# Generated by Django 4.0.3 on 2022-07-26 15:09

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Drug',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('drug_name', models.CharField(max_length=30)),
                ('brand_name', models.CharField(max_length=30)),
                ('drug_type', models.CharField(max_length=10)),
                ('weight', models.CharField(max_length=10)),
                ('manufacturer', models.CharField(max_length=30)),
                ('exp_date', models.DateField()),
                ('stock_amount', models.IntegerField()),
                ('price', models.IntegerField()),
                ('category', models.CharField(max_length=30)),
                ('purpose', models.CharField(max_length=30)),
                ('location', models.CharField(max_length=10)),
            ],
        ),
    ]
