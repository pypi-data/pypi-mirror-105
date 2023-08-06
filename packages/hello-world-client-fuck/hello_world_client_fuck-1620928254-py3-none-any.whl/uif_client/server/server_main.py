import requests
import json
import time
import threading
import socket
import subprocess
from aiohttp import web

SERVER_API_KEY = "123"
MAX_ALLOW_USING = 4
SERVER_API_PORT = 8081

g_user_list = {}
g_current_ip = '127.0.0.1'


def MyRequest(url, dicts, is_return=True):
    try:
        dicts['api_key'] = SERVER_API_KEY
        resp = requests.get(url, params=dicts, timeout=10)
        return resp.text
    except Exception as e:
        print(e)
    return ""


def ClientInfo():  # myself info
    # get IPv4
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(('8.8.8.8', 80))
        g_current_ip = s.getsockname()[0]
    except Exception as e:
        s.close()
        print(e)
        raise ValueError('failed to get VPS IPv4')
    return "http://%s:%s/api" % (g_current_ip, SERVER_API_PORT)


def Get(dicts, key, default_value=""):
    if key in dicts:
        return dicts[key]
    return default_value


def DisConnect(user_key, client_address):
    if user_key == "" or client_address == "":
        return
    payload = {
        'type': 'DisConnect',
        'user_key': user_key,
        'api_key': SERVER_API_KEY
    }
    MyRequest(client_address, payload)
    try:
        g_user_list[user_key]['using'].remove(client_address)
    except:
        pass


def CountUsedFlow(user_dict):
    for item in user_dict['used']:
        pass
    return


def CheckOutDate(user_dict):
    t = time.time()
    t = int(t)
    user_dict['last_time'] = t

    if 'pass_time' not in user_dict:
        user_dict['is_out_date'] = True
        return False
        # return True

    if user_dict > t:
        user_dict['is_out_date'] = True
        return True
    user_dict['is_out_date'] = False
    return False


def AddUser(user_key, client_address):
    if client_address in g_user_list[user_key]['using']:
        return
    g_user_list[user_key]['using'].append(client_address)
    if len(g_user_list[user_key]['using']) > MAX_ALLOW_USING:
        DisConnect(user_key, g_user_list[user_key]['using'].pop())


def UserLogin(params, user_key):
    if user_key not in g_user_list:
        g_user_list[user_key] = {}
        g_user_list[user_key]['using'] = []
    client_address = Get(params, 'client_address')
    if client_address == '':  # should not happen
        status = 2
    elif CheckOutDate(g_user_list[user_key]):
        status = 1
        for item in g_user_list[user_key]['using']:  # DisConnect all
            if item == client_address:  # avoid dead lock
                continue
            DisConnect(user_key, item)
    else:
        status = 0  # ok
        AddUser(user_key, client_address)

    return json.dumps({'params': g_user_list[user_key], 'status': status})


async def API(req):
    params = req.rel_url.query
    user_key = Get(params, 'user_key')
    api_key = Get(params, 'api_key')
    client_address = Get(params, 'client_address')
    if api_key != SERVER_API_KEY or user_key == '':
        return web.Response(text="missing SERVER_API_KEY or user_key")
    print('receive user_key: %s from %s' % (user_key, client_address))
    types = Get(params, 'type')
    text = "wrong type"
    if types == 'UserLogin':
        text = UserLogin(params, user_key)
    elif types == "DisConnect":
        text = DisConnect(user_key, client_address)
    return web.Response(text=text)


def HeartBeat():
    while True:
        time.sleep(200)
        for item in g_user_list:
            if 'using' not in item:
                continue
            for client_address in item['using']:
                payload = {'type': 'CheckAlive'}
                respon = MyRequest(client_address, payload)
                try:
                    if respon is '' or 'is_ok' not in respon:
                        g_user_list[item]['using'].remove(client_address)
                except:
                    pass


app = web.Application()
app.add_routes([web.get('/api', API)])

if __name__ == '__main__':
    print('server started.')
    threading.Thread(target=HeartBeat).start()
    web.run_app(app, host=g_current_ip, port=SERVER_API_PORT)
