Server and Client File Transfer

Purpose
The server and client file transfer program pair facilitates the transfer of files between a host server and client over a TCP connection. It allows users to specify the server's IP address and port for hosting, and clients can connect to the server using the same IP:Port pair.

Features
Host a server for file transfer.
Connect clients to the server for sending files.
Server prompts for user permission before accepting files from clients.
Users can specify IP and port via command line arguments or be prompted for input.
Simple command-line interface for both server and client.

Installation
Clone the repository: git clone https://github.com/your_repository.git
Navigate to the project directory.
Ensure you have Python 3 installed.
Install dependencies: pip install -r requirements.txt

Usage
Server
python3 server.py IP PORT
If no command-line arguments are provided, the program will prompt for user input.

Client
python3 client.py IP PORT FILENAME
If no command-line arguments are provided, the program will prompt for user input.

File Transfer Protocol
The program pair uses TCP (Transmission Control Protocol) for file transfer.

Security
Option to enable RSA encryption for file transfer (currently disabled due to long encryption times for large files).
Minimal to no other security protections implemented; users are expected to use the program responsibly.

Performance
Large file encryption can significantly increase transfer time.

Verification
this program was tested with a variety of file types and extensions
file size was tested from empty to 96Mb transfer size
program was simmulated in a fabric environment to test network connectivity
