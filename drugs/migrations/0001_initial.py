# Generated by Django 5.0.6 on 2024-07-01 19:44

import datetime
import django.db.models.deletion
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
                ('drug_type', models.CharField(max_length=20)),
                ('state', models.CharField(choices=[('Tab', 'Tab'), ('Suspension', 'Suspension'), ('Injectable', 'Injectable')], default='Suspension', max_length=20)),
                ('weight', models.CharField(max_length=10)),
                ('manufacturer', models.CharField(max_length=30)),
                ('exp_date', models.DateField(verbose_name='Expiery Date')),
                ('stock_amount', models.IntegerField()),
                ('purchase_amount', models.IntegerField()),
                ('units', models.CharField(choices=[('Cartons', 'Cartons'), ('Packets', 'Packets'), ('Unit', 'Sachets/Bottle/Card')], default='Unit', max_length=30)),
                ('price', models.DecimalField(decimal_places=2, max_digits=10)),
                ('cost_price', models.DecimalField(decimal_places=2, max_digits=10)),
                ('category', models.CharField(max_length=30)),
                ('purpose', models.CharField(max_length=30)),
                ('location', models.CharField(max_length=10)),
                ('day_added', models.DateField(default='2024-02-27')),
                ('out_of_stock', models.BooleanField(default=False)),
            ],
        ),
        migrations.CreateModel(
            name='Injectable',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('no_bottles', models.IntegerField(default=10, null=True)),
                ('no_packs', models.IntegerField(default=1, null=True)),
                ('drug', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='drugs.drug')),
            ],
        ),
        migrations.CreateModel(
            name='Sale',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('drug_name', models.CharField(max_length=30)),
                ('brand_name', models.CharField(max_length=30)),
                ('weight', models.CharField(max_length=10)),
                ('amount', models.IntegerField(default=1)),
                ('total_price', models.IntegerField(null=True)),
                ('sale_time', models.DateTimeField(default=datetime.datetime(2024, 7, 1, 19, 44, 30, 133899, tzinfo=datetime.timezone.utc))),
                ('drug', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='drugs.drug')),
            ],
        ),
        migrations.CreateModel(
            name='Suspension',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('no_bottles', models.IntegerField(default=10, null=True)),
                ('no_packs', models.IntegerField(default=1, null=True)),
                ('drug', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='drugs.drug')),
            ],
        ),
        migrations.CreateModel(
            name='Tablet',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('tab_cd', models.CharField(max_length=10, null=True)),
                ('no_packs', models.IntegerField(default=0, null=True)),
                ('drug', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='drugs.drug')),
            ],
        ),
    ]
