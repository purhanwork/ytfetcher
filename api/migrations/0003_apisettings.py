# Generated by Django 4.0.6 on 2022-07-13 04:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0002_alter_videometa_options'),
    ]

    operations = [
        migrations.CreateModel(
            name='ApiSettings',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('baseTime', models.DateTimeField()),
            ],
        ),
    ]
