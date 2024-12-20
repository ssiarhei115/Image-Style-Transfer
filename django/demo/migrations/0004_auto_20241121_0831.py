# Generated by Django 3.2.25 on 2024-11-21 08:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('demo', '0003_auto_20241121_0829'),
    ]

    operations = [
        migrations.AlterField(
            model_name='stylemodel',
            name='content',
            field=models.ImageField(upload_to='images/%Y/%m/%d', verbose_name='Content image'),
        ),
        migrations.AlterField(
            model_name='stylemodel',
            name='mixed',
            field=models.ImageField(blank=True, upload_to='output/%Y/%m/%d', verbose_name='Mixed image'),
        ),
        migrations.AlterField(
            model_name='stylemodel',
            name='style',
            field=models.ImageField(blank=True, upload_to='images/%Y/%m/%d', verbose_name='Style image'),
        ),
    ]
