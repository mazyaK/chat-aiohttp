import aiohttp_jinja2
from aiohttp_session import get_session
from aiohttp import web, WSMsgType
from settings import log

from chat.models import get_messages, save
from auth.models import get_login

class ChatList(web.View):
    @aiohttp_jinja2.template('chat/index.html')
    async def get(self):
        async with self.request.app['db'].acquire() as conn:
            messages = await get_messages(conn)
            return {'messages': messages}


class WebSocket(web.View):
    async def get(self):
        ws = web.WebSocketResponse()
        await ws.prepare(self.request)

        session = await get_session(self.request)
        async with self.request.app['db'].acquire() as conn:
            data = await self.request.post()
            login = await get_login(conn, session.get('user'))

        for _ws in self.request.app['websockets']:
            _ws.send_str(f'{login}s joined')
        self.request.app['websockets'].append(ws)

        async for msg in ws:
            if type(msg) == WSMsgType.TEXT:
                # if msg.data == 'close':
                async with self.request.app['db'].acquire() as conn:
                    result = await save(conn, login, data['content'])
                    log.debug(result)
                    for _ws in self.request.app['websockets']:
                        await _ws.send_str({
                            'user_id': data['user_id'],
                            'content': data['content'],
                        })
            elif type(msg) == WSMsgType.ERROR:
                log.debug(f'ws connection closed with exception {ws.exception()}')

        self.request.app['websockets'].remove(ws)
        for _ws in self.request.app['websockets']:
            _ws.send_str(f'{login}s disconnected')
        log.debug('websocket connection closed')

        return ws





