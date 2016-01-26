#!/usr/bin/python
# -*- coding: utf8 -*-
from logging.config import dictConfig
from subprocess import check_output
from logging import getLogger
import yaml
import re


class XRandr(object):
    _info = None

    def __init__(self):
        with open('/etc/zsupply.yml') as fd:
            self.config = yaml.load(fd)
        dictConfig(self.config['logging'])
        self.logger = getLogger('xrandr')
        self.logger.debug('XRandr: Init')

    @property
    def info(self):
        if self._info is None:
            self._info = self._run(['xrandr'])
        return self._info

    def _run(self, args):
        self.logger.debug('XRandr: run %s' % repr(args))
        return check_output(args, env={
            'DISPLAY': ':0.0',
            'XAUTHORITY': '/home/%s/.Xauthority' % self.config['user']
        })

    def is_connected(self, screen):
        x = '%s connected' % screen in self.info
        self.logger.debug('XRandr: %s is_connected: %s' % (screen, x))
        return x

    def enable_only(self, screen,):
        self.logger.debug('XRandr: enable only: %s' % screen)
        args = ['xrandr']
        for d in self.list():
            if d == screen:
                args += ['--output', screen, '--preferred', '--primary']
            else:
                args += ['--output', d, '--off']
        self._run(args)
        self._info = None

    def list(self):
        m = re.findall(r'^([^\s]+)', self.info, re.MULTILINE)
        m.remove('Screen')
        return m


def main():
    xrandr = XRandr()

    try:
        if xrandr.is_connected('HDMI3'):
            xrandr.enable_only('HDMI3')

        elif xrandr.is_connected('HDMI1'):
            xrandr.enable_only('HDMI1')

        else:
            xrandr.enable_only('LVDS1')
    except:
        xrandr.logger.debug('XRandr: exception:\n', exc_info=True)
        raise


if __name__ == '__main__':
    main()
