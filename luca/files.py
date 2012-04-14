"""Routines to access a luca file tree."""

import ConfigParser
import os
from .ofx import institutions

class Login(object):
    def __init__(self, nickname, fi, username, password):
        self.nickname = nickname
        self.fi = fi
        self.username = username
        self.password = password

def parse_ini():
    config = ConfigParser.RawConfigParser()
    with open('luca.ini') as f:
        config.readfp(f)
    return config

def read_logins():
    config = parse_ini()
    nicknames = config.sections()
    logins = {}
    for nickname in nicknames:
        iname = config.get(nickname, 'institution')
        logins[nickname] = Login(
            nickname=nickname,
            fi=institutions.db[iname],
            username=config.get(nickname, 'username'),
            password=config.get(nickname, 'password'),
            )
    return logins

def ofx_listdir():
    if not os.path.isdir('ofx'):
        os.mkdir('ofx')
    return sorted(os.listdir('ofx'))

def ofx_open(filename, mode='rb'):
    if not os.path.isdir('ofx'):
        os.mkdir('ofx')
    return open(os.path.join('ofx', filename), mode)

def get_most_recent_account_list(login):
    prefix = login.nickname + '-accounts-'
    filenames = [ f for f in ofx_listdir() if f.startswith(prefix) ]
    if not filenames:
        return None
    filename = filenames[-1]
    with open(os.path.join('ofx', filename)) as f:
        return f.read()
