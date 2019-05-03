#!/usr/bin/env python
# -*- coding: utf-8 -*-

#
# PlayFetch - Fetch playlists from GMusicProxy
# https://github.com/jeffmhubbard/playfetch
#

import argparse
import configparser
import sys
from os import path

import commands as cmd
from utils import debug, error


__APP_NAME__ = "playfetch"
__APP_DESC__ = "Fetch playlists from GMusicProxy"

__APP_DIRS__ = {
        'cache': path.expanduser('~/.cache/'+__APP_NAME__),
        'config': path.expanduser('~/.config/'+__APP_NAME__),
}

global DEFAULTS
DEFAULTS = {
    'proxy-url': 'http://localhost:9999',
    'plist-prefix': 'pf',
    'plist-dest': '~/.mpd/playlists',
    'mpd-host': 'localhost',
    'mpd-port': 6600,
    'auto-clear': 'false',
    'auto-load': 'false',
    'auto-start': 'false',
}


def main():

    args = read_args()

    if args.debug:
        global DEBUG
        DEBUG = True

    config = load_config(DEFAULTS)

    if args.clear is True:
        config['auto-clear'] = True

    if args.load is True:
        config['auto-load'] = True

    if args.start is True:
        config['auto-start'] = True

    if args.subparser:
        execute(config, args)


def execute(config, args):

    try:
        debug('subparser: %s' % args.subparser)
        run = getattr(cmd, args.subparser)
        run(config, args)
    except TypeError as e:
        error(e)


