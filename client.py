import socket
import threading
import random
import hill_cipher

nickname = input("Choose your nickname: ")

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect(('127.0.0.1', 55555))

my_pvt_key=random.randint(1,10)

prime_number=23
pri_root=9

encr_decr_key=0


X=(pri_root**my_pvt_key)%prime_number
X=str(X)

print(X)
Y=0

def receive():
    while True:
        try:
            message = client.recv(1024).decode('ascii')
            
            if message == 'NICK':
                client.send(nickname.encode('ascii'))
            elif message == 'key':
                client.send(X.encode('ascii'))


            elif message.startswith('key:'):
                Y=int(message[4:])
                print("my key :",X,"his key :",Y)
                key='keys:{}'.format(X)
                client.send(key.encode('ascii'))
                global encr_decr_key
                encr_decr_key=(Y**my_pvt_key)%prime_number
                print(encr_decr_key)


            elif message.startswith('keys:'):
                
                Y=int(message[5:])
                print("my key :",X,"his key :",Y)
                encr_decr_key=(Y**my_pvt_key)%prime_number
                print(encr_decr_key)


            else:
                name,text = message.split(":")
                message = name +text
                message=hill_cipher.DECRYPTION(message,encr_decr_key)
                print(message[:len(name)],": ",message[len(name):])
        except:
            print("An error occured!")
            client.close()
            break
        
        
def write():
    while True:
        message = '{}{}'.format(nickname, input(''))
        print(message)
        message=hill_cipher.ENCRYPTION(message,encr_decr_key)
        message = message[:len(nickname)] +":"+message[len(nickname):]
        client.send(message.encode('ascii'))
        

receive_thread = threading.Thread(target=receive)
receive_thread.start()

write_thread = threading.Thread(target=write)
write_thread.start()