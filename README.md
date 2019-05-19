## PlayFetch
Fetch playlists from GMusicProxy  
  
#### Requirements
python-requests  
python-mpd
prompt_toolkit
  
#### Usage
Fetch playlist of search results:  
  `playfetch search 'artist, title' --tracks <num> --album --exact`  
  
Fetch new station playlist from search:  
  `playfetch radio 'artist, title' --name 'station' --tracks <num> --exact`  
  
Fetch new station playlist from current song:  
  `playfetch current --tracks <num>`  
  
Fetch Promoted Tracks (Thumbs Up) playlist:  
  `playfetch promoted --shoff`  
  
Fetch I'm Feeling Lucky playlist:  
  `playfetch lucky --tracks <num>`  
  
Fetch Listen Now playlists:  
  `playfetch listen --artist|--album|--situation|--all`  
  
Fetch an artist's Top Tracks playlist:  
  `playfetch toptracks 'artist' --tracks <num>`  
  
Fetch an artist's complete discography:  
  `playfetch discog 'artist' --exact`  
  
Fetch user collection playlist:  
  `playfetch collection --rating <rating> --shoff`  
  
Fetch all user station playlists:  
  `playfetch stations`  
  
Fetch all user playlists:  
  `playfetch playlists`  
  
Rate current track:  
  `playfetch rate --up|--down`  
  
Print current MPD playlist:  
  `playfetch show --status`  
  
List playlists:  
  `playfetch list --all`  
  
Delete playlists:  
  `playfetch purge --[filter] --older <hours>`  
  
Start interactive shell:  
  `playfetch shell`  
  
  
#### Options
*  -F or --force:   Do not prompt for overwrite or delete  
*  -C or --clear:   Clear current MPD playlist  
*  -L or --load:    Append to current MPD playlist  
*  -S or --start:   Start playing current MPD playlist  
*  -A or --auto:    Clear, load, and start MPD playlist
  
  
#### Configuration  
A configuration file can be placed at `~/.config/playfetch/config`  

> [playfetch]  
> proxy-url = http://localhost:9999  
> plist-dest = ~/.mpd/playlists  
> plist-prefix = play  
> mpd-host = localhost  
> mpd-port = 6600  
  
  
#### Tips
* Add `alias pf="playfetch"` to `.zshrc` or `.bashrc`   
* Add keybind for `playfetch lucky -t 100 -FA`  
  
  
