import argparse
from ConfigParser import (
    NoSectionError,
    SafeConfigParser as ConfigParser
)
from getpass import getpass
from os import path
from socket import socket
import sys

import appdirs

from pjlink import Projector
from pjlink import projector
from pjlink.cliutils import make_command

def cmd_power(p, state=None):
    if state is None:
        print p.get_power()
    else:
        p.set_power(state)

def cmd_input(p, source, number):
    if source is None:
        source, number = p.get_input()
        print source, number
    else:
        p.set_input(source, number)

def make_parser():
    parser = argparse.ArgumentParser()
    parser.add_argument('-p', '--projector')

    sub = parser.add_subparsers(title='command')

    power = make_command(sub, 'power', cmd_power)
    power.add_argument('state', nargs='?', choices=('on', 'off'))

    inpt = make_command(sub, 'input', cmd_input)
    inpt.add_argument('source', nargs='?', choices=projector.SOURCE_TYPES)
    inpt.add_argument('number', nargs='?', choices='123456789', default='1')

    return parser

def resolve_projector(projector):
    password = None

    # host:port
    if projector is not None and ':' in projector:
        host, port = projector.rsplit(':', 1)
        port = int(port)

    # maybe defined in config
    else:
        appdir = appdirs.user_data_dir('pjlink')
        conf_file = path.join(appdir, 'pjlink.conf')

        try:
            config = ConfigParser({'port': '4352', 'password': ''})
            with open(conf_file, 'r') as f:
                config.readfp(f)

            section = projector
            if projector is None:
                section = 'default'

            host = config.get(section, 'host')
            port = config.getint(section, 'port')
            password = config.get(section, 'password') or None

        except (NoSectionError, IOError):
            if projector is None:
                raise KeyError('No default projector defined in %s' % conf_file)

            # no config file, or no projector defined for this host
            # thus, treat the projector as a hostname w/o port
            host = projector
            port = 4352

    return host, port, password

def main():
    parser = make_parser()
    args = parser.parse_args()

    kwargs = dict(args._get_kwargs())
    func = kwargs.pop('__func__')

    projector = kwargs.pop('projector')
    host, port, password = resolve_projector(projector)

    sock = socket()
    sock.connect((host, port))
    f = sock.makefile()

    if password:
        get_password = lambda: password
    else:
        get_password = getpass

    proj = Projector(f)
    rv = proj.authenticate(get_password)
    if rv is False:
        print>>sys.stderr, 'Incorrect password.'
        return

    func(proj, **kwargs)

if __name__ == '__main__':
    main()
