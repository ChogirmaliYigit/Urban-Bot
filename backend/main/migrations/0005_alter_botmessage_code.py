# Generated by Django 4.2.1 on 2023-05-30 17:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0004_botmessage_lang'),
    ]

    operations = [
        migrations.AlterField(
            model_name='botmessage',
            name='code',
            field=models.CharField(max_length=1000, unique=True),
        ),
    ]
