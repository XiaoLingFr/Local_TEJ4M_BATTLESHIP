import random
import socket

ZHAO_LANG_SYNTAX = {
    "PRINT": "PRNT",
    "IMMEDIATE REPLY": "IREP",
    "PRINT WITH REPLY": "PRIREP",
    "GAME END" : "GM_END"
}

conn = None
addr = None
SERVER = None

SIZE = 10
SHIP = ["carrier", "battleship", "cruiser","submarine","destroyer"]
SHIP_DATA = {
    "carrier": 5,
    "battleship": 4,
    "cruiser": 3,
    "submarine": 3,
    "destroyer": 2
}
SHIP_REPRESENTATION = {
    "carrier": 'C',
    "battleship": 'B',
    "cruiser": 'Q',
    "submarine": 'S',
    "destroyer": 'D'
}
UNKNOWN = '~'
HIT = 'X'
MISS = 'O'

VERTICAL = "V"
HORIZONTAL = "H"

ORIENTATIONS = [VERTICAL,HORIZONTAL]

board_header = "X A B C D E F G H I J"
board_header_to_column = {
    "A" : 0,
    "B" : 1,
    "C" : 2,
    "D" : 3,
    "E" : 4,
    "F" : 5,
    "G" : 6,
    "H" : 7,
    "I" : 8,
    "J" : 9
}

player_board = [
    ['~','~','~','~','~','~','~','~','~','~'],
    ['~','~','~','~','~','~','~','~','~','~'],
    ['~','~','~','~','~','~','~','~','~','~'],
    ['~','~','~','~','~','~','~','~','~','~'],
    ['~','~','~','~','~','~','~','~','~','~'],
    ['~','~','~','~','~','~','~','~','~','~'],
    ['~','~','~','~','~','~','~','~','~','~'],
    ['~','~','~','~','~','~','~','~','~','~'],
    ['~','~','~','~','~','~','~','~','~','~'],
    ['~','~','~','~','~','~','~','~','~','~']
]

player_guess = [
    ['~','~','~','~','~','~','~','~','~','~'],
    ['~','~','~','~','~','~','~','~','~','~'],
    ['~','~','~','~','~','~','~','~','~','~'],
    ['~','~','~','~','~','~','~','~','~','~'],
    ['~','~','~','~','~','~','~','~','~','~'],
    ['~','~','~','~','~','~','~','~','~','~'],
    ['~','~','~','~','~','~','~','~','~','~'],
    ['~','~','~','~','~','~','~','~','~','~'],
    ['~','~','~','~','~','~','~','~','~','~'],
    ['~','~','~','~','~','~','~','~','~','~']
]

server_board = [
    ['~','~','~','~','~','~','~','~','~','~'],
    ['~','~','~','~','~','~','~','~','~','~'],
    ['~','~','~','~','~','~','~','~','~','~'],
    ['~','~','~','~','~','~','~','~','~','~'],
    ['~','~','~','~','~','~','~','~','~','~'],
    ['~','~','~','~','~','~','~','~','~','~'],
    ['~','~','~','~','~','~','~','~','~','~'],
    ['~','~','~','~','~','~','~','~','~','~'],
    ['~','~','~','~','~','~','~','~','~','~'],
    ['~','~','~','~','~','~','~','~','~','~']
]
server_guess = [
    ['~','~','~','~','~','~','~','~','~','~'],
    ['~','~','~','~','~','~','~','~','~','~'],
    ['~','~','~','~','~','~','~','~','~','~'],
    ['~','~','~','~','~','~','~','~','~','~'],
    ['~','~','~','~','~','~','~','~','~','~'],
    ['~','~','~','~','~','~','~','~','~','~'],
    ['~','~','~','~','~','~','~','~','~','~'],
    ['~','~','~','~','~','~','~','~','~','~'],
    ['~','~','~','~','~','~','~','~','~','~'],
    ['~','~','~','~','~','~','~','~','~','~']
]

#=====UTILITIES=====
def menu():
    valid_input = False
    choice = 0
    print("Welcome To Battleship\n1.Setup Server\n2. Setup as player\n3.Exit")
    while valid_input == False:
        try:
            choice = int(input(">> "))
            if choice == 1 or choice == 2 or choice == 3:
               valid_input = True 
        except:
            print("Try again")
    return choice

def get_ip():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        s.connect(('8.8.8.8', 80))
        ip = s.getsockname()[0]
    except Exception:
        ip = '127.0.0.1'
    finally:
        s.close()
    return ip

def send(text):
    conn.sendall((ZHAO_LANG_SYNTAX["PRINT"] +" "+ text).encode())

def recieve():
    conn.sendall(ZHAO_LANG_SYNTAX["IMMEDIATE REPLY"])
    data = conn.recv(1024).decode()
    return data

def send_and_recieve(text):
    conn.sendall((ZHAO_LANG_SYNTAX["PRINT WITH REPLY"] + " " + text).encode())
    data = conn.recv(1024).decode()
    return data

def end_signal():
    conn.sendall(ZHAO_LANG_SYNTAX["END GAME"])

def board_to_string(board):
    string = ""
    string = string + board_header + "\n"
    for r in range(0,SIZE):
        string = string + str(r) + " "
        for c in range(0,SIZE):
            string = string + board[r][c]
            string = string + " "
        string = string + "\n"
    return string

def place_ship(row, col, ship, board, orientation):
    try:
        if orientation == VERTICAL:
                for i in range(0, SHIP_DATA[ship]):
                    if(board[row+i][col] != UNKNOWN):
                        return False
                for i in range(0, SHIP_DATA[ship]):
                    board[row + i][col] = SHIP_REPRESENTATION[ship]
                return True
        elif orientation == HORIZONTAL:
                for i in range(0, SHIP_DATA[ship]):
                    if(board[row][col+i] != UNKNOWN):
                        return False
                for i in range(0, SHIP_DATA[ship]):
                    board[row][col+i] = SHIP_REPRESENTATION[ship]
                return True
        return False
    except IndexError:
        return False

