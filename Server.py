import socket
import threading

host = '127.0.0.1'
port = 55555

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((host, port))
server.listen()

clients = []
nicknames = []

def broadcast(message,self_client):
    message_server=message.decode('ascii')
    print(nicknames[clients.index(self_client)],"sent",message_server)
    for client in clients:
        if(client!=self_client):
            client.send(message)
        
def handle(client):
    while True:
        try:
            message = client.recv(1024)
            broadcast(message,client)
        except:
            index = clients.index(client)
            clients.remove(client)
            client.close()
            nickname = nicknames[index]
            broadcast('{} left!'.format(nickname,client).encode('ascii'))
            nicknames.remove(nickname)
            break
        
def receive():
    while True:
        client, address = server.accept()
        print("Connected with {}".format(str(address)))

        client.send('NICK'.encode('ascii'))
        nickname = client.recv(1024).decode('ascii')
        nicknames.append(nickname)
        clients.append(client)

        client.send('key'.encode('ascii'))
        key = client.recv(1024).decode('ascii')
        print("key =",key)
        broadcast("key:{}".format(key).encode('ascii'),client)



        thread = threading.Thread(target=handle,args=(client,))
        thread.start()
receive()