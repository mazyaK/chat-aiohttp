from sqlalchemy import (
    MetaData, Table, Column, Integer, String
)

__all__ = ['user']

meta = MetaData()


user = Table(
    'user', meta,

    Column('id', Integer, primary_key=True),
    Column('login', String(200), nullable=False),
    Column('email', String(200), nullable=False),
    Column('password', String(200), nullable=False),
)


async def check_user(conn, login):
    result = await conn.execute(user.select().where(user.columns.login == login))
    user_record = await result.first()
    if user_record:
        return user_record
    else:
        return False


async def get_login(conn, user_id):
    result = await conn.execute(user.select().where(user.columns.id == user_id))
    result_user = await result.first()
    return result_user.get('login')


async def create_user(conn, data):
    user_existence = await check_user(conn, data['login'])
    if not user_existence:
        result = await conn.execute(user.insert(), [
            {
                'login': data['login'],
                'email': data['email'],
                'password': data['password'],
            }
        ])
    else:
        result = 'User exists'
    return result
