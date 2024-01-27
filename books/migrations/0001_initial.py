# Generated by Django 4.0.3 on 2024-01-10 12:28

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='BussinessMonth',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('opening_cash', models.IntegerField()),
                ('opening_stock', models.IntegerField()),
                ('opening_date', models.DateField(auto_now_add=True, verbose_name='opening date')),
                ('closing_cash', models.IntegerField(null=True)),
                ('closing_stock', models.IntegerField(null=True)),
                ('closing_date', models.DateField(null=True, verbose_name='closing date')),
                ('profit', models.IntegerField(default=0)),
            ],
        ),
        migrations.CreateModel(
            name='Credit',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('item', models.CharField(max_length=200)),
                ('amount', models.IntegerField()),
                ('book_date', models.DateField(auto_now_add=True, verbose_name='date')),
            ],
        ),
        migrations.CreateModel(
            name='Debit',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('item', models.CharField(max_length=200)),
                ('amount', models.IntegerField()),
                ('book_date', models.DateField(auto_now_add=True, verbose_name='date')),
            ],
        ),
        migrations.CreateModel(
            name='Stock',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('drug', models.CharField(max_length=100)),
                ('price', models.IntegerField()),
                ('date_added', models.DateField(auto_now_add=True)),
                ('balanced', models.BooleanField(default=True)),
            ],
        ),
    ]
