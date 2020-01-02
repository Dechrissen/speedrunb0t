import string
from Socket import sendMessage
from Settings import ADMIN


def joinRoom(s):
    readbuffer = ""
    Loading = True
    while Loading:
        readbuffer = s.recv(1024)
        readbuffer = readbuffer.decode()
        temp = readbuffer.split("\n")
        readbuffer = readbuffer.encode()
        readbuffer = temp.pop()
        for line in temp:
            print(line)
            Loading = loadingComplete(line)
    sendMessage(s, ADMIN, "/me has reconnected.")

def loadingComplete(line):
    if("End of /NAMES list" in line):
        return False
    else:
        return True
