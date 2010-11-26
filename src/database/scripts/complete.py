#!/usr/bin/python
import sys
from getopt import getopt, GetoptError

from createdatabase import CreateDatabase

def usage():
    print('''Usage: complete.py <options>
    
options:

-n (--databaseName) -> required
-m (--scriptManifestPath) -> required
-s (--scriptDirectory) -> required
-d (--dropExisting)
''')

def main(commandLineArgs):
    try:
        rawOpts, args = getopt(
            commandLineArgs,
            'n:m:s:d',
            ['databaseName=', 'scriptManifestPath=', 'scriptDirectory=', 'dropExisting'])
        
    except GetoptError, msg:
        print(str(msg))
        usage()
        sys.exit(2)
    
    opts = {}
    for i in rawOpts:
        opts[i[0]] = i[1]
        
    def get_opt(short, long, required=False):
        if short in opts:
            return opts[short]
        elif long in opts:
            return opts[long]
        elif required is True:
            print('Option missing: {0} (or {1})\n'.format(short, long))
            usage()
            sys.exit()
        else:
            return None
    
    databaseName = get_opt('-n', '--databaseName', True)
    manifestPath = get_opt('-m', '--scriptManifestPath', True)
    scriptDirectory = get_opt('-s', '--scriptDirectory', True)
    
    drop = True if '-d' in opts or '--dropExisting' in opts else False
    
    c = CreateDatabase(
        databaseName,
        manifestPath,
        scriptDirectory,
        drop)
    
    c.go()

if __name__ == '__main__':
    main(sys.argv[1:])
    