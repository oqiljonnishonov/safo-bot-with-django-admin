from typing import Union

import asyncpg
from asyncpg import Connection
from asyncpg.pool import Pool

from data import config


# user='root', password='root',
#                                                database='pokerpg', host='127.0.0.1'
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

    async def add_user(
        self,
        full_name,
        username,
        telegram_id,
        phone_number,
        latitude,
        longitude,
        create_dt,
        k1,
    ):
        sql = "INSERT INTO products_user (full_name, username, telegram_id,phone_number,latitude,longitude,create_dt,bool) VALUES($1, $2, $3,$4,$5,$6,$7,$8) returning *"
        return await self.execute(
            sql,
            full_name,
            username,
            telegram_id,
            phone_number,
            latitude,
            longitude,
            create_dt,
            k1,
            fetchrow=True,
        )

    async def update_user_bool(
        self, user_id, bool,
    ):
        sql = "UPDATE products_user SET   bool=$2 WHERE id=$1;"
        return await self.execute(sql, user_id, bool, execute=True)

    async def update_user_text(self, user_id, text):
        sql = "UPDATE products_user SET   text=$2 WHERE id=$1;"
        return await self.execute(sql, user_id, text, execute=True)

    async def update_user_location(self, user_id, latitude, longitude):
        sql = "UPDATE products_user SET   longitude=$2,latitude=$3 WHERE id=$1;"
        return await self.execute(sql, user_id, latitude, longitude, execute=True)

    async def update_user1(self, user_id, latitude, longitude):
        sql = "UPDATE products_user SET   latitude=$2, longitude=$3 WHERE id=$1;"
        return await self.execute(sql, user_id, latitude, longitude, execute=True)

    async def update_user2(self, user_id, phone_number):
        sql = "UPDATE products_user SET   phone_number=$2  WHERE id=$1;"
        return await self.execute(sql, user_id, phone_number, execute=True)

    async def update_order_count(self, order_id, count):
        sql = "UPDATE products_order SET   count=$2  WHERE id=$1;"
        return await self.execute(sql, order_id, count, execute=True)

    # async def get_user_bool(self, user_id):
    #     sql = 'UPDATE products_user SET   bool=$2  WHERE id=$1;'
    #     return await self.execute(sql, user_id, bool, execute=True)

    async def add_order(self, count, create_dt, product_id, user_id, k):
        sql = "INSERT INTO products_order (count, create_dt, product_id,user_id,type) VALUES($1, $2, $3,$4,$5) returning *"
        return await self.execute(
            sql, count, create_dt, product_id, user_id, k, fetchrow=True
        )

    async def select_all_users(self):
        sql = "SELECT * FROM products_user"
        return await self.execute(sql, fetch=True)

    async def select_user(self, **kwargs):
        sql = "SELECT * FROM products_user WHERE "
        sql, parameters = self.format_args(sql, parameters=kwargs)
        return await self.execute(sql, *parameters, fetchrow=True)

    async def get_user_bool(self, user_id):
        sql = f"SELECT bool FROM products_user WHERE id={user_id}"
        return await self.execute(sql, fetchval=True)

    async def count_users(self):
        sql = "SELECT COUNT(*) FROM products_user"
        return await self.execute(sql, fetchval=True)

    async def update_user_username(self, username, telegram_id):
        sql = "UPDATE products_user SET username=$1 WHERE telegram_id=$2"
        return await self.execute(sql, username, telegram_id, execute=True)

    async def delete_user(self, telegram_id):
        await self.execute(
            "DELETE FROM products_user WHERE telegram_id=$1", telegram_id, execute=True
        )

    async def delete_order(self, user_id):
        await self.execute(
            "DELETE FROM products_order WHERE user_id=$1", user_id, execute=True
        )

    async def delete_order1(self, oder_id):
        await self.execute(
            "DELETE FROM products_order WHERE id=$1", oder_id, execute=True
        )

    async def get_categories(self):
        sql = "SELECT DISTINCT category_name, category_code FROM products_product"
        return await self.execute(sql, fetch=True)

    async def get_subcategories(self, category_code):
        sql = f"SELECT DISTINCT subcategory_name, subcategory_code FROM products_product WHERE category_code='{category_code}'"
        return await self.execute(sql, fetch=True)

    async def count_products(self, category_code, subcategory_code=None):
        if subcategory_code:
            sql = f'SELECT COUNT(*) FROM products_product WHERE category_code="{category_code}" AND subcategory_code="{subcategory_code}"'
        else:
            sql = f'SELECT COUNT(*) FROM products_product WHERE category_code="{category_code}"'
        return await self.execute(sql, fetchval=True)

    async def get_products(self, category_code, subcategory_code):
        sql = f"SELECT * FROM products_product WHERE category_code='{category_code}' AND subcategory_code='{subcategory_code}'"
        return await self.execute(sql, fetch=True)

    async def get_product(self, product_id):
        sql = f"SELECT * FROM products_product WHERE id={product_id}"
        return await self.execute(sql, fetchrow=True)

    async def get_user(self, telegram_id):
        sql = f"SELECT * FROM products_user WHERE telegram_id={telegram_id}"
        return await self.execute(sql, fetchrow=True)

    async def get_product_subcategory(self, id):
        sql = f"SELECT price,subcategory_name FROM products_product WHERE id={id}"
        return await self.execute(sql, fetchrow=True)

    async def get_user_id(self, telegram_id):
        sql = f"SELECT id FROM products_user WHERE telegram_id={telegram_id}"
        return await self.execute(sql, fetchval=True)

    async def get_oder_id_null(self, user_id):
        sql = f"SELECT id FROM products_order WHERE user_id={user_id} and count=0"
        return await self.execute(sql, fetchval=True)

    async def get_user_order(self, user_id):
        sql = f"SELECT  count,product_id, id FROM products_order WHERE user_id='{user_id}' ORDER BY id "
        return await self.execute(sql, fetch=True)

    async def get_user_order_id(self, user_id, product_id):
        sql = f"SELECT  count, id FROM products_order WHERE user_id='{user_id}' and product_id='{product_id}' "
        return await self.execute(sql, fetchrow=True)

    async def get_user_order1(self, user_id):
        sql = f"SELECT  * FROM products_order WHERE user_id='{user_id}' ORDER BY id "
        return await self.execute(sql, fetch=True)

    async def get_subcategory(self, item_id):
        sql = f"SELECT  subcategory_name FROM products_product WHERE id={item_id}"
        return await self.execute(sql, fetchval=True)

    async def count_update(self, item_id, count):
        sql = f"UPDATE products_order SET  count={count} WHERE id={item_id}  "
        return await self.execute(sql, fetchval=True)
