import socket
from os.path import isfile, isdir
import os
from mimetypes import guess_type
import re
import base64

TCP_IP = '127.0.0.1' #pętla lokalna
TCP_PORT1 = 5005 #port pod którym działa serwer
TCP_PORT2 = 5006
BUFFER_SIZE = 1024
SERVER_RESPONSE_HEADER = '<<PTPP END>>'  #końcowy nagłówek zgodnie z założeniami projektowymi
CONNECTION_LIST = []


def to_ascii(s):           #kodowanie jest niezbędne do niektórych operacji
    return s.encode('utf-8')


def to_unicode(s):
    return s

class Socket():
    def __init__(self, port, directory):
        self.port = port
        self.directory = directory

    def init_conn(self):      #inicjuje nasłuchiwanie na porcie
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.bind((TCP_IP, self.port))
        s.listen(10)
        CONNECTION_LIST.append(s)
        return s

    def listen_tcp(self):    #odbieranie połączenia
        P1 = self.init_conn()
        while 1:
            conn, addr = P1.accept()  # odebranie polaczenia
            try:
                data = conn.recv(1024).decode('utf-8')
                if not data: break
                response = self.serve_file(data)
                conn.sendall(response + to_ascii(SERVER_RESPONSE_HEADER))
                conn.close()
            except socket.error:
                print("Error Occured.")
                break

    def get_request(self, request):    #pobieranie nazwy pliku, który trzeba wysłać
        x = re.compile('GET(.*)PTPP/1.0')
        filepath = x.findall(request)
        filepath = str(filepath[0]).strip()
        return filepath

    def serve_file(self, request):  #serwowanie pliku lub dyrektorii
        filename = self.get_request(request)
        filepath = (self.directory + filename)
        if isfile(filepath):
            try:
                f = open(filepath, 'rb')
                content = to_unicode(f.read())
                content_type, _ = guess_type(filepath)
                return content
            except IOError as e:
                return 'File "%s" is not readable' % filepath
        elif isdir(filepath):
            files_list = []
            for path, subdirs, files in os.walk(filepath):
                for name in files:
                    files_list.append(name)
            files_list = " ".join(files_list)
            files_list = to_ascii(files_list)
            return files_list
        else:
            return (to_ascii('File or directory "%s" does not exist' % filename))


if __name__ == "__main__":
    (Socket(TCP_PORT1, '../../serwer/')).listen_tcp()

