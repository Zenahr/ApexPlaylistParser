import os
import vdf
# https://github.com/ValvePython/vdf
# https://developer.valvesoftware.com/wiki/KeyValues

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
                try:
                        return vdf.parse(open(INTERMEDIATE_FILE))['playlists']['Playlists']
                except KeyError:
                        print('something went wrong. Playlists could not be found.')

        def save(self, newData):
                vdf.dump(newData, open(self.__inputFilePath,'w'), pretty=True)

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


if __name__ == '__main__':
        p = ApexPlaylistParser('./test.txt')
        p.preprocess()
        playlists = p.getPlaylists()
        print(playlists)
        # p.postprocess()