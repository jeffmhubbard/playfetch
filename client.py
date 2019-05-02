import sys

from mpd import MPDClient

from utils import info, warn, error, debug
from utils import time_format


def setup(config):
    host = config['mpd-host']
    port = config['mpd-port']

    client = MPDClient()
    client.connect(host, port)

    return client


def end(client):

    client.close()
    client.disconnect()


def play(client):

    client.play()


def pause(client):

    client.pause()


def stop(client):

    client.stop()


def next(client):

    client.next()


def prev(client):

    client.prev()


def ctrl(client, config, playlist=None):

    try:
        snum = len(client.playlistinfo())
    except Exception:
        snum = 0

    auto_clear = str(config['auto-clear']).lower()
    if auto_clear == 'true':
        client.clear()
        snum = 0

    auto_load = str(config['auto-load']).lower()
    if auto_load == 'true' and playlist:
        playlist = playlist.split('.')[0]
        client.load(playlist)

    auto_start = str(config['auto-start']).lower()
    if auto_start == 'true':
        client.play(snum)


def playlist(client):

    plist_info = client.playlistinfo()

    col_width = len(str(len(plist_info)+1))+1

    if len(plist_info) > 0:
        for song in plist_info:

            try:
                if 'pos' in song:
                    item_num = int(song['pos'])+1
                    item_num = str(item_num).ljust(col_width)
                if 'name' in song:
                    song_info = song['name']
                elif all(key in song for key in ['artist', 'album', 'title']):
                    song_info = "{} - {} - {}".format(
                            song['artist'],
                            song['album'],
                            song['title'])

            except Exception as e:
                sys.exit(e)

            begin = ''
            sep = '│ '
            end = '\033[0m'
            if song['id'] == get_id(client):
                begin = '\033[37;1m'

            sep_len = len(sep)
            name_len = len(song_info)
            total_len = col_width+sep_len+name_len
            if total_len > 80:
                trim_amt = total_len - 80
                song_info = song_info[:-trim_amt]

            print("{}{}{}{}{}".format(begin, item_num, sep, song_info, end))
    else:
        print('(playlist empty)')


def status(client):

    status = client.status()

    line1 = []
    if status:
        line1.append("{}".format(get_song(client)))

    line2 = []
    if 'state' in status:
        state = status['state']
        line2.append("[{}]  ".format(state))

    if 'song' in status:
        cur = str(int(status['song'])+1)
        total = status['playlistlength']
        line2.append("#{}/{}  ".format(cur, total))

    if 'elapsed' in status:
        elapsed = time_format(status['elapsed'])
        line2.append("{}/".format(elapsed))

    if 'duration' in status:
        duration = time_format(status['duration'])
        line2.append("{}  ".format(duration))

    line3 = []
    if 'volume' in status:
        volume = status['volume']
        line3.append("Volume: {}%  ".format(volume))

    if 'repeat' in status:
        if status['repeat'] == 1:
            repeat = "on"
        else:
            repeat = "off"
        line3.append("Repeat: {}  ".format(repeat))

    if 'random' in status:
        if status['random'] == 1:
            rand = "on"
        else:
            rand = "off"
        line3.append("Random: {}  ".format(rand))

    if 'single' in status:
        if status['single'] == 1:
            single = "on"
        else:
            single = "off"
        line3.append("Single: {}  ".format(single))

    if 'consume' in status:
        if status['consume'] == 1:
            consume = "on"
        else:
            consume = "off"
        line3.append("Consume: {}  ".format(consume))

    for line in (line1, line2, line3):
        print("".join(map(str, line)))


def list_playlists(client):

    plist_data = client.listplaylists()

    return plist_data


def get_id(client):

    try:
        return client.currentsong()['id']
    except Exception:
        pass


def get_song(client):

    try:
        song = client.currentsong()
        name = "{} - {}".format(song['artist'], song['title'])
    except Exception:
        name = "(not playing)"

    return name


def get_playid(client):

    current_url = client.currentsong()['file']
    url, playid = current_url.split('=')

    return playid
