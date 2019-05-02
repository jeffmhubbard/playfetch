import os
import requests
import time
from os import path

import client as mpc
from shell import prompt
from utils import info, warn, error, debug
from utils import (
        get_filename,
        fetch_playlist,
        fetch_batch,
        fetch_albums,
        post_fetch,
        user_confirm)


def help(config, args):
    debug(args)
    error("Not implemented")


def shell(config, args):
    prompt(config)


def search(config, args):

    client = mpc.setup(config)

    url_name = 'search'
    url_cmd = '/get_by_search'
    url_opts = {
            'type': 'matches',
            'title': None,
            'artist': None,
            'exact': 'no',
            'num_tracks': '20'}

    if args.search_string:
        search = tuple(args.search_string.split(','))

        artist = search[0].rstrip(',')
        url_opts['artist'] = artist

        if len(search) >= 2:
            title = search[1].strip()
            url_opts['title'] = title
        else:
            title = None

    if args.tracks:
        url_opts['num_tracks'] = args.tracks

    if args.exact:
        url_opts['exact'] = 'yes'

    if args.album:
        url_opts['type'] = 'album'

    proxy_url = config['proxy-url']
    prefix = config['plist-prefix']
    dest = config['plist-dest']

    url_base = proxy_url + url_cmd
    request = requests.get(url_base, params=url_opts)
    debug('request.url: %s' % request.url)

    filename = get_filename(prefix, url_name, artist, title)
    playlist = path.join(dest, filename)

    if request and playlist:
        if fetch_playlist(request, playlist, args):
            config = post_fetch(config, args)
            mpc.ctrl(client, config, filename)

    mpc.end(client)


def top(config, args):

    client = mpc.setup(config)

    search_cmd = '/search_id'
    search_opts = {
            'type': 'artist',
            'artist': None,
            'exact': 'no'}

    url_name = 'toptracks'
    url_cmd = '/get_top_tracks_artist'
    url_opts = {
            'id': None,
            'type': 'artist',
            'num_tracks': '20'}

    if args.search_string:
        artist = args.search_string
        search_opts['artist'] = artist
    else:
        warn("needs artist")
        return

    if args.tracks:
        url_opts['num_tracks'] = int(args.tracks)

    proxy_url = config['proxy-url']
    prefix = config['plist-prefix']
    dest = config['plist-dest']

    search_url = proxy_url + search_cmd
    search_req = requests.get(search_url, params=search_opts)

    if search_req.status_code == 200:
        url_opts['id'] = search_req.text

        url_base = proxy_url + url_cmd
        request = requests.get(url_base, params=url_opts)
        debug('request.url: %s' % request.url)

        filename = get_filename(prefix, url_name, artist, title=None)
        playlist = path.join(dest, filename)

        if request and playlist:
            if fetch_playlist(request, playlist, args):
                config = post_fetch(config, args)
                mpc.ctrl(client, config, filename)

    mpc.end(client)


def playlists(config, args):

    url_name = 'playlists'
    url_cmd = '/get_all_playlists'
    url_opts = {'format': 'text'}

    proxy_url = config['proxy-url']
    prefix = config['plist-prefix']

    url_base = proxy_url + url_cmd
    request = requests.get(url_base, params=url_opts)
    debug('request.url: %s' % request.url)

    if fetch_batch(config, request, prefix, url_name, args):
        info("Stations fetched!")


def stations(config, args):

    url_name = 'stations'
    url_cmd = '/get_all_stations'
    url_opts = {'format': 'text'}

    proxy_url = config['proxy-url']
    prefix = config['plist-prefix']

    url_base = proxy_url + url_cmd
    request = requests.get(url_base, params=url_opts)
    debug('request.url: %s' % request.url)

    if fetch_batch(config, request, prefix, url_name, args):
        info("Stations fetched!")


def list(config, args):

    client = mpc.setup(config)

    match = config['plist-prefix']

    if args.all:
        match = None

    display = []

    for item in mpc.list_playlists(client):
        if args.all:
            display.append(item['playlist'])
        elif item['playlist'].split('-')[0] == match:
            display.append(item['playlist'])

    # Print
    display.sort()
    for line in display:
        info(line)

    mpc.end(client)


