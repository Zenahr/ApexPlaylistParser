import os
import vdf
# https://github.com/ValvePython/vdf
# https://developer.valvesoftware.com/wiki/KeyValues

def preprocess():
    with open(r'test.txt', 'r') as infile, \
         open(r'test-intermediate.txt', 'w') as outfile:
        data = infile.read()
        data = data.replace("#", "___SOME_RANDOM_TOKEN___")
        outfile.write(data)
        return data

def postprocess():
    with open(r'test-intermediate.txt', 'r') as infile, \
         open(r'test.txt', 'w') as outfile:
        data = infile.read()
        data = data.replace("___SOME_RANDOM_TOKEN___", "#")
        outfile.write(data)
        outfile.close()
    os.remove('test-intermediate.txt')
    return data

def parse():
        d = vdf.parse(open('test-intermediate.txt'))
        return d

def write(newData):
        vdf.dump(newData, open('test.txt','w'), pretty=True)

if __name__ == '__main__':
    preprocess()
    parse()
    postprocess()