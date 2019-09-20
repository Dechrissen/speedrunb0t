import socket
from Settings import HOST, PORT, PASS, IDENT, ADMIN


def openSocket():

    s = socket.socket()
    s.connect((HOST, PORT))
    s.send(("PASS " + PASS + "\r\n").encode())
    s.send(("NICK " + IDENT + "\r\n").encode())
    s.send(("JOIN #" + ADMIN + "\r\n").encode())
    return s

def sendMessage(s, CHANNEL, message):
    messageTemp = "PRIVMSG #" + CHANNEL + " :" + message
    s.send((messageTemp + "\r\n").encode())
    print("Sent: " + messageTemp)
