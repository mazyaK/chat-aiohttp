from sqlalchemy import (
    MetaData, Table, Column, String, DateTime, ForeignKey
)

from datetime import datetime
from auth.models import user

__all__ = ['message']

meta = MetaData()


message = Table(
    'message', meta,

    Column('user_id', None, ForeignKey('user.id')),
    Column('content', String(200), nullable=False),
    Column('time', DateTime, nullable=False),
)


async def save(conn, user_id, msg, **kw):
    result = await conn.execute(message.insert(), [
        {
            'user_id': user_id,
            'content': msg,
            'time': datetime.now(),
        }
    ])
    return result


async def get_messages(conn):
    messages = await (await conn.execute(message.select())).fetchall()
    return await messages.to_list(length=None)









