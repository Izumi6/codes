# TCP (lan) based chatting app

# --------------------------------------------------------------
#                          client.py
# --------------------------------------------------------------

# req. libs
import socket
import threading


# global
## connection data
host = '127.0.0.1' # server ip
port = 4444        # free/open port
print(f"[#] connecting to {host}:{port}")

## nickname
nickname = input("[+] enter nickname:")

## starting client
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect((host, port))
print(f"[+] connected to {host}:{port}")


# listening to server & sending nickname
def receive():
    while True:
        try:
            # receive msg
            msg = client.recv(1024).decode('ascii')

            # print msg
            if msg == 'NICKNAME':
                client.send(nickname.encode('ascii'))
            else:
                print(msg)
        except:
            print("[!] error 404\n[#] terminating...")
            client.close()
            break

# send msg to server
def write():
    while True:
        msg = f"{nickname}: {input('')}"
        client.send(msg.encode('ascii'))


# starting threads for listening & writing
receive_thread = threading.Thread(target=receive)
receive_thread.start()

write_thread = threading.Thread(target=write)
write_thread.start()
