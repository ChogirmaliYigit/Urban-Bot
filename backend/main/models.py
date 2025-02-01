from django.db import models


class User(models.Model):
    id = models.BigIntegerField(unique=True, verbose_name='ID Telegram',blank=True)
    username = models.CharField(max_length=150, null=True, verbose_name='Username',blank=True)
    name = models.CharField(max_length=150, null=True, verbose_name='Имя',blank=True)
    competition_id = models.BigAutoField(primary_key=True, verbose_name='ID Участника',blank=True)
    fullname = models.CharField(max_length=250, null=True, verbose_name='Имя',blank=True)
    phone = models.CharField(max_length=250, null=True, verbose_name='Номер',blank=True)
    birth_day = models.DateField(null=True, verbose_name='День рождение',blank=True)
    ref_count = models.BigIntegerField(null=True, verbose_name='Рефералы',blank=True)
    parent = models.BigIntegerField(null=True, verbose_name='ID Пригласителя',blank=True)
    lang = models.CharField(max_length=250, null=True,verbose_name='Язык',blank=True)
    ban = models.BooleanField(default=True,verbose_name='Бан',blank=True)

    class Meta:
        verbose_name = 'Пользователя'
        verbose_name_plural = 'Пользователи'


class AdminsTG(models.Model):
    tg_id = models.BigIntegerField(verbose_name='ID Telegram')
    name = models.CharField(verbose_name='Имя администратора',max_length=200)

    class Meta:
        verbose_name = 'Админа'
        verbose_name_plural = 'Администраторы'


class Token(models.Model):
    ids = models.IntegerField(default=1, unique=True, editable=False)
    token = models.TextField(verbose_name='Токен бота')
    channel = models.BigIntegerField(verbose_name='ID канала')
    contest = models.BooleanField(verbose_name='Активность конкурса')

    class Meta:
        verbose_name = 'Токен'
        verbose_name_plural = 'Токены'


class BotMessage(models.Model):
    UZ = 'uz'
    RU = 'ru'
    EN = 'en'

    LANGUAGES = (
        (UZ, 'Uz'),
        (RU, 'Ru'),
        (EN, 'En')
    )
    code = models.CharField(max_length=1000, unique=True)
    content = models.TextField()
    lang = models.CharField(max_length=10, choices=LANGUAGES, default=RU)

    def __str__(self) -> str:
        return f"{self.code} - {self.content}"

    class Meta:
        verbose_name = 'Сообщение бота'
        verbose_name_plural = 'Сообщения бота'


class Channel(models.Model):
    chat_id = models.BigIntegerField(verbose_name="ID канала")
    name = models.CharField(max_length=250, verbose_name='Название канала')
    link = models.CharField(max_length=250, verbose_name='Ссылка на канал')

    class Meta:
        verbose_name = 'Канал'
        verbose_name_plural = 'Каналы'


class SubscribeRequests(models.Model):
    channel = models.ForeignKey(Channel, on_delete=models.CASCADE, verbose_name="Канал", related_name="subscribe_requests")
    user_telegram_id = models.BigIntegerField(verbose_name="ID Telegram")
