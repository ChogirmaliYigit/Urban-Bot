# Generated by Django 4.1.4 on 2023-01-07 15:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0001_initial'),
    ]

    operations = [
        migrations.DeleteModel(
            name='Channels',
        ),
        migrations.AddField(
            model_name='token',
            name='channel',
            field=models.BigIntegerField(default=1, verbose_name='ID канала'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='token',
            name='contest',
            field=models.BooleanField(default=1, verbose_name='Активность конкурса'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='user',
            name='ban',
            field=models.BooleanField(blank=True, default=True, verbose_name='Бан'),
        ),
        migrations.AlterField(
            model_name='user',
            name='birth_day',
            field=models.DateField(blank=True, null=True, verbose_name='День рождение'),
        ),
        migrations.AlterField(
            model_name='user',
            name='fullname',
            field=models.CharField(blank=True, max_length=250, null=True, verbose_name='Имя'),
        ),
        migrations.AlterField(
            model_name='user',
            name='id',
            field=models.BigIntegerField(blank=True, unique=True, verbose_name='ID Telegram'),
        ),
        migrations.AlterField(
            model_name='user',
            name='lang',
            field=models.CharField(blank=True, max_length=250, null=True, verbose_name='Язык'),
        ),
        migrations.AlterField(
            model_name='user',
            name='name',
            field=models.CharField(blank=True, max_length=150, null=True, verbose_name='Имя'),
        ),
        migrations.AlterField(
            model_name='user',
            name='parent',
            field=models.BigIntegerField(blank=True, null=True, verbose_name='ID Пригласителя'),
        ),
        migrations.AlterField(
            model_name='user',
            name='phone',
            field=models.CharField(blank=True, max_length=250, null=True, verbose_name='Номер'),
        ),
        migrations.AlterField(
            model_name='user',
            name='ref_count',
            field=models.BigIntegerField(blank=True, null=True, verbose_name='Рефералы'),
        ),
        migrations.AlterField(
            model_name='user',
            name='username',
            field=models.CharField(blank=True, max_length=150, null=True, verbose_name='Username'),
        ),
    ]
