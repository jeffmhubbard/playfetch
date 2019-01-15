## PlayFetch
Fetch playlists from GMusicProxy  
  
#### Requirements
python-requests  
python-mpd
  
#### Usage
Fetch new station playlist:  
  `playfetch [-fcls] radio 'artist, title' --name 'station' --tracks <num> --exact`  
  
Fetch playlist of search results:  
  `playfetch [-fcls] search 'artist, title' --tracks <num> --album --exact`  
  
Fetch playlist of entire collection:  
  `playfetch [-fcls] collection --rating <rating> --shoff`  
  
Fetch I'm Feeling Lucky playlist:  
  `playfetch [-fcls] lucky --tracks <num>`  
  
Fetch all station playlists:  
  `playfetch [-f] stations`  
  
Fetch all user playlists:  
  `playfetch [-f] playlists`  
  
Fetch artist discography:  
  `playfetch [-f] discog 'artist' --exact`  
  
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
  
  