def promoted(config, args):

    client = mpc.setup(config)

    url_name = "promoted"
    url_cmd = "/get_promoted"
    url_opts = {'shuffle': 'yes'}

    if args.shoff:
        url_opts['shuffle'] = False

    proxy_url = config['proxy-url']
    prefix = config['plist-prefix']
    dest = config['plist-dest']

    url_base = proxy_url + url_cmd
    request = requests.get(url_base, params=url_opts)
    debug('request.url: %s' % request.url)

    filename = get_filename(prefix, url_name, artist=None, title=None)
    playlist = path.join(dest, filename)

    if request and playlist:
        if fetch_playlist(request, playlist, args):
            config = post_fetch(config, args)
            mpc.ctrl(client, config, filename)

    mpc.end(client)


def current(config, args):

    client = mpc.setup(config)

    playid = mpc.get_playid(client)

    url_name = "current"
    url_cmd = "/get_new_station_by_id"
    url_opts = {
            'id': playid,
            'num_tracks': '20',
            'type': 'song',
            'transient': 'yes',
            'name': None}

    if args.tracks:
        url_opts['num_tracks'] = args.tracks

    proxy_url = config['proxy-url']
    prefix = config['plist-prefix']
    dest = config['plist-dest']

    url_base = proxy_url + url_cmd
    request = requests.get(url_base, params=url_opts)
    debug('request.url: %s' % request.url)

    filename = get_filename(prefix, url_name)
    playlist = path.join(dest, filename)

    if request and playlist:
        if fetch_playlist(request, playlist, args):
            config = post_fetch(config, args)
            mpc.ctrl(client, config, filename)

    mpc.end(client)


def radio(config, args):

    client = mpc.setup(config)

    url_name = "radio"
    url_cmd = "/get_new_station_by_search"
    url_opts = {
            'type': 'artist',
            'title': None,
            'artist': None,
            'exact': 'no',
            'num_tracks': '20',
            'type': 'artist',
            'transient': 'yes',
            'name': None}

    if args.search_string:
        search = tuple(args.search_string.split(','))

        artist = search[0].rstrip(',')
        url_opts['artist'] = artist

        if len(search) >= 2:
            title = search[1].strip()
            url_opts['title'] = title
        else:
            title = None

    if args.name:
        url_opts['transient'] = 'no'
        url_opts['name'] = args.name

    if args.tracks:
        url_opts['num_tracks'] = args.tracks

    if args.exact:
        url_opts['exact'] = 'yes'

    proxy_url = config['proxy-url']
    prefix = config['plist-prefix']
    dest = config['plist-dest']

    url_base = proxy_url + url_cmd
    request = requests.get(url_base, params=url_opts)
    debug('request.url: %s' % request.url)

    filename = get_filename(prefix, url_name, artist, title)
    playlist = path.join(dest, filename)

    if request and playlist:
        if fetch_playlist(request, playlist, args):
            config = post_fetch(config, args)
            mpc.ctrl(client, config, filename)

    mpc.end(client)


def lucky(config, args):

    client = mpc.setup(config)

    url_name = 'lucky'
    url_cmd = '/get_ifl_station'
    url_opts = {'num_tracks': 20}

    if args.tracks:
        debug('tracks: %s' % args.tracks)
        url_opts['num_tracks'] = int(args.tracks)

    proxy_url = config['proxy-url']
    prefix = config['plist-prefix']
    dest = config['plist-dest']

    url_base = proxy_url + url_cmd
    request = requests.get(url_base, params=url_opts)
    debug('request.url: %s' % request.url)

    filename = get_filename(prefix, url_name, artist=None, title=None)
    playlist = path.join(dest, filename)

    if request and playlist:
        debug('request: %s' % request)
        debug('playlist: %s' % playlist)
        if fetch_playlist(request, playlist, args):
            config = post_fetch(config, args)
            mpc.ctrl(client, config, filename)

    mpc.end(client)


