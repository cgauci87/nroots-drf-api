# Generated by Django 3.2.4 on 2023-02-08 21:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0012_auto_20230207_1524'),
    ]

    operations = [
        migrations.AddField(
            model_name='item',
            name='additional_details',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name='item',
            name='comparePrice',
            field=models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True),
        ),
    ]
