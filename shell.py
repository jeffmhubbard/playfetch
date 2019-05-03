import argparse
import shlex

from prompt_toolkit.completion import FuzzyWordCompleter
from prompt_toolkit.history import InMemoryHistory
from prompt_toolkit.shortcuts import PromptSession
from prompt_toolkit.auto_suggest import AutoSuggestFromHistory

import commands as cmd
from utils import info, error, debug

command_completer = FuzzyWordCompleter([
    'help', 'search', 'current', 'top',
    'discog', 'radio', 'listen', 'lucky',
    'promoted', 'collection', 'stations',
    'playlists', 'purge', 'list', 'show',
    '--tracks', '--rating', '--exact',
    '--album', '--name', '--artist',
    '--situation', '--all', '--status',
    '--both', '--shoff', '--up', '--down',
    '--force', '--clear', '--load', '--start',
    '--play', '--pause', '--stop', '--next', '--prev',
])


class ShellCmdError(Exception):
    pass


class ShellCmdParser(argparse.ArgumentParser):

    def error(self, message):
        raise ShellCmdError(message)


def prompt(config):

    info("♫ pf-shell - 0.1")
    info('(Ctrl+D to quit)')

    history = InMemoryHistory()
    session = PromptSession(
            history=history,
            enable_history_search=True,
            auto_suggest=AutoSuggestFromHistory(),
            completer=command_completer,
            complete_while_typing=True,)

    while True:
        try:
            command = session.prompt('▶ ')
            if command:
                args = get_args(command)
                execute(config, args)

        except ShellCmdError as e:
            error("%s" % e)

        except KeyboardInterrupt:
            pass

        except EOFError:
            break

        except Exception as e:
            error(e)
            break


def get_args(command):

    main_parser = ShellCmdParser(add_help=False)
    main_parser.add_argument(
            '-F', '--force',
            action='store_true')

    post_parser = ShellCmdParser(add_help=False)
    post_parser.add_argument(
            '-C', '--clear',
            action='store_true')
    post_parser.add_argument(
            '-L', '--load',
            action='store_true')
    post_parser.add_argument(
            '-S', '--start',
            action='store_true')

    parser = ShellCmdParser(add_help=False)
    subparsers = parser.add_subparsers(dest='subparser')

    parser_mpc = subparsers.add_parser(
            'm',
            add_help=False)
    parser_mpc.add_argument(
            '--play',
            action='store_true')
    parser_mpc.add_argument(
            '--pause',
            action='store_true')
    parser_mpc.add_argument(
            '--stop',
            action='store_true')
    parser_mpc.add_argument(
            '--next',
            action='store_true')
    parser_mpc.add_argument(
            '--prev',
            action='store_true')

    parser_help = subparsers.add_parser(
            'help',
            add_help=False)

    parser_search = subparsers.add_parser(
            'search',
            parents=[main_parser, post_parser],
            add_help=False)
    parser_search.add_argument(
            'search_string',
            action='store')
    parser_search.add_argument(
            '-t', '--tracks',
            action='store',
            type=int)
    parser_search.add_argument(
            '-e', '--exact',
            action='store_true')
    parser_search.add_argument(
            '-a', '--album',
            action='store_true')

    parser_current = subparsers.add_parser(
            'current',
            parents=[main_parser, post_parser],
            add_help=False)
    parser_current.add_argument(
            '-t', '--tracks',
            action='store',
            type=int)

    parser_radio = subparsers.add_parser(
            'radio',
            parents=[main_parser, post_parser],
            add_help=False)
    parser_radio.add_argument(
            'search_string',
            action='store')
    parser_radio.add_argument(
            '-n', '--name',
            action='store')
    parser_radio.add_argument(
            '-t', '--tracks',
            action='store',
            type=int)
    parser_radio.add_argument(
            '-e', '--exact',
            action='store_true')

    parser_promoted = subparsers.add_parser(
            'promoted',
            parents=[main_parser, post_parser],
            add_help=False)
    parser_promoted.add_argument(
            '--shoff',
            action='store_true')

    parser_discog = subparsers.add_parser(
            'discog',
            parents=[main_parser],
            add_help=False)
    parser_discog.add_argument(
            'search_string',
            action='store')
    parser_discog.add_argument(
            '-e', '--exact',
            action='store_true')

    parser_lucky = subparsers.add_parser(
            'lucky',
            parents=[main_parser, post_parser],
            add_help=False)
    parser_lucky.add_argument(
            '-t', '--tracks',
            action='store',
            type=int)

    parser_collection = subparsers.add_parser(
            'collection',
            parents=[main_parser, post_parser],
            add_help=False)
    parser_collection.add_argument(
            '-r', '--rating',
            action='store',
            type=int)
    parser_collection.add_argument(
            '--shoff',
            action='store')

    parser_top = subparsers.add_parser(
            'top',
            parents=[main_parser, post_parser],
            add_help=False)
    parser_top.add_argument(
            'search_string',
            action='store')
    parser_top.add_argument(
            '-t', '--tracks',
            action='store',
            type=int)

    parser_stations = subparsers.add_parser(
            'stations',
            parents=[main_parser],
            add_help=False)

    parser_playlists = subparsers.add_parser(
            'playlists',
            parents=[main_parser],
            add_help=False)

    parser_show = subparsers.add_parser(
            'show',
            add_help=False)
    parser_show.add_argument(
            '-s', '--status',
            action='store_true')
    parser_show.add_argument(
            '-b', '--both',
            action='store_true')

    parser_list = subparsers.add_parser(
            'list',
            add_help=False)
    parser_list.add_argument(
            '-a', '--all',
            action='store_true')

    parser_rate = subparsers.add_parser(
            'rate',
            add_help=False)
    parser_rate.add_argument(
            '-u', '--up',
            action='store_true')
    parser_rate.add_argument(
            '-d', '--down',
            action='store_true')

    parser_purge = subparsers.add_parser(
            'purge',
            parents=[main_parser],
            add_help=False)
    parser_purge.add_argument(
            '--search',
            action='store_true')
    parser_purge.add_argument(
            '--radio',
            action='store_true')
    parser_purge.add_argument(
            '--station',
            action='store_true')
    parser_purge.add_argument(
            '--all',
            action='store_true')
    parser_purge.add_argument(
            '-o', '--older',
            action='store',
            type=int)

    return parser.parse_args(shlex.split(command, posix=True))


def execute(config, args):

    try:
        debug('subparser: %s' % args.subparser)
        run = getattr(cmd, args.subparser)
        run(config, args)
    except TypeError as e:
        error(e)
