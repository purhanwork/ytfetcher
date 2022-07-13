# Generated by Django 4.0.6 on 2022-07-12 11:41

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='VideoMeta',
            fields=[
                ('title', models.CharField(max_length=100)),
                ('description', models.TextField()),
                ('publishedAt', models.DateTimeField()),
                ('thumbnailURL', models.URLField()),
                ('videoId', models.CharField(max_length=256, primary_key=True, serialize=False)),
            ],
            options={
                'verbose_name': 'Video Metadata',
                'verbose_name_plural': 'Videos Metadata',
                'ordering': ['-publishedAt'],
                'get_latest_by': 'publishedAt',
            },
        ),
        migrations.AddIndex(
            model_name='videometa',
            index=models.Index(fields=['videoId'], name='api_videome_videoId_2f247e_idx'),
        ),
        migrations.AddIndex(
            model_name='videometa',
            index=models.Index(fields=['publishedAt'], name='api_videome_publish_b4d6b0_idx'),
        ),
    ]
