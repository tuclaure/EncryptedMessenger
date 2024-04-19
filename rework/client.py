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
    
  #reads in decryption key
  def set_key(self, path) :
    self.pubkey = Encrypt.read_public_key(path)
    
  #sets the server ip
  def set_host(self, host) :
    self.host = host
  
  #sets the server port
  def set_port(self, port) :
    self.port = port
  
  #sets the ip from user takes cmd line input, if none prompts in terminal
  def set_host_user(self) :
    self.host = input("Server IP: ") if len(sys.argv) < 2 else sys.argv[1]
  
  #sets port from user takes cmd line input, if none prompts in terminal
  def set_port_user(self):
    self.port = int(input('Server Port: ')) if len(sys.argv) < 3 else int(sys.argv[2])
  
  #sets filename from user takes cmd line input, if none prompts in terminal
  def get_filename_user(self):
    filename = input('Filename: ') if len(sys.argv) < 4 else sys.argv[3]
    return filename
  
  #reads in the file
  def read_file(self, file_path):
    with open(file_path, 'rb') as file:
      information = file.read()
    return information
  
  #encrypts file
  def encode_file(self, file):
    encoded_message = Encrypt.encrypt(file, self.pubkey)
    return encoded_message
  
  #deliniates the file into chunks
  def make_chunks(self, file) :
    return [file[i:i + self.chunk_size] for i in range(0, len(file), self.chunk_size)]
  
  #returns the type of request, the name of the file and the size of the file, encoded into bytes
  def file_information(self, file, filename):
    type = 'filetransfer'
    filesize = len(file)
    information = (f"{type} {filename} {filesize}").encode()
    return information

  #connect to a server
  def establish_connection(self):
    # binding interface for fabric
    interface_name = 'enp7s0'
    interface_index = socket.if_nametoindex(interface_name)
    self.client_socket = socket.socket(socket.AF_INET6, socket.SOCK_STREAM)
    self.client_socket.connect((self.host, self.port, 0, interface_index))
    
  #sends a request to the server with the information packet
  def send_request(self, information):
    self.client_socket.send(information)
    split_information = information.split()
    print(f"requesting permission to {split_information[0].decode()} {split_information[1].decode()} to {self.host}:{self.port}...")
    response = self.client_socket.recv(1024) #gets response
    
    if response == b'accepted' : #file transfer accepted
      print('Server accepted file, transfering...') #update user
      return True #return true
    else :
      print('Server rejected file, closing connection') #file transfer denied
      self.client_socket.close() #close connection
      return False #return false
  
  #send the file
  def send_file(self, file):
    file_chunks = self.make_chunks(file) #create chunks from the file
    for chunk in file_chunks : #iterate through
      self.client_socket.send(chunk) #send 
    self.client_socket.close() #close connection
  
  #comprehensive method to perform a file transfer
  def send_package(self):
    filename = self.get_filename_user() #gets the name of the file
    file = self.read_file(filename) #reads in a file
    # encoded_file = self.encode_file(file) #encrypts it (currently disabled)
    encoded_file = file
    information = self.file_information(file, filename) #creates an information packet to send as the initial request
    self.establish_connection() #connects to server
    response = self.send_request(information) #sends the request, recieves a true or false response
    if response : #transfer accepted
      self.send_file(encoded_file) #send the user the file
      print("file sent") #update user
        
if __name__ == "__main__":
  client = Client('localhost', 12345) #declare instance
  client.set_host_user() #update ip
  client.set_port_user() #update port
  client.set_key('Keys/client_key.pem') #get key
  client.send_package() #perform comprehensive file transfer
