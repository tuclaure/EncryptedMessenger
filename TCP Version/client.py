import socket
import sys
import Encrypt
import os

class Client:
  def __init__(self, host, port):
    self.host = host
    self.port = port
    self.client_socket = None
    self.pubkey = None
    self.chunk_size = 1024
    
  def set_key(self, path) :
    self.pubkey = Encrypt.read_public_key(path)
    
  def set_host(self, host) :
    self.host = host
  
  def set_port(self, port) :
    self.port = port
  
  def set_name(self, name):
    self.name = name

  def set_host_user(self) :
    self.host = 'localhost' if len(sys.argv) < 2 else sys.argv[1]
    
  def set_port_user(self):
    self.port = 12345 if len(sys.argv) < 3 else int(sys.argv[2])
  
  def get_filename_user(self):
    filename = 'cat.jpg' if len(sys.argv) < 4 else sys.argv[3]
    return filename

  def read_file(self, file_path):
    with open(file_path, 'rb') as file:
      information = file.read()
    return information
    
  def encode_file(self, file):
    encoded_message = Encrypt.encrypt(file, self.pubkey)
    return encoded_message
  
  def make_chunks(self, file) :
    return [file[i:i + self.chunk_size] for i in range(0, len(file), self.chunk_size)]


  def establish_connection(self):
    self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    self.client_socket.connect((self.host, self.port))
    print('1')
    
  def send_request(self, filename):
    print(2)
    self.client_socket.send(b'filetransfer')
    self.client_socket.send(filename.encode())
    response = self.client_socket.recv(1024)
    print(3)
    if response == b'accepted' :
      print('Server accepted file, transfering...')
      return True
    else :
      print('Server rejected file, closing connection')
      self.client_socket.close()
      return False
      
  def send_file(self, file):
    print(4)
    file_chunks = self.make_chunks(file)
    for chunk in file_chunks :
      self.client_socket.send(chunk)
    
    print(5)
    print(6)
    self.client_socket.close()
    return status
        
if __name__ == "__main__":
  client = Client('localhost', 12345)
  client.set_host_user()
  client.set_port_user()
  client.set_key('Keys/client_key.pem')
  filename = client.get_filename_user()
  file = client.read_file(filename)
  encoded_file = client.encode_file(file)
  
  client.establish_connection()
  response = client.send_request(filename)
  if response :
    status = client.send_file(encoded_file)
    print(status)
  else :
    print('Transfer Failed')
