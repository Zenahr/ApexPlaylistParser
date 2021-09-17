from ApexPlaylistParser import QuickApexPlaylistParser

playlists = QuickApexPlaylistParser('test.txt')
print(playlists[0]['playlistVariables']['max_players'])
playlists[0]['playlistVariables']['max_players'] = 10

QuickApexPlaylistParser('test2.txt').save(playlists, 'test_new.txt')