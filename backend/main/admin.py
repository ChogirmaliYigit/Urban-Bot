from django.contrib import admin
from .models import User, AdminsTG, Token, BotMessage, Channel


class UserList(admin.ModelAdmin):
    list_display = (
    'id', 'username', 'fullname', 'competition_id', 'phone', 'birth_day', 'ref_count', 'parent', 'lang', 'ban')
    search_fields = ['id', ]


admin.site.register(User, UserList)


class AdminList(admin.ModelAdmin):
    list_display = ('tg_id', 'name')


admin.site.register(AdminsTG, AdminList)


class TokenList(admin.ModelAdmin):
    list_display = ('token','channel','contest')


admin.site.register(Token, TokenList)


class BotMessageList(admin.ModelAdmin):
    list_display = ('id', 'code', 'content', 'lang')
    search_fields = ['code', 'content']


admin.site.register(BotMessage, BotMessageList)


@admin.register(Channel)
class ChannelAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "chat_id", "link")
    search_fields = list_display