def read_args():

    parser = argparse.ArgumentParser(
        prog=__APP_NAME__,
        description="Fetch playlists from GMusicProxy")
    # debug
    parser.add_argument(
            '-d', '--debug',
            action='store_true',
            help="Print debug strings")
    # auto confirm
    parser.add_argument(
            '-f', '--force',
            action='store_true',
            help="Do not prompt for confirmation")
    # auto clear
    parser.add_argument(
            '-c', '--clear',
            action='store_true',
            help="Clear current MPD playlist")
    # auto load
    parser.add_argument(
            '-l', '--load',
            action='store_true',
            help="Append to current MPD playlist")
    # auto play
    parser.add_argument(
            '-s', '--start',
            action='store_true',
            help="Start current MPD playlist")

    # sub commands
    subparsers = parser.add_subparsers(dest='subparser')

    # playlists subcommand
    parser_shell = subparsers.add_parser(
            'shell',
            description="Start interative shell",
            usage="playfetch shell")

    # search subcommand
    parser_search = subparsers.add_parser(
            'search',
            description="Fetch playlist of search results",
            usage="playfetch [-fcls] search <string> -t <num> -e -a")
    # search string
    parser_search.add_argument(
            'search_string',
            action='store',
            help="Search string as 'Artist, Title'")
    # num tracks
    parser_search.add_argument(
            '-t', '--tracks',
            action='store',
            type=int,
            help="Number of tracks to return")
    # exact
    parser_search.add_argument(
            '-e', '--exact',
            action='store_true',
            help="Exact match only")
    # album
    parser_search.add_argument(
            '-a', '--album',
            action='store_true',
            help="Fetch album playlist")

    # radio subcommand
    parser_radio = subparsers.add_parser(
            'radio',
            description="Fetch new station playlist",
            usage="playfetch [-fcls] radio <string> -n <name> -t <num> -e")
    # search string
    parser_radio.add_argument(
            'search_string',
            action='store',
            help="Search string as 'Artist, Title'")
    # station name
    parser_radio.add_argument(
            '-n', '--name',
            action='store',
            help="Name of new station")
    # num tracks
    parser_radio.add_argument(
            '-t', '--tracks',
            action='store',
            type=int,
            help="Number of tracks to return")
    # exact
    parser_radio.add_argument(
            '-e', '--exact',
            action='store_true',
            help="Exact match only")

    # current subcommand
    parser_current = subparsers.add_parser(
            'current',
            description="Fetch new station playlist based on current song",
            usage="playfetch [-fcls] radio <string> -n <name> -t <num> -e")
    # num tracks
    parser_current.add_argument(
            '-t', '--tracks',
            action='store',
            type=int,
            help="Number of tracks to return")

    # top subcommand
    parser_top = subparsers.add_parser(
            'top',
            description="Fetch an Artist's Top Tracks playlist",
            usage="playfetch [-fcls] top <string> -t <num>")
    # search string
    parser_top.add_argument(
            'search_string',
            action='store',
            help="Search string as 'Artist'")
    # num tracks
    parser_top.add_argument(
            '-t', '--tracks',
            action='store',
            type=int,
            help="Number of tracks to return")

    # collection subcommand
    parser_collection = subparsers.add_parser(
            'collection',
            description="Fetch collection playlist",
            usage="playfetch [-fcls] collection -r <num> --shoff")
    # min rating
    parser_collection.add_argument(
            '-r', '--rating',
            action='store',
            type=int,
            help="Minimum track rating")
    # disable shuffle
    parser_collection.add_argument(
            '--shoff',
            action='store_true',
            help="Do not shuffle playlist")

    # promoted subcommand
    parser_promoted = subparsers.add_parser(
            'promoted',
            description="Fetch Promoted Tracks playlist",
            usage="playfetch [-fcls] promoted")
    # disable shuffle
    parser_promoted.add_argument(
            '--shoff',
            action='store_true',
            help="Do not shuffle playlist")

    # ifl subcommand
    parser_lucky = subparsers.add_parser(
            'lucky',
            description="Fetch I'm Feeling Lucky playlist",
            usage="playfetch [-fcls] lucky -t <num>")
    # num tracks
    parser_lucky.add_argument(
            '-t', '--tracks',
            action='store',
            type=int,
            help="Number of tracks to return")

    # stations subcommand
    parser_stations = subparsers.add_parser(
            'stations',
            description="Fetch all registered stations",
            usage="playfetch [-f] stations")

    # listen subcommand
    parser_listen = subparsers.add_parser(
            'listen',
            description="Fetch Listen Now stations",
            usage="playfetch [-f] listen --all")
    # listen artist
    parser_listen.add_argument(
            '-r', '--artist',
            action='store_true',
            help="Listen Now artist station playlists")
    # listen album
    parser_listen.add_argument(
            '-a', '--album',
            action='store_true',
            help="Listen Now suggested album playlists")
    # listen situation
    parser_listen.add_argument(
            '-s', '--situation',
            action='store_true',
            help="Listen Now situation playlists")
    # listen all
    parser_listen.add_argument(
            '--all',
            action='store_true',
            help="Fetch all Listen Now playlists")

    # playlists subcommand
    parser_playlists = subparsers.add_parser(
            'playlists',
            description="Fetch all user playlists",
            usage="playfetch [-f] playlists")

    # discog subcommand
    parser_discog = subparsers.add_parser(
            'discog',
            description="Fetch artist discography",
            usage="playfetch [-fcls] discog <string> -e")
    # search string
    parser_discog.add_argument(
            'search_string',
            action='store',
            help="Search string as 'Artist'")
    # exact
    parser_discog.add_argument(
            '-e', '--exact',
            action='store_true',
            help="Exact match only")

    # print current mpd playlist
    parser_show = subparsers.add_parser(
            'show',
            description="Print current MPD playlist",
            usage="playfetch show")
    # print status
    parser_show.add_argument(
            '-s', '--status',
            action='store_true',
            help="Also print MPD status")
    # print status only
    parser_show.add_argument(
            '-b', '--both',
            action='store_true',
            help="Print only MPD status")

    # list playlists in path
    parser_list = subparsers.add_parser(
            'list',
            description="List playlists with matching prefix",
            usage="playfetch list [-a]")
    # list all
    parser_list.add_argument(
            '-a', '--all',
            action='store_true',
            help="List all playlists")

    # purge playlists in path
    parser_purge = subparsers.add_parser(
            'purge',
            description="Delete playlists with matching prefix",
            usage="playfetch [-f] purge --[filter]")
    # filter searches
    parser_purge.add_argument(
            '--search',
            action='store_true',
            help="Filter search playlists")
    # filter radio
    parser_purge.add_argument(
            '--radio',
            action='store_true',
            help="Filter radio playlists")
    # purge all
    parser_purge.add_argument(
            '--station',
            action='store_true',
            help="Filter station playlists")
    # purge all
    parser_purge.add_argument(
            '--all',
            action='store_true',
            help="Delete *ALL* playlists")
    # older than
    parser_purge.add_argument(
            '-o', '--older',
            action='store',
            type=int,
            help="Number of hours")

    # rate current song
    parser_rate = subparsers.add_parser(
            'rate',
            description="rate song currently playing in MPD",
            usage="playfetch rate --[up/down]")
    # thumbs up
    parser_rate.add_argument(
            '-u', '--up',
            action='store_true',
            help="Thumbs up")
    # thumbs down
    parser_rate.add_argument(
            '-d', '--down',
            action='store_true',
            help="Thumbs down")

    return parser.parse_args(sys.argv[1:])


def load_config(defaults):

    config = defaults

    filename = path.join(__APP_DIRS__['config'], 'config')

    if path.exists(filename):
        user_conf = configparser.ConfigParser(config)
        user_conf.read(filename)

        try:
            for key in config.keys():
                config[key] = user_conf.get(__APP_NAME__, key)
        except Exception as e:
            error("Invalid config: %s" % e)
        return config


if __name__ == '__main__':
    main()