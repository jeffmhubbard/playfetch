## PlayFetch
Fetch playlists from GMusicProxy  
  
#### Requirements
python-requests  
python-mpd
  
#### Usage
Fetch playlist of search results:  
  `playfetch [-fcls] search 'artist, title' --tracks <num> --album --exact`  
  
Fetch new station playlist from search:  
  `playfetch [-fcls] radio 'artist, title' --name 'station' --tracks <num> --exact`  
  
Fetch new station playlist from current song:  
  `playfetch [-fcls] current --tracks <num>`  
  
Fetch Promoted Tracks playlist:  
  `playfetch [-fcls] promoted --shoff`  
  
Fetch I'm Feeling Lucky playlist:  
  `playfetch [-fcls] lucky --tracks <num>`  
  
Fetch an artist's Top Tracks playlist:  
  `playfetch [-fcls] top 'artist' --tracks <num>`  
  
Fetch an artist's complete discography:  
  `playfetch [-f] discog 'artist' --exact`  
  
Fetch user collection playlist:  
  `playfetch [-fcls] collection --rating <rating> --shoff`  
  
Fetch all user station playlists:  
  `playfetch [-f] stations`  
  
Fetch all user playlists:  
  `playfetch [-f] playlists`  
  
Rank current track:  
  `playfetch rank --up|--down`  
  
Print current MPD playlist:  
  `playfetch show --status`  
  
List playlists:  
  `playfetch list --all`  
  
Delete playlists:  
  `playfetch [-f] purge --[filter] --older <hours>`  
  
  
#### Options
*  -f or --force:   Do not prompt for overwrite or delete  
*  -c or --clear:   Clear current MPD playlist  
*  -l or --load:    Append to current MPD playlist  
*  -s or --start:   Start playing current MPD playlist  
*  -h or --help:    Print help
*  -d or --debug:   Print debug messages  


#### Configuration  
A configuration file can be placed at `~/.config/playfetch/config`  

> [playfetch]  
> proxy-url = http://localhost:9999  
> plist-dest = ~/.mpd/playlists  
> plist-prefix = play  
> mpd-host = localhost  
> mpd-port = 6600  
> auto-clear = False  
> auto-load = False  
> auto-start = False 
  
  
#### Tips
* Add `alias pf="playfetch"` to `.zshrc` or `.bashrc`   
* Add keybind for `playfetch -fcls lucky -t 100`  
  
  
