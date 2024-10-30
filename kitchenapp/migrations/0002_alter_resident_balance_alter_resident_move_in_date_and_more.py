# Generated by Django 5.1.2 on 2024-10-30 15:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('kitchenapp', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='resident',
            name='balance',
            field=models.FloatField(null=True),
        ),
        migrations.AlterField(
            model_name='resident',
            name='move_in_date',
            field=models.DateField(null=True),
        ),
        migrations.AlterField(
            model_name='resident',
            name='room_number',
            field=models.IntegerField(null=True),
        ),
    ]