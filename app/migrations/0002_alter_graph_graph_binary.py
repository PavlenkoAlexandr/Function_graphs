# Generated by Django 3.2.6 on 2021-08-19 22:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='graph',
            name='graph_binary',
            field=models.BinaryField(blank=True, default=b''),
        ),
    ]