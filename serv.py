import socket
import sys
import serpent
import time
import random
import string

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_address = ('localhost', 10000)
sock.bind(server_address)
sock.listen(1)

key = "12345678901234561234567890123457"
rsa_key = "rsa_key"
iv = "1234567890123456"
def getText(textName):
    data = open('./files/' + textName)
    return data.read()

def genKey():
    return ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(len(key)))

while True:
    connection, client_address = sock.accept()
    try:
        while True:
            data = connection.recv(16)
            print >>sys.stderr, 'received "%s"' % data
            if data:
                command = data[:8]
                info = data[8:]
                print >>sys.stderr, 'command ', command
                if command == "exit":
                    print >>sys.stderr, 'goodbye'
                    connection.close()
                    sys.exit()
                if command[:7] == "gen_key":
                    print >>sys.stderr, 'generating key'
                    key = genKey()
                elif command[:7] == "get_key":
                    print >>sys.stderr, 'sending key'
                    connection.sendall(key)
                elif command[:7] == "rec_key":
                    rsa_key = info
                elif command == "get_file":
                    print >>sys.stderr, 'sending data'
                    info = getText(info[1:])
                    serp = serpent.serpent_cbc(key, iv)
                    connection.sendall(serp.encrypt(info))
                    break
                else:
                    rsa_key += data
            else:
                break

    finally:
        connection.close()

