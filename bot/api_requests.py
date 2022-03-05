import aiohttp

HOST = 'http://127.0.0.1:8000'

async def get(url, data: dict = None):
    async with aiohttp.ClientSession() as session:
        res = await session.get(url, headers={
            'Content-Type': 'application/json',
        }, json=data)
        return await res.json()


async def get_admins():
    return await get(f'{HOST}/admins/')


async def user_get_or_create(user_id, **data):
    return await get(f'{HOST}/user/', data={
        'user_id': user_id,
        'data': data
    })


async def email_get(**kwargs):
    return await get(f'{HOST}/mail/', data={
        'data': kwargs,
    })


async def email_objects_filter(user_id, **kwargs):
    return await get(f'{HOST}/mails/', data={
        'user_id': user_id,
        'data': kwargs,
    })


async def email_create(user_id, **kwargs):
    await get(f'{HOST}/newmail/', data={
        'user_id': user_id,
        'data': kwargs
    })
