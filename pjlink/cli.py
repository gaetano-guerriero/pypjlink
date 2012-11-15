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
from pjlink.cliutils import make_command

def cmd_power(p, state=None):
    if state is None:
        return p.get_power()
    p.set_power(state)

def make_parser():
    parser = argparse.ArgumentParser()
    parser.add_argument('-p', '--projector')

    sub = parser.add_subparsers(title='command')

    power = make_command(sub, 'power', cmd_power)

    return parser

def resolve_projector(projector):
    # host:port
    if projector is not None and ':' in projector:
        host, port = projector.rsplit(':', 1)
        port = int(port)

    # maybe defined in config
    else:
        appdir = appdirs.user_data_dir('pjlink')
        conf_file = path.join(appdir, 'pjlink.conf')

        try:
            config = ConfigParser({'port': '4352'})
            with open(conf_file, 'r') as f:
                config.readfp(f)

            section = projector
            if projector is None:
                section = 'default'

            host = config.get(section, 'host')
            port = config.getint(section, 'port')

        except (NoSectionError, IOError):
            if projector is None:
                raise KeyError('No default projector defined in %s' % conf_file)

            # no config file, or no projector defined for this host
            # thus, treat the projector as a hostname w/o port
            host = projector
            port = 4352

    return host, port

def main():
    parser = make_parser()
    args = parser.parse_args()

    kwargs = dict(args._get_kwargs())
    func = kwargs.pop('__func__')

    projector = kwargs.pop('projector')
    host, port = resolve_projector(projector)

    sock = socket()
    sock.connect((host, port))
    f = sock.makefile()

    proj = Projector(f)
    rv = proj.authenticate(getpass)
    if rv is False:
        print>>sys.stderr, 'Incorrect password.'
        return

    func(proj, **kwargs)

if __name__ == '__main__':
    main()
