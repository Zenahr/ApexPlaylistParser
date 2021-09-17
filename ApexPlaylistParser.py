import os
import vdf
from pprint import pprint
# https://github.com/ValvePython/vdf
# https://developer.valvesoftware.com/wiki/KeyValues

# TODO: pass raw file data around instead of creating intermediate file on disk.

#   _   _ ____    _    ____ _____ 
#  | | | / ___|  / \  / ___| ____|
#  | | | \___ \ / _ \| |  _|  _|  
#  | |_| |___) / ___ \ |_| | |___ 
#   \___/|____/_/   \_\____|_____|
# 
# create instance
# apply instance.preprocess()
# get playlist data via instance.getPlaylists()
# apply instance.postprocess()

# or use QuickApexPlaylistParser() instead to get the playlists immediately


PARSER_FIX_TOKEN = '___SOME_RANDOM_TOKEN___'
INTERMEDIATE_FILE = 'intermediate.txt'

class ApexPlaylistParser:
        def __init__(self, filePath):
                self.__inputFile     = open(filePath, 'r')
                self.__inputFilePath = filePath

        def preprocess(self):
                """Since Apex does not use VDF strictly we need to replace any '#' we find with a random token so that the standard VDF parser doesn't break."""
                infile  = self.__inputFile
                outfile = open(INTERMEDIATE_FILE, 'w')
                data    = infile.read()
                data    = data.replace("#", PARSER_FIX_TOKEN)
                outfile.write(data)
                outfile.close()
                return data

        def parse(self):
                d = vdf.parse(open(INTERMEDIATE_FILE))
                return d

        def getPlaylists(self):
                """Parse out playlists.
                Output: dict(playlistLabel, playlistVariables, inherit)
                playlistLabel = playlist name
                playlistVariables = key/value pairs of playlist variables
                inherit = None or playlist label of parent playlist
                """
                try:
                        result = []
                        playlists = self.parse()['playlists']['Playlists']
                        for playlist in playlists:
                                print(playlist)
                                try:
                                        inherit = playlists[playlist]['inherit']
                                except KeyError:
                                        inherit = None # no other playlist has been inherited from yet.
                                result.append(dict(
                                        playlistLabel = playlist,
                                        playlistVariables = playlists[playlist]['vars'],
                                        inherit=inherit
                                ))
                        return result

                        return dict(
                                playlistLabels = playlists.keys()
                        )
                except KeyError:
                        print('something went wrong. Playlists could not be found.')

        def save(self, newData, destination=None):
                temp = vdf.parse(open(INTERMEDIATE_FILE))
                temp['playlists']['Playlists'] = newData
                if destination:
                        vdf.dump(temp, open(destination, 'w'))
                else:
                        vdf.dump(temp, open(self.__inputFilePath,'w'), pretty=True)

        def postprocess(self):
                """Revert changes made by preprocess() to revert parser hotfix."""
                with open(INTERMEDIATE_FILE, 'r') as infile, \
                     open(self.__inputFilePath, 'w') as outfile:
                    data = infile.read()
                    data = data.replace(PARSER_FIX_TOKEN, "#")
                    outfile.write(data)
                    outfile.close()
                os.remove(INTERMEDIATE_FILE)
                return data

class QuickApexPlaylistParser:
        """Quickly parse a playlist file and silently execute preprocess and cleanup operations."""
        def __new__(cls, filePath):
            parser = ApexPlaylistParser(filePath)
            parser.preprocess()
            playlists = parser.getPlaylists()
            parser.postprocess()
            return playlists

        def __init__(self, filePath):
                self.filePath = filePath
        
        # TODO: this dones't make much sense when called since QuickApexPlaylistParser ist just a list of playlists after intialization. use __init__ instead and modify save() API accordingly.
        def save(self, newData, destination=None):
                """If destination is not set, input file will be overwritten"""
                parser = ApexPlaylistParser(self.filePath)
                parser.preprocess()
                parser.save(newData, destination)
                parser.postprocess()
                return newData

if __name__ == '__main__':

        #   _   _ ____    _    ____ _____   _______  __    _    __  __ ____  _     _____ 
        #  | | | / ___|  / \  / ___| ____| | ____\ \/ /   / \  |  \/  |  _ \| |   | ____|
        #  | | | \___ \ / _ \| |  _|  _|   |  _|  \  /   / _ \ | |\/| | |_) | |   |  _|  
        #  | |_| |___) / ___ \ |_| | |___  | |___ /  \  / ___ \| |  | |  __/| |___| |___ 
        #   \___/|____/_/   \_\____|_____| |_____/_/\_\/_/   \_\_|  |_|_|   |_____|_____|

        oldPlaylists = QuickApexPlaylistParser('./test.txt')
        # add/remove/modify playlists here
        # then save the new data
        newPlaylists = oldPlaylists
        QuickApexPlaylistParser.save(newPlaylists, './test.txt')