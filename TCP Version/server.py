import socket
import Decrypt
from collections import deque
import sys
import datetime

class Server:
  def __init__(self, host, port):
    self.host = host
    self.port = port
    self.server_socket = None
    self.privkey = None
    self.message_list = deque(maxlen=5)
    
  def set_host(self, host):
    self.host = host
  
  def set_port(self, port):
    self.port = port
    
  def set_key(self, path):
   self.privkey = Decrypt.read_private_key(path)
   
  def set_host_user(self):
    self.host = 'localhost' if len(sys.argv) < 2 else sys.argv[1]
    
  def set_port_user(self):
    self.port = 12345 if len(sys.argv) < 3 else int(sys.argv[2])
    
  def decrypt_file(self, file) :
    decrypted_file = Decrypt.decrypt(file, self.privkey)
    return decrypted_file

  def start(self):
    self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    self.server_socket.bind((self.host, self.port))
    self.server_socket.listen(1)
    print(f"Server listening on {self.host}:{self.port}")

    while True:
      #waiting for a connection
      print("Waiting for a connection...")
      client_socket, client_address = self.server_socket.accept()
      request_type = client_socket.recv(1024).decode() #get the kind of message being sent (only file for now)
      filename = client_socket.recv(1024).decode() #get the name of the file
      
      print(f"Connection from {client_address[0]}:{client_address[1]}, requesting {request_type} {filename}?")
      accept_response = input('y/n: ')
      filename = 'server_' + filename
      
      if accept_response == 'y' :
        client_socket.send(b'accepted')
        with open(filename, 'wb') as write_file :
          while True :
            chunk = client_socket.recv(1024)
            if not chunk:
              break
            
            decrypted_chunk = self.decrypt_file(chunk)
            write_file.write(decrypted_chunk)

if __name__ == "__main__":
    server = Server('localhost', 12345)
    server.set_host_user()
    server.set_port_user()
    server.set_key('Keys/server_key.pem')
    server.start()