def collection(config, args):

    client = mpc.setup(config)

    url_name = "collection"
    url_cmd = "/get_collection"
    url_opts = {
            'shuffle': 'yes',
            'rating': 2}

    if args.rating:
        debug('rating: %s' % args.rating)
        url_opts['rating'] = args.rating

    if args.shoff:
        debug('shoff: %s' % args.shoff)
        url_opts['shuffle'] = False

    proxy_url = config['proxy-url']
    prefix = config['plist-prefix']
    dest = config['plist-dest']

    url_base = proxy_url + url_cmd
    request = requests.get(url_base, params=url_opts)
    debug('request.url: %s' % request.url)

    filename = get_filename(prefix, url_name, artist=None, title=None)
    playlist = path.join(dest, filename)

    if request and playlist:
        debug('request: %s' % request)
        debug('playlist: %s' % playlist)
        if fetch_playlist(request, playlist, args):
            config = post_fetch(config, args)
            mpc.ctrl(client, config, filename)

    mpc.end(client)


def show(config, args):

    client = mpc.setup(config)

    plist = True
    status = False

    if args.status:
        debug('status: %s' % args.status)
        plist = False
        status = True

    if args.both:
        debug('both: %s' % args.both)
        plist = True
        status = True

    if plist:
        mpc.playlist(client)
    if status:
        if plist:
            print(u'\u2500'*80)
        mpc.status(client)

    mpc.end(client)


def rate(config, args):

    client = mpc.setup(config)

    playid = mpc.get_playid(client)

    url_opts = {'id': playid}

    if args.up:
        url_cmd = '/like_song'
        success = 'Thumbs up!'
        skip = False
    elif args.down:
        url_cmd = '/dislike_song'
        success = 'Thumbs down!'
        skip = True
    else:
        pass

    proxy_url = config['proxy-url']
    url_base = proxy_url + url_cmd
    request = requests.get(url_base, params=url_opts)
    debug('request.url: %s' % request.url)

    if request.status_code == 200:
        info(success)
        if skip:
            mpc.next(client)

    mpc.end(client)


def purge(config, args):

    client = mpc.setup(config)

    dest = path.expanduser(config['plist-dest'])
    prefix = config['plist-prefix']

    if not prefix == '':
        prefix += '-'

    if args.search:
        prefix += 'search'

    elif args.radio:
        prefix += 'radio'

    elif args.station:
        prefix += 'station'

    elif args.all:
        prefix = ''

    if args.older:
        older = int(args.older)

    plist_data = mpc.listplaylists(client)

    to_delete = []

    for dirfile in plist_data:
        if dirfile['playlist'].startswith(prefix):
            to_delete.append(dirfile)
    debug("to_delete: {}, {}".format(len(to_delete), to_delete))

    if args.older and older > 0:
        older_than = []
        now = time.time()
        hours = older * 3600

        for dfile in to_delete:
            fext = dfile['playlist']
            fext += ".m3u"
            mtime = path.getmtime(path.join(dest, fext))
            difftime = int(now - mtime)

            if difftime > hours:
                older_than.append(dfile)

        if len(older_than) > 0:
            debug("older_than: {}, {}".format(len(older_than), older_than))
            to_delete = older_than

    if len(to_delete) == 0:
        warn("No playlists to delete")
        return

    for pname in to_delete:
        pname = pname['playlist']+".m3u"
        fname = path.join(config['plist-dest'], pname)
        fpath = path.expanduser(fname)

        if path.exists(fpath):
            if not args.force:
                if not user_confirm('Delete: %s' % pname):
                    continue
            try:
                os.remove(fpath)
                info("Deleted: %s" % pname)
            except Exception as e:
                error(e)

    mpc.end(client)


def m(config, args):

    client = mpc.setup(config)

    if args.play:
        mpc.play(client)
    elif args.pause:
        mpc.pause(client)
    elif args.stop:
        mpc.stop(client)
    elif args.next:
        mpc.next(client)
    elif args.prev:
        mpc.prev(client)
    else:
        pass

    mpc.end(client)


