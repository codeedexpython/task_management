# Generated by Django 5.0.7 on 2024-08-07 07:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user_app', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='reports',
            name='export_data',
            field=models.JSONField(blank=True, null=True),
        ),
    ]
