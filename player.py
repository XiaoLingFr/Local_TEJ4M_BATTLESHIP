import socket

HOST = None
PORT = None
CLIENT = None

RUNNING = True

def interpret(text):
    parse = text.split(" ")
    if parse[0] == "GM_END":
        RUNNING = False
    elif parse[0] == "PRNT":
        print(parse[0],end="")
    elif parse[0] == "IREP":
        CLIENT.sendall((input(">> ")).encode())
    elif parse[0] == "PRIREP":
        print(parse[1],end="")
        CLIENT.sendall((input(">>")).encode())
    return
def runtime():
    while running:
        text = CLIENT.recv(1024).decode()
        interpret(text)

    return


def player():
    print("Host IP: ",end="")
    HOST = input()

    valid_port = False
    while valid_port == False:
        try:
            print("Host PORT: ",end="")
            PORT = int(input())
            valid_port = True
        except:
            print("Try again...")

    CLIENT = socket.socket(socket.AF_NET, socket.SOCK_STREAM)
    CLIENT.connect((HOST, PORT))

    runtime()

    client.close()

    return