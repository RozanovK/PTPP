import socket
from os.path import isfile
from mimetypes import guess_type
import re
import base64

TCP_IP = '127.0.0.1'
TCP_PORT1 = 5005
TCP_PORT2 = 5006
BUFFER_SIZE = 1024
SERVER_RESPONSE_HEADER = '<<PTPP END>>'
CONNECTION_LIST = []


def to_ascii(s):
    return s.encode('utf-8')


def to_unicode(s):
    return s

class Socket():
    def __init__(self, port):
        self.port = port

    def init_conn(self):
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.bind((TCP_IP, self.port))
        s.listen(10)
        CONNECTION_LIST.append(s)
        return s

    def listen_tcp(self):
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


    def get_request_p1(self, request):
        x = re.compile('GET(.*)PTPP/1.0')
        filepath = x.findall(request)
        filepath = str(filepath[0]).strip()
        return filepath

    def serve_file(self, request):
        filepath = self.get_request_p1(request)
        if not isfile(filepath):
            return 'File "%s" does not exist' % filepath
        try:
            f = open(filepath, 'rb')
        except IOError as e:
            return 'File "%s" is not readable' % filepath
        content = to_unicode(f.read())
        content_type, _ = guess_type(filepath)
        return content


if __name__ == "__main__":
    (Socket(TCP_PORT2)).listen_tcp()

