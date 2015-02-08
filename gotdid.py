
import sys
import json
import os

gotdidData =  { 'counter':0, 'dids':[] }

def makeEntry(status,desc):
    global gotdidData
    gotdidData['counter'] = gotdidData['counter'] + 1
    did = { 'status':status, 'id':gotdidData['counter'], 'desc' : desc }
    return did

def findFile():
    filename = os.path.abspath(os.path.join(os.getcwd(), '.gotdid'))
    while not (os.path.isfile(filename)):
        folder = os.path.dirname(filename)
        parent, child = os.path.split(folder)
        next = os.path.join(parent, '.gotdid')
        if next == filename:
            break
        filename = next
    return filename

def readFile(filename):
    print 'reading file %s' % filename
    if not (os.path.isfile(filename)):
        print "can't find .gotdid file"
        return False
    with open(filename, 'r') as infile:
        global gotdidData
        gotdidData = json.load(infile)
    return True

def writeFile(filename):
    with open(filename, 'w') as outfile:
        json.dump(gotdidData, outfile, indent=4, separators=(',',': '))
 
def initCommand(options):
    print 'init'
    filename = os.path.abspath(os.path.join(os.getcwd(), '.gotdid'))
    if(os.path.isfile(filename)):
        print 'the file %s is already there' % filename
        return False
    print 'making %s' % filename
    global gotdidData 
    gotdidData = { 'counter':0, 'dids':[] }
    writeFile(filename)
    return True

def doCommand(options):
    print 'do'
    if len(options) != 1:
        print 'error - do requires an option with the do text'
        return False
    filename = findFile()
    if readFile(filename):
        gotdidData['dids'].append(makeEntry('do',options[0]))
        writeFile(filename)
    return True

def winCommand(options):
    print 'win'
    if len(options) != 1:
        print 'error - win requires an option with the win text'
        return False
    filename = findFile()
    if readFile(filename):
        gotdidData['dids'].append(makeEntry('win',options[0]))
        writeFile(filename)
    return True

def didCommand(options):
    print 'did'
    if len(options) != 1:
        print 'error - did requires the id of the do you want to did'
        return False
    filename = findFile()
    if readFile(filename):
        i = int(options[0])
        print '%d is getting did' % i
        #global gotdidData
        for d in gotdidData['dids']:
            if i == d['id'] and d['status'] == 'do':
                d['status'] = 'did'
                writeFile(filename)
                return True
        print "can't did %d - id not found" % i
    return False

def undidCommand(options):
    print 'undid'
    if len(options) != 1:
        print 'error - undid requires the id of the do you want to did'
        return False
    filename = findFile()
    if readFile(filename):
        i = int(options[0])
        print '%d is getting undid' % i
        for d in gotdidData['dids']:
            if i == d['id'] and d['status'] == 'did':
                d['status'] = 'do'
                writeFile(filename)
                return True
        print "can't undid %d - id not found" % i
    return False

def gtfoCommand(options):
    print 'gtfo'
    if len(options) != 1:
        print 'error - gtfo requires the id of the do you want to delete'
        return False
    filename = findFile()
    if readFile(filename):
        i = int(options[0])
        print '%d is getting tfo' % i
        for d in gotdidData['dids']:
            if i == d['id']:
                gotdidData['dids'].remove(d)
                writeFile(filename)
                return True
        print "can't gtfo %d - id not found" % i
    return False

def printEntry(entry):
    print '%d %s %s' % (entry['id'], entry['status'], entry['desc'])

def wutCommand(options):
    print 'wut'
    filename = findFile()
    if readFile(filename):
        filter = ""

        # See what the options are
        if len(options) == 1:
            filter = options[0]

        # Show do elements first
        if filter == 'do' or filter == '':
             for d in gotdidData['dids']:
                if d['status'] == 'do':
                    printEntry(d)
        
        # Show dids
        if filter == 'did' or filter == '':
            for d in gotdidData['dids']:
                if d['status'] == 'did':
                    printEntry(d)        
        
        # Show wins
        if filter == 'win' or filter == '':
            for d in gotdidData['dids']:
                if d['status'] == 'win':
                    printEntry(d)
    return True

def mergeCommand(options):
    print 'merge'
    if len(options) != 2:
        print 'error - merge needs a source and destination file args'
        return False

    source = options[0]
    if not readFile(source):
        print "error - can't find source file %s" % source
        return False
    sourceData = gotdidData;

    destination = options[1]
    if not readFile(destination):
        print "error - can't find destination file %s" % destination
        return False
    destData = gotdidData;

    if len(sourceData['dids']) > 0:
        for d in sourceData['dids']:
            destData['counter'] = destData['counter'] + 1
            did = { 'id':destData['counter'], 'status':d['status'], 'desc':d['desc'] }
            destData['dids'].append(did)
        writeFile(filename)
    return True


def usage():
    us = '\ngotdid command options\n' \
         'init    - make a .gotdid file in the current directory\n' \
         'do      - add something that needs to get did\n' \
         '            gotdid do "The stuff to do"\n' \
         'did     - mark a todo did using the id from wut\n' \
         '            gotdid did <id>\n' \
         'win     - add something that you just did without knowin it needed did\n' \
         '            gotdid win "fixed the make file that was broken forever"\n' \
         'undid   - mark a todo back to do using the id from wut\n' \
         '            gotdid undid <id>\n' \
         'gtfo    - delete an item from the list using the id from wut\n' \
         '            gotdid gtfo <id>\n' \
         'wut     - see the what needs to get did and what got did \n' \
         '            gotdid wut will show everything\n' \
         '            gotdid wut [do|did] will filter\n' \
         'merge   - moves the do/did entries from one .gotdid file to another\n' \
         '          the id values from the source enthries are \n' \
         '          overwritten in the destination with new id values\n' \
         '\n' \
         'Except for init and merge, all commands look in the current directory\n' \
         'before looking up the tree for the first .gotdid found\n' \
         '\n'
    return us

def main():
    if len(sys.argv) < 2:
        print usage()
    else:
        command = sys.argv[1]
        opts = sys.argv[2:]
        if command == 'init':
            if not initCommand(opts):
                print usage()
        elif command == 'do':
            if not doCommand(opts):
                print usage()
        elif command == 'win':
            if not winCommand(opts):
                print usage()
        elif command == 'did':
            if not didCommand(opts):
                print usage()
        elif command == 'wut':
            if not wutCommand(opts):
                print usage()
        elif command == 'undid':
            if not undidCommand(opts):
               print usage()
        elif command == 'gtfo':
            if not gtfoCommand(opts):
               print usage()
        else:
            print usage()   

if __name__ == '__main__':
    main()


