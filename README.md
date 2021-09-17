# Apex Legends Playlist file parser

## Installation

1. pip install vdf
2. Paste `ApexPlaylistParser.py` into your codebase
3.

## Import

```py
from ApexPlaylistParser import ApexPlaylistParser, QuickApexPlaylistParser
```

## Usage

```py
from ApexPlaylistParser import QuickApexPlaylistParser

playlists = QuickApexPlaylistParser('./test.txt')
for playlist in playlists:
    print(playlist['playlistLabel])
    print(playlist['playlistVariables])
    print(playlist['inherit])
```

The `QuickApexPlaylistParser` class is limited and should only be used to read files, not update them.

For more advanced operations use the `ApexPlaylistParser` class instead:

```py
from ApexPlaylistParser import ApexPlaylistParser

    parser = ApexPlaylistParser('./test.txt')
    parser.preprocess()
    playlists = parser.getPlaylists()
    print(playlists[0]['playlistVariables']['max_players']) # print max_players value from first playlist found.
    
    # add/remove/modify playlists
    playlists[0]['playlistVariables']['max_players'] = 10 
    
    # save changes
    parser.save(newData, destination) # destination is optional. If not provided, the file will be overwritten.
    
    # clean up. Do not omit.
    parser.postprocess()
```

> Note that the return value of ApexPlaylistParser.getPlaylists() is a regular Python dictionary.

## Additional Notes

Apex Legends is built on the Source engine and uses a slight variation of Valve's KeyValue format (VDF) to store information. Hence why we need a special parser for this.
