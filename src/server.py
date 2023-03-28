import socket

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(("localhost", 9999))

server.listen()

client, addr = server.accept()

done = False

while not done:
    message = client.recv(1024).decode('utf-8')
    if message == 'quit':
        done = True
    else:
        print(message)
    client.send(input("Message: ").encode('utf-8'))
    
server.close()
client.close()
