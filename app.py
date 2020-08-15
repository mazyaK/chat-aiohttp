import asyncio
import aiohttp_jinja2
import jinja2
from aiohttp import web
from aiohttp_session import session_middleware
# from aiohttp_session.cookie_storage import EncryptedCookieStorage

from core.database import init_pg, close_pg
from routes import routes
from settings import *
from middlewares import authorize

from chat.views import ChatList, WebSocket
from auth.views import Login, SignIn, SignOut

import hashlib

loop = asyncio.get_event_loop()

# middle = [
#     session_middleware(EncryptedCookieStorage(hashlib.sha256(bytes(SECRET_KEY, 'utf-8')).digest())),
#     authorize,
# ]

app = web.Application()
app['config'] = config
app.on_startup.append(init_pg)
app.on_cleanup.append(close_pg)
app['websockets'] = []

aiohttp_jinja2.setup(app, loader=jinja2.FileSystemLoader('templates'))

app.router.add_route('GET', '/', ChatList, name='main')
app.router.add_route('GET', 'ws', WebSocket, name='chat')
app.router.add_route('*', '/login', Login, name='login')
app.router.add_route('*', '/signin', SignIn, name='signin')
app.router.add_route('*', '/signout', SignOut, name='signout')

app['static_root_url'] = '/static'
app.router.add_static('/static', 'static', name='static')

log.debug('start server')
web.run_app(app)
log.debug('Stop server end')
