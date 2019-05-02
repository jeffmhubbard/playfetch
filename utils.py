import re
import string
from datetime import datetime
from os import path

import requests
from prompt_toolkit import prompt

DEBUG = False


def info(msg):
    print("> %s" % msg)


def error(msg):
    print("ERROR: %s" % msg)


def warn(msg):
    print("WARN: %s" % msg)


def debug(msg):
    if DEBUG:
        print("DEBUG: %s" % msg)


def time_format(seconds):

    dtime = round(float(seconds))
    return datetime.strftime(datetime.utcfromtimestamp(dtime), "%M:%S")


def user_confirm(question):

    answer = prompt('%s. Continue? (y/n) [y]: ' % question)
    return answer.lower() in ('', "yes", "y", "true", "t", "1", "on")


def get_valid_str(text):

    vchar = "-_.()[] %s%s" % (string.ascii_letters, string.digits)
    text = re.sub('\s', '_', text)
    return ''.join(c for c in text if c in vchar)


def get_filename(prefix=None, command=None, artist=None, title=None, ext=".m3u"):

    str_list = []

    if prefix:
        str_list.append(get_valid_str(prefix))

    if command:
        str_list.append(get_valid_str(command))

    if artist:
        str_list.append(get_valid_str(artist))

    if title:
        str_list.append(get_valid_str(title))

    if len(str_list) > 0:
        filename = '-'.join(str_list)
        filename += ext
        return filename.lower()

    else:
        return False


def fetch_playlist(results, filename, args):

    filename = path.expanduser(filename)

    if not results.status_code == 200:
        warn('Request failed: %s' % results.status_code)
        return False

    if path.exists(filename):
        if not args.force:
            if not user_confirm('File exists: %s' % path.basename(filename)):
                warn('User aborted!')
                return False

    with open(filename, 'wb') as fd:
        for chunk in results.iter_content(chunk_size=128):
            fd.write(chunk)
        info('Fetch: ' + path.basename(filename))
        return True


def fetch_batch(config, results, prefix, command, args):

    for line in results.text.splitlines():
        if len(line) > 0:

            name, url = line.split('|')
            if command == 'listen':
                junk, name = name.split(' - ')
            filename = path.join(
                    config['plist-dest'],
                    get_filename(prefix, command, name))

            subreq = requests.get(url)
            fetch_playlist(subreq, filename, args)


def fetch_albums(config, results, prefix, command, artist, args):

    for line in results.text.splitlines():
        if len(line) > 0:

            title, year, url = line.split('|')
            album = artist+'-'+year+'-'+title

            filename = path.join(
                    config['plist-dest'],
                    get_filename(prefix, command, album))

            subreq = requests.get(url)
            fetch_playlist(subreq, filename, args)


def post_fetch(config, args):
    if args.clear:
        config['auto-clear'] = True
    if args.load:
        config['auto-load'] = True
    if args.start:
        config['auto-start'] = True
    return config
