import socket

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(("localhost", 9999))

server.listen()

client, addr = server.accept()

while True:
    message = client.recv(1024).decode('utf-8')
    if message == 'quit':
        break
    else:
        print(message)
    
server.close()
client.close()
