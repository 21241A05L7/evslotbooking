# Generated by Django 5.0.6 on 2024-06-04 10:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('App', '0003_remove_evstation_description'),
    ]

    operations = [
        migrations.CreateModel(
            name='EV',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('number', models.CharField(max_length=100)),
            ],
        ),
    ]
