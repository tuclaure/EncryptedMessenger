from os import path as os_path
from os import makedirs as mkdirs
from base64 import b64decode
from base64 import b64encode
from sys import argv as sys_argv

def read_plain_text(path):
  """Reads in file to a byte string
  
  Arguments: (path)
    path: file location to read from
    
  Output:
    file_bytes: byte string of the file"""
  try :
    with open(path, 'rb') as file: #read in the file as binary
      file_bytes = file.read()
  except Exception as e:
    print(f"{e}")
    new_path = input("New Path: ")
    read_plain_text(new_path)
  return file_bytes
  
def read_public_key(path):
  """Reads in a public key into a tupple
  
  Arguments (path)
    path: file location for public key
  
  Output (decoded_n, decoded_e)
    decoded_n: key modulus integer
    decoded_e key exponent integer"""
    
  try:
    read_numbers = [] #list to store n and e strings
    with open(path, 'r') as pem_file: #reading standard text
      for line in pem_file: #iterate through file
        line = line.strip() #strip 
        if line and line != "-----BEGIN PUBLIC KEY-----" and line != "-----END PUBLIC KEY-----": #look for header and footer
          read_numbers.append(b64decode(line)) #decode the base 64 string
          
    # Decode bytes back to integers
    decoded_n = int.from_bytes(read_numbers[0], byteorder='big')
    decoded_e = int.from_bytes(read_numbers[1], byteorder='big')
    
  except Exception as e:
    print(f"{e}")
    new_path = input("Public Key Path: ")
    decoded_n, decoded_e = read_public_key(new_path)
    
  return (decoded_n, decoded_e)

def write_cipher_text(cipher, write_location):
  """Writes out in binary the ciphered text to write location as cipher.enc
  
  Arguments: (cipher, write_location)
    cipher: ciphered byte string
    write_location: directory to write to"""
    
  #create folder if it doesnt exist
  if not os_path.exists(write_location) :
    mkdirs(write_location)
    
  with open(write_location + '/cipher.enc', 'wb') as file: #writes to cipher.enc always in binary
    file.write(cipher)
  
def encrypt(message, public_key):
  """ Encrypts a message using a public_key
  
  Arguments:
    message: byte string
    public_key: tupple holding (n, e)
  
  Output:
    cipher_text: byte string containing the ciphered message"""

  #Encodes a message to base64 to handle strange bytes
  #turns messages into key size manipulable chunks
  #Encrypts message chunks using C = M^e mod n
  #returns all C chunks as a byte string
  
  n, e = public_key #get key numbers
  chunk_size = n.bit_length() // 8  # Calculate the maximum chunk size based on the modulus size
  cipher_text = b"" #byte string
  message_base64 = b64encode(message) #encode the message as base64 to handle null bytes
  
  for i in range(0, len(message_base64), chunk_size): #loop through the message in chunks
    plain_chunk = message_base64[i:i + chunk_size] #get chunk of message
    plain_int = int.from_bytes(plain_chunk, 'big') #convert chunk to an integer
    cipher_int = pow(plain_int, e, n) #perform m^e mod n on chunk
    cipher_chunk = cipher_int.to_bytes(chunk_size, 'big') #convert chunk to bytes
    cipher_text += cipher_chunk #append bytes chunk to final byte string
  return cipher_text

def run_encrypt():
  """Executes the encryption program using internal functions"""
  
  #gets text to encrypt and public key from cmd line call or user
  if len(sys_argv) > 1: #if commamnd line is used No Protections
    text_path = sys_argv[1] #expects a file
    key_path = 'Keys/public_key.pem' if len(sys_argv) < 3 else sys_argv[2] #key file, no input defaults 
    write_location = 'Output' if len(sys_argv) < 4 else sys_argv[3] #write location, in input default
      
    plain_text = read_plain_text(text_path) #get text as binary
    key = read_public_key(key_path) #get key as tupple of (n,e)
    cipher = encrypt(plain_text, key) #encrypt message, return the ciphered byte string
    write_cipher_text(cipher, write_location) #write the byte string

if __name__ == "__main__":
  run_encrypt()