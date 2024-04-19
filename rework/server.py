import socket
import Decrypt
from collections import deque
import sys

class Server:
  def __init__(self, host, port):
    self.host = host
    self.port = port
    self.server_socket = None
    self.privkey = None
    self.message_list = deque(maxlen=5)
  
  #setter method for host ip
  def set_host(self, host):
    self.host = host
  
  #set host port
  def set_port(self, port):
    self.port = port
    
  #read in key using the decrypt method
  def set_key(self, path):
   self.privkey = Decrypt.read_private_key(path)
   
  #set ip from a user
  def set_host_user(self):
    self.host = input('Host IP: ') if len(sys.argv) < 2 else sys.argv[1]
    
  #set port from a user
  def set_port_user(self):
    self.port = int(input("Host Port: ")) if len(sys.argv) < 3 else int(sys.argv[2])
  
  #decrypt an encrypted file using the Decrypt classes internal method
  #currently set to return the original file as 96Mb test file takes 800,000 loops with current style
  def decrypt_file(self, file) :
    # decrypted_file = Decrypt.decrypt(file, self.privkey)
    # return decrypted_file
    return file

  #handles server running and events
  def start(self):
    #declare a TCP style socket
    self.server_socket = socket.socket(socket.AF_INET6, socket.SOCK_STREAM)
    # binding an interface for fabric
    interface_name = 'enp7s0'
    interface_index = socket.if_nametoindex(interface_name)
    self.server_socket.bind((self.host, self.port, 0, interface_index))
    
    #begin listening on socket
    self.server_socket.listen(1)
    print(f"Server listening on {self.host}:{self.port}")

    while True:
      #waitfor a connection
      print("Waiting for a connection...")
      client_socket, client_address = self.server_socket.accept()
      
      #first reception is a file request with a data packet
      request = client_socket.recv(1024).decode()
      information = request.split() #split the data packet into its components
      
      #print out client information and ask for permission to accept request
      print(f"Connection from {client_address[0]}:{client_address[1]}, requesting {information[0]} of {information[1]} size {information[2]} bytes")
      accept_response = input('Accept this file (y/n): ') #get user response
      filename = 'server_' + information[1] #from information packet add server_ to filename
      
      if accept_response == 'y' : #request accepted
        client_socket.send(b'accepted') #send a positive response to client
        with open(filename, 'wb') as write_file : #open a file
          while True : #loop through chunks being sent
            chunk = client_socket.recv(1024) #recieve chunk
            if not chunk:
              break
            
            decrypted_chunk = self.decrypt_file(chunk) #decrypt chunk
            write_file.write(decrypted_chunk) #write to file
      else :
        client_socket.send(b'denied') #response rejected

if __name__ == "__main__":
    server = Server('localhost', 12345) #declare an instance
    server.set_host_user() #user sets ip
    server.set_port_user() #user sets port
    server.set_key('Keys/server_key.pem') #gets key
    server.start() #starts server
