import uuid
import socket
import time
import requests
import subprocess
import os
import sys


SERVER_API_KEY = '123'
BASE_DIR = os.path.abspath(os.path.dirname(__file__))
BASE_DIR = BASE_DIR.replace('\\', '/')

try:
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.connect(('8.8.8.8', 80))
    g_current_ip = s.getsockname()[0]
    g_current_ip = '127.0.0.1'
    print(g_current_ip)
except Exception as e:
    s.close()
    print(e)
    raise ValueError('failed to get VPS IPv4')


def MyRequest(url, dicts):
    try:
        global SERVER_API_KEY
        dicts['api_key'] = SERVER_API_KEY
        resp = requests.get(url, params=dicts, timeout=10)
        return resp.text
    except Exception as e:
        print(e)
    return ""


def RunCMD(cmd, is_wait=True):
    print('=' * 10)
    print('is_wait: %s $: %s' % (is_wait, cmd))
    print('↓' * 10)
    sys.stdout.flush()
    if is_wait:
        subprocess.Popen(cmd, shell=True).wait()
    else:
        subprocess.Popen(cmd, shell=True)


#install deps
RunCMD('python3 -m pip install psutil')
RunCMD('python3 -m pip install aiohttp')
RunCMD('python3 -m pip install requests')
RunCMD('python3 -m pip install ntplib')

import install

# run server and client
RunCMD('python3 %s' % (BASE_DIR + '/main.py'), is_wait=False)
RunCMD('python3 %s' % (BASE_DIR + '/server/server_main.py'), is_wait=False)

time.sleep(20)  # wait them to be ok.

# check UserLogin function
my_uuid = uuid.uuid1()
url = 'http://%s:8082' % (g_current_ip)

print('UserLogin ', MyRequest(url, {'type': 'UserLogin', 'user_key': my_uuid}))

# check DisConnect function
print('DisConnect ', MyRequest(url, {
    'type': 'DisConnect',
    'user_key': my_uuid
}))

RunCMD('python3 %s --stop' % (BASE_DIR + '/main.py'))
