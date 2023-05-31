from typing import Union

import asyncpg
from asyncpg import Connection
from asyncpg.pool import Pool

from data import config


class Database:
    def __init__(self):
        self.pool: Union[Pool, None] = None

    async def create(self):
        self.pool = await asyncpg.create_pool(
            user=config.DB_USER,
            password=config.DB_PASS,
            host=config.DB_HOST,
            database=config.DB_NAME,
        )

    async def execute(
            self,
            command,
            *args,
            fetch: bool = False,
            fetchval: bool = False,
            fetchrow: bool = False,
            execute: bool = False,
    ):
        async with self.pool.acquire() as connection:
            connection: Connection
            async with connection.transaction():
                if fetch:
                    result = await connection.fetch(command, *args)
                elif fetchval:
                    result = await connection.fetchval(command, *args)
                elif fetchrow:
                    result = await connection.fetchrow(command, *args)
                elif execute:
                    result = await connection.execute(command, *args)
            return result

    @staticmethod
    def format_args(sql, parameters: dict):
        sql += " AND ".join(
            [f"{item} = ${num}" for num, item in enumerate(parameters.keys(), start=1)]
        )
        return sql, tuple(parameters.values())

    async def get_bat(self, ban, id):
        sql = "UPDATE main_user SET ban=$1 WHERE id=$2"
        return await self.execute(sql, ban, id, execute=True)

    async def bot_info(self):
        sql = "SELECT * FROM main_token"
        return await self.execute(sql, fetch=True)

    async def add_user(self, full_name, username, telegram_id, ref_count, parent, name2, phone, birth_day, lang, ban):
        sql = "INSERT INTO main_user (name, username, id, ref_count, parent,fullname,phone,birth_day,lang,ban) VALUES($1, $2, $3, $4, $5,$6,$7,$8,$9,$10) returning *"
        return await self.execute(sql, full_name, username, telegram_id, ref_count, parent, name2, phone, birth_day,
                                  lang, ban, fetchrow=True)

    async def add_new(self, full_name, username, telegram_id, ref_count, parent, name2, phone, birth_day, lang, ban,
                      conkurs):
        sql = "INSERT INTO main_user (name, username, id, ref_count, parent,fullname,phone,birth_day,lang,ban,competition_id) VALUES($1, $2, $3, $4, $5,$6,$7,$8,$9,$10,$11) returning *"
        return await self.execute(sql, full_name, username, telegram_id, ref_count, parent, name2, phone, birth_day,
                                  lang, ban, conkurs, fetchrow=True)

    async def user_info(self, name, phone, birth_day, tg_id):
        sql = "UPDATE main_user SET fullname=$1, phone=$2, birth_day=$3 WHERE id=$4"
        return await self.execute(sql, name, phone, birth_day, tg_id, execute=True)

    async def user_restart(self, count, tg_id):
        sql = "UPDATE main_user SET ref_count=$1 WHERE id=$2"
        return await self.execute(sql, count, tg_id, execute=True)

    # Выдача языка
    async def show_lang(self, **kwargs):
        sql = "SELECT * FROM main_user WHERE "
        sql, parameters = self.format_args(sql, parameters=kwargs)
        return await self.execute(sql, *parameters, fetchrow=True)

    async def add_count(self, tg_id):
        sql = "UPDATE main_user SET ref_count = ref_count + 1 WHERE id=$1"
        return await self.execute(sql, tg_id, execute=True)

    async def update_lang(self, lang, telegram_id):
        sql = "UPDATE main_user SET lang=$1 WHERE id=$2"
        return await self.execute(sql, lang, telegram_id, execute=True)

    async def select_all_users(self):
        sql = "SELECT * FROM main_user"
        return await self.execute(sql, fetch=True)

    async def select_user(self, **kwargs):
        sql = "SELECT * FROM main_user WHERE "
        sql, parameters = self.format_args(sql, parameters=kwargs)
        return await self.execute(sql, *parameters, fetchrow=True)
    
    async def select_bot_message(self, **kwargs):
        sql = "SELECT * FROM main_botmessage WHERE "
        sql, parameters = self.format_args(sql, parameters=kwargs)
        return await self.execute(sql, *parameters, fetchrow=True)

    async def count_users(self):
        sql = "SELECT COUNT(*) FROM main_user"
        return await self.execute(sql, fetchval=True)

    async def delete_user(self, id):
        sql = 'DELETE FROM main_user WHERE id=$1'
        return await self.execute(sql, id, execute=True)

    async def update_user_username(self, username, telegram_id):
        sql = "UPDATE main_user SET username=$1 WHERE id=$2"
        return await self.execute(sql, username, telegram_id, execute=True)

    async def delete_users(self):
        await self.execute("DELETE FROM main_user WHERE TRUE", execute=True)

    async def drop_users(self):
        await self.execute("DROP TABLE main_user", execute=True)
