# Generated by Django 3.2.25 on 2024-11-22 14:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('demo', '0006_alter_stylemodel_style_input'),
    ]

    operations = [
        migrations.AlterField(
            model_name='stylemodel',
            name='style_input',
            field=models.CharField(choices=[('my style', 'my style'), ('preloaded style', 'preloaded style')], default='preloaded style', max_length=15, verbose_name=''),
        ),
    ]
