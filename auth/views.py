import json
from time import time

import aiohttp_jinja2
from aiohttp import web
from aiohttp_session import get_session
from .models import check_user, create_user


def redirect(request, router_name):
    url = request.app.router[router_name].url()
    raise web.HTTPFound(url)


def set_session(session, user_id, request):
    session['user'] = str(user_id)
    session['last_visit'] = time()
    redirect(request, 'main')


def convert_json(message):
    return json.dumps({'error': message})


class Login(web.View):

    @aiohttp_jinja2.template('auth/login.html')
    async def get(self):
        session = await get_session(self.request)
        if session.get('user'):
            redirect(self.request, 'main')
        return {'conten': 'Please enter login or email'}

    async def post(self):
        async with self.request.app['db'].acquire() as conn:
            data = await self.request.post()
            result = await check_user(conn, data['login'])
            if isinstance(result, dict):
                session = await get_session(self.request)
                set_session(session, str(result['id']), self.request)
            else:
                return web.Response(content_type='application/json', text=convert_json(result))


class SignIn(web.View):

    @aiohttp_jinja2.template('auth/sign.html')
    async def get(self, **kw):
        session = await get_session(self.request)
        if session.get('user'):
            redirect(self.request, 'main')
        return {'conten': 'Please enter tour data'}

    async def post(self, **kw):
        async with self.request.app['db'].acquire() as conn:
            data = await self.request.post()
            result = await create_user(conn, data)
            if type(result) != str:
                session = await get_session(self.request)
                set_session(session, str(result), self.request)
            else:
                return web.Response(content_type='application/json', text=convert_json(result))


class SignOut(web.View):

    async def get(self, **kw):
        session = await get_session(self.request)
        if session.get('user'):
            del session['user']
            redirect(self.request, 'login')
        else:
            raise web.HTTPForbidden(body=b'Forbidden')