def input_to_coordinate(text):
    try:
        column = board_header_to_column[text[0]]
        row = int(text[1])
        return (row,column)
    except:
        return None

#=====SETUP=====

def player_setup():
    for i in range(0, len(SHIP)):
        valid_placement = False
        while(valid_placement == False):
            try:
                send((board_to_string(player_board)))
                send(("Setting up for: " + SHIP[i]))
                
                reply = send_and_recieve(("Co-ordinates (Letter, Row Number): "))
                result = input_to_coordinate(reply)
                if result != None:
                    row, column = result
                    send_and_recieve("Orientation [V (Vertical)/ H (Horizontal)]: ")
                    orientation = send_and_recieve("Orientation [V (Vertical)/ H (Horizontal)]: ", end="")
                    valid_placement = place_ship(row, column, SHIP[i], player_board, orientation)
            except IndexError:
                send("Try again\n")
    return

def server_setup():
    for i in range(0, len(SHIP)):
        valid_placement = False
        while(valid_placement == False):
            row = random.randint(0,9)
            col = random.randint(0,9)
            orient = ORIENTATIONS[random.randint(0,1)]

            valid_placement = place_ship(row, col, SHIP[i],server_board,orient)
    return

#=====Game Stuff=====
def check_loss(board):
    #while it is entirely possible to use the data, this is a lot more solid because its cooler lol
    loss = True
    for r in range(0,SIZE):
        for c in range(0,SIZE):
            if board[r][c] != HIT and board[r][c] != MISS and board[r][c] != UNKNOWN:
                return False
    return True

player_ships = [True, True, True, True, True]
server_ships = [True, True, True, True, True]

def check_sunk(board, state):
    shadow_state = [False, False, False,False, False]
    for r in range(0,SIZE):
        for c in range(0,SIZE):
            #first check if the board is a boat
            if board[r][c] != UNKNOWN and board[r][c] != MISS and board[r][c] != HIT:
                #check what boat it is
                i = 0
                while (i<5):
                    if(SHIP_REPRESENTATION[SHIP[i]] == board[r][c]):
                        break
                    i = i + 1
                shadow_state[i] = True
    
    for i in range(0,5):
        if state[i] != shadow_state[i]:
            #update ship information
            state[i] = shadow_state[i]
            send(SHIP[i] + " has sunk!\n")
    return

def ship_remaining_to_string(ships):
    text = "Enemy Remaining: "
    for i in range(0,len(ship)):
        if ships[i] == True:
            text = text + SHIP[i]
            text = text + " "
    return text

def servers_turn(board):
    row = 0
    column = 0

    return (row, column)

#=====Runtimes=====
def server_runtime():
    player_setup()
    server_setup()

    player_loss = False
    server_loss = False
    
    while player_loss == False and server_loss == False:
        send(board_to_string(player_board) + "\n")
        send(board_to_string(player_guess) + "\n")
        send(ship_remaining_to_string(server_ships) + "\n")

        #player's turn
        valid_move = False
        while valid_move == False:
            reply = send_and_recieve("Where to hit: ")
            res = input_to_coordinate(reply)
            if res != None:
                row, column = res
                if(player_guess[row][column] != HIT and player_guess[row][column] != MISS):
                    if server_board[row][column] != UNKNOWN:
                        player_guess[row][column] = HIT
                        server_board[row][column] = HIT
                    elif server_board[row][column] == UNKNOWN:
                        player_guess[row][column] = MISS
                        server_board[row][column] = MISS
                    else:
                        player_guess[row][column] = "?"
                        server_board[row][column] = "?"
                    valid_move = True
                else:
                    send("Try again")
            else:
                send("Try inputting a valid co-ordinate\n")
        #check if a ship has been sunk
        check_sunk(server_board, server_ships)

        #check if player has won
        server_loss = check_loss(server_board)

        if server_loss == False:
            row, col = servers_turn(server_guess)
            if player_board[row][column] != UNKNOWN:
                server_guess[row][column] = HIT
                player_board[row][column] = HIT
            else:
                server_guess[row][column] = MISS
                player_board[row][column] = MISS

        check_sunk(player_board, player_ships)
        player_loss = check_loss(player_board)
    
    if player_loss == True:
        send("You lost! Reconnect to try again.\n")
    elif server_loss == True:
        send("You won! Reconnect to play again!\n")
    else:
        send("How?\n")

def server():
    #setup server

    HOST = get_ip()
    PORT = 0
    valid_port = False
    while valid_port == False:
        try:
            PORT = int(input("Port to listen from: "))
            valid_port == True
        except:
            print("Enter a valid port")

    print("IP Address: " + HOST)
    print("PORT: " + str(PORT))

    #find client:
    SERVER = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    SERVER.bind((HOST,PORT))
    SERVER.listen(1)

    print("Waiting for player to connect....")
    conn,addr = SERVER.accept()
    print("Connected to: " + addr)

    server_runtime()

    conn.close()
    SERVER.close()

    return

#client part of the script

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
def player_runtime():
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
            print("\n",end="")
            valid_port = True
        except:
            print("Try again...")

    CLIENT = socket.socket(socket.AF_NET, socket.SOCK_STREAM)
    CLIENT.connect((HOST, PORT))

    player_runtime()

    client.close()

    return

#actual entry
def _start():
    choice = menu()
    match choice:
        case 1:
            server()
        case 2:
            player()
        case 3:
            return

_start()