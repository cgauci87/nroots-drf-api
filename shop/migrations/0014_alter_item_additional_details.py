# Generated by Django 3.2.4 on 2023-02-08 21:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0013_auto_20230208_2134'),
    ]

    operations = [
        migrations.AlterField(
            model_name='item',
            name='additional_details',
            field=models.CharField(blank=True, max_length=1000, null=True),
        ),
    ]