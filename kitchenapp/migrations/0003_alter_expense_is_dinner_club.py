# Generated by Django 5.1.2 on 2024-10-31 16:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('kitchenapp', '0002_alter_resident_balance_alter_resident_move_in_date_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='expense',
            name='is_dinner_club',
            field=models.BooleanField(null=True),
        ),
    ]
