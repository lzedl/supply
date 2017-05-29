#!/usr/bin/python2
# -*- coding: utf8 -*-
from dbus import SessionBus
from dbus.exceptions import DBusException
from subprocess import check_call, Popen
from argparse import ArgumentParser
from time import sleep
import re


class Spotify(object):
    BUS_NAME = 'org.mpris.MediaPlayer2.spotify'
    OBJECT_PATH = '/org/mpris/MediaPlayer2'
    DBUS_INTERFACE = 'org.mpris.MediaPlayer2.Player'
    SERVICE_UNKNOWN_ERROR = 'org.freedesktop.DBus.Error.ServiceUnknown'

    obj = None

    def __init__(self):
        self.bus = SessionBus()
        self.connect()

    def connect(self):
        try:
            self.obj = self.bus.get_object(self.BUS_NAME, self.OBJECT_PATH)
        except DBusException as e:
            if e.get_dbus_name() != self.SERVICE_UNKNOWN_ERROR:
                raise

    @property
    def is_connected(self):
        return self.obj is not None

    def toggle(self):
        self.obj.PlayPause(dbus_interface=self.DBUS_INTERFACE)

    def open(self, uri):
        if not self.is_connected:
            self.run()
            self.connect()
        if uri.startswith('https://open.spotify.com/'):
            m = re.match(
                r'https://open\.spotify\.com/(?P<type>\w+?)/(?P<id>.+)$',
                uri
            )
            self.obj.OpenUri('spotify:%s:%s' % (m.group('type'),
                                                m.group('id')),
                             dbus_interface=self.DBUS_INTERFACE)
        elif uri.startswith('spotify:'):
            self.obj.OpenUri(uri, dbus_interface=self.DBUS_INTERFACE)

    def run(self):
        Popen(['spotify'])
        sleep(2)

    def next(self):
        self.obj.Next(dbus_interface=self.DBUS_INTERFACE)

    def previous(self):
        self.obj.Previous(dbus_interface=self.DBUS_INTERFACE)


class MPD(object):
    def play(self):
        check_call(['mpc', 'play'])

    def pause(self):
        check_call(['mpc', 'pause'])

    def toggle(self):
        check_call(['mpc', 'toggle'])

    def next(self):
        check_call(['mpc', 'next'])

    def previous(self):
        check_call(['mpc', 'prev'])


def main():
    parser = ArgumentParser()
    sub = parser.add_subparsers(title='command', dest='command',
                                help='one of toggle, open')

    parser_toggle = sub.add_parser('toggle')

    parser_open = sub.add_parser('open')
    parser_open.add_argument('--uri', type=str, required=True)

    parser_next = sub.add_parser('next')

    parser_prev = sub.add_parser('previous')

    options = parser.parse_args()

    spotify = Spotify()
    mpd = MPD()

    if options.command == 'toggle':
        if spotify.is_connected:
            spotify.toggle()
        else:
            mpd.toggle()
    elif options.command == 'open':
        mpd.pause()
        spotify.open(options.uri)
    elif options.command == 'next':
        if spotify.is_connected:
            spotify.next()
        else:
            mpd.next()
    elif options.command == 'previous':
        if spotify.is_connected:
            spotify.previous()
        else:
            mpd.previous()


if __name__ == '__main__':
    main()
