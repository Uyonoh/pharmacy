# Generated by Django 4.0.3 on 2022-08-07 15:37

from django.db import migrations, models
import django.db.models.deletion


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
                ('exp_date', models.DateField(verbose_name='Expiery Date')),
                ('stock_amount', models.IntegerField()),
                ('price', models.IntegerField()),
                ('category', models.CharField(max_length=30)),
                ('purpose', models.CharField(max_length=30)),
                ('location', models.CharField(max_length=10)),
                ('day_added', models.DateField(auto_now_add=True, null=True)),
                ('out_of_stock', models.BooleanField(default=False)),
                ('expired', models.BooleanField(default=False)),
            ],
        ),
        migrations.CreateModel(
            name='Sale',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('drug_name', models.CharField(max_length=30)),
                ('brand_name', models.CharField(max_length=30)),
                ('weight', models.CharField(max_length=10)),
                ('amount', models.IntegerField()),
                ('total_price', models.IntegerField(null=True)),
                ('sale_time', models.DateTimeField(auto_now_add=True)),
                ('drug', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='drugs.drug')),
            ],
        ),
    ]
