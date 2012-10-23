"""Routines to access a luca file tree."""

import ConfigParser
import os
from datetime import datetime
from .ofx import institutions, parse

class NotFound(Exception):
    """File not found."""

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
            password=config.get(nickname, 'password') if
              config.has_option(nickname, 'password') else None,
            )
    return logins

def ofxdir():
    if not os.path.isdir('ofx'):
        os.mkdir('ofx')
    return 'ofx'

def ofx_listdir():
    return sorted(os.listdir(ofxdir()))

def ofx_create(filename, data):
    """Create a unique filename suffixed with the current date."""
    before, after = filename.split('DATE', 1)
    letter = ''
    while True:
        date = datetime.now().strftime('%Y-%m-%d')
        filename = before + date + letter + after
        pathname = os.path.join(ofxdir(), filename)
        try:
            fd = os.open(pathname, os.O_WRONLY | os.O_CREAT | os.O_EXCL, 0666)
        except OSError:
            letter = chr(ord(letter or 'a') + 1)
        else:
            break
    with os.fdopen(fd, 'wb') as f:
        f.write(data)

        # Make the file read-only now that it contains data.
        mask = os.umask(0)
        os.umask(mask)
        os.fchmod(fd, 0444 & ~mask)

def ofx_open(filename, mode='rb'):
    return open(os.path.join(ofxdir(), filename), mode)

def get_most_recent_xml(prefix):
    """Parse the the most recent file starting with ``prefix``."""
    filenames = [ f for f in ofx_listdir() if f.startswith(prefix) ]
    if not filenames:
        raise NotFound(prefix + '*')
    filename = filenames[-1]
    with open(os.path.join('ofx', filename)) as f:
        data = f.read()
    if data.startswith('<?xml'):
        headers = {}  # TODO: pull attributes from <?OFX> tag
        xml = data
    else:
        blankline = '\r\n\r\n' if '\r\n\r\n' in data else '\n\n'
        heading, xml = data.split(blankline)
        headers = { key: value for key, value in (
                line.split(':', 1) for line in heading.split('\r\n')
                )}
    return headers, xml

def get_most_recent_accounts(login):
    prefix = login.nickname + '-accounts-'
    try:
        headers, ofx = get_most_recent_xml(prefix)
    except NotFound:
        return None
    else:
        return parse.accounts(ofx)

def get_most_recent_activity(login):
    prefix = login.nickname + '-activity-'
    try:
        headers, ofx = get_most_recent_xml(prefix)
    except NotFound:
        return {}, {}
    else:
        return parse.activity(ofx)
