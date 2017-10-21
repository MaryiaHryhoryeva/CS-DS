import socket
import sys
import serpent
import time
# Create a TCP/IP socket
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

server_address = ('localhost', 10000)
print >>sys.stderr, 'connecting to %s port %s' % server_address
sock.connect(server_address)

key = "12345678901234561234567890123457"
file = ""
iv = "1234567890123456"
serp = serpent.serpent_cbc(key, iv)
while True:
    request = raw_input('Enter request:\n')
    try:
        message = request
        print >>sys.stderr, 'sending "%s"' % message
        #if message == "rec_key":
        #message = message + ' ' + str(publicKey)
        sock.sendall(message)
        if message == "exit":
            sys.exit()
        if message[:7] != "gen_key" and message[:7] != "rec_key":
            while True:
                data = sock.recv(32)
                if data == "":
                    break
                print >>sys.stderr, 'received "%s"' % data
                if message[:7] == "get_key":
                    key = data
                    print >>sys.stderr, 'key is_"%s"' % key
                    serp = serpent.serpent_cbc(key, iv)
                    break
                elif message[:7] == "get_file":
                    file = data[8:]
                else:
                    file += data
        print >>sys.stderr, 'file info "%s"' % serp.decrypt(file)

    finally:
        print >>sys.stderr, 'ololo'

