import random
import socket
import copy
import time

ZHAO_LANG_SYNTAX = {
    "PRINT": "PRNT",
    "IMMEDIATE REPLY": "IREP",
    "PRINT WITH REPLY": "PREP",
    "GAME END" : "GEND",
}

conn = None
addr = None
SERVER = None

HOST = None
PORT = None
CLIENT = None

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

player_board_copy = []
server_board_copy = []

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
            print("Please enter a correct co-ordinate")
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
    conn.sendall((ZHAO_LANG_SYNTAX["PRINT"] +" "+ text + "\n"+"|").encode())

def recieve():
    conn.sendall(ZHAO_LANG_SYNTAX["IMMEDIATE REPLY"])
    data = conn.recv(1024).decode()
    return data

def send_and_recieve(text):
    conn.sendall((ZHAO_LANG_SYNTAX["PRINT WITH REPLY"] + " " + text + "\n"+"|").encode())
    data = conn.recv(1024).decode()
    return data

def end_signal():
    conn.sendall((ZHAO_LANG_SYNTAX["GAME END"] + "|").encode())
    return

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
                send((board_to_string(player_board) + "\n"))
                send((("Setting up for: " + SHIP[i]) + "\n"))
                
                reply = send_and_recieve(("Co-ordinates (Letter, Row Number): "))
                result = input_to_coordinate(reply)
                if result != None and result != "":
                    row, column = result
                    orientation = send_and_recieve("Orientation [V (Vertical)/ H (Horizontal)]: ")
                    valid_placement = place_ship(row, column, SHIP[i], player_board, orientation)
            except IndexError:
                send("Please enter a valid placement.\n")
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
            #update state information
            state[i] = shadow_state[i]
            if state is player_ships:
                send(("Message: Client's " + SHIP[i] + " has sunk!\n"))
                print("Message: Client's " + SHIP[i]+ " has sunk!")
            elif state is server_ships:
                send(("Message: Host's " + SHIP[i] + " has sunk!\n"))
                print("Message: Host's " + SHIP[i]+ " has sunk!")
            else:
                send(("Message: " + SHIP[i] + " has sunk!\n"))
                print("Message: " + SHIP[i]+ " has sunk!")
    return

def ship_remaining_to_string(ships):
    text = "Enemy Remaining: "
    for i in range(0,len(ships)):
        if ships[i] == True:
            text = text + SHIP[i]
            text = text + " "
    return text

#=====Algorithm====
pre_AI_moves = [(1,1),(1,8),(8,1),(8,8)]

SHIP_SIZE = [2,3,3,4,5]
WEIGHT = 5

def check_count(board, row, col, ship_size):
    count = 0

    #Down Case
    down = True
    right = True

    up = True
    left = True

    #down case
    try:
        for i in range(0, ship_size):
            if(board[row+i][col] == MISS):
                down = False
                break
    except IndexError:
        down = False
        pass 

    #right case:
    try:
        for i in range(0, ship_size):
            if (board[row][col+i] == MISS):
                right = False
                break
    except IndexError:
        right = False
        pass
    
    #up case:
    if row - ship_size + 1 < 0:
        up = False
    else:
        for i in range(0, ship_size):
            if (board[row-i][col] == MISS):
                up = False
                break
    
    #left case:
    if col-ship_size + 1 < 0:
        left = False
    else:
        for i in range(0, ship_size):
            if (board[row][col-i] == MISS):
                left = False
                break

    if up == True:
        count = count + 1
    if down == True:
        count = count + 1
    if left == True:
        count = count + 1
    if right == True:
        count = count + 1

    return count

def probability_function(original, board):
    #strip the board of all of its bloat
    for r in range(0,SIZE):
        for c in range(0,SIZE):
            if board[r][c] != MISS and board[r][c] != UNKNOWN:
                board[r][c] = '~'
    
    #probability calculations
    probability_density = []
    for r in range(0,SIZE):
        row_prob = []
        for c in range(0,SIZE):
            num = 0
            for i in range(0, len(SHIP_SIZE)):
                num = num + check_count(board, r, c, SHIP_SIZE[i])
            row_prob.append(num)
        probability_density.append(row_prob)
    
    for r in range(0,SIZE):
        for c in range(0,SIZE):
            if original[r][c] == HIT:
                if r<(SIZE-1) and original[r+1][c] != MISS and original[r+1][c] != HIT :
                    probability_density[r+1][c] = probability_density[r+1][c] + WEIGHT

                if c<(SIZE-1) and original[r][c+1] != MISS and original[r][c+1] != HIT:
                    probability_density[r][c+1] = probability_density[r][c+1] + WEIGHT

                if r > 0 and original[r-1][c] != MISS and original[r-1][c] != HIT:
                    probability_density[r-1][c] = probability_density[r-1][c] + WEIGHT
                
                if c > 0 and original[r][c-1] != MISS and original[r][c-1] != HIT:
                    probability_density[r][c-1] = probability_density[r][c-1] + WEIGHT
    
    #if we dont overwrite the hit with 0s, the AI will never move onto the next valid move
    for r in range(0,SIZE):
        for c in range(0,SIZE):
            if original[r][c] == HIT:
                probability_density[r][c] = 0

    return probability_density

def servers_turn(board, move_no):
    if move_no <= len(pre_AI_moves):
        return pre_AI_moves[(move_no - 1)]
    else:
        probability_density = probability_function(board,copy.deepcopy(board))

        best_row = 0
        best_col = 0
        best_value = probability_density[best_row][best_col]

        for r in range(0,SIZE):
            for c in range(0,SIZE):
                if probability_density[best_row][best_col] < probability_density[r][c]:
                    best_row = r
                    best_col = c
                    best_value = probability_density[best_row][best_col]
        return (best_row,best_col)

#=====Runtimes=====
def server_runtime():
    computer_turn_count = 0
    
    player_setup()
    server_setup()

    #this is just used to keep track of old player boards. However, it probably wont be used much
    player_board_copy = copy.deepcopy(player_board)
    server_board_copy = copy.deepcopy(server_board)

    player_loss = False
    server_loss = False
    
    #the game happens here
    while player_loss == False and server_loss == False:
        send("YOUR BOARD:\n")
        send(board_to_string(player_board) + "\n")
        send("YOUR GUESSING BOARD:\n")
        send(board_to_string(player_guess) + "\n")
        send("HOST'S REMAINING SHIPS:\n")
        send(ship_remaining_to_string(server_ships) + "\n")

        #player's turn
        valid_move = False
        while valid_move == False:
            reply = send_and_recieve("Where to hit: ")
            res = input_to_coordinate(reply)
            try:
                row, column = res
                if res != None and res != "":
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
                        send("Try choosing a different co-ordinate")
                else:
                    send("Try inputting a valid co-ordinate\n")
            except:
                send("Please enter a full input.\n")
        send("===============================\n")

        #check if any of host's ships has been sunk
        check_sunk(server_board, server_ships)
        #check if player has won
        server_loss = check_loss(server_board)
        
        #server's turn
        if server_loss == False:
            print("Server's turn!")
            computer_turn_count = computer_turn_count + 1
            AI_row, AI_col = servers_turn(server_guess,computer_turn_count)
            if player_board[AI_row][AI_col] != UNKNOWN:
                server_guess[AI_row][AI_col] = HIT
                player_board[AI_row][AI_col] = HIT
            else:
                server_guess[AI_row][AI_col] = MISS
                player_board[AI_row][AI_col] = MISS

        print("==============================")
        check_sunk(player_board, player_ships)
        player_loss = check_loss(player_board)
    
    if player_loss == True:
        send("You lost! Reconnect to try again.\n")
        print("You won! Start up the program to play again!")
    elif server_loss == True:
        send("You won! Reconnect to play again!\n")
        print("You lost! Start up the program to play again!")
    else:
        send("How?\n")
    
    time.sleep(3)

    #this is logic for finalization of the game for the server side

    print("Client's Ships: ")
    print(board_to_string(player_board_copy))

    print("Your Ships: ")
    print(board_to_string(server_board_copy))

    send("Host's Ships: \n")
    send((board_to_string(server_board_copy) + "\n"))
    send("Your Ships: \n")
    send((board_to_string(server_board_copy) + "\n"))
    
    end_signal()

    return

def server():
    #setup server
    global HOST
    global PORT

    global SERVER
    global conn
    global addr

    HOST = get_ip()
    PORT = 0
    valid_port = False
    while valid_port == False:
        try:
            PORT = int(input("Port to listen from: "))
            valid_port = True
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
    print("Connected to: ", addr)

    server_runtime()

    conn.close()
    SERVER.close()

    return

#client part of the script

RUNNING = True

def interpret(text):
    global RUNNING
    parse = text.split(" ",1)
    valid_input = False
    if parse[0] == ZHAO_LANG_SYNTAX["GAME END"]:
        RUNNING = False
    
    elif parse[0] == ZHAO_LANG_SYNTAX["PRINT"]:
        print(parse[1])

    elif parse[0] == ZHAO_LANG_SYNTAX["IMMEDIATE REPLY"]:
        while valid_input == False:
            response = input(">> ")
            if len(response) > 0:
                valid_input = True
                CLIENT.sendall(response.encode())
            else:
                print("You pressed enter without typing anything, try again.")
    
    elif parse[0] == ZHAO_LANG_SYNTAX["PRINT WITH REPLY"]:
        print(parse[1])
        while valid_input == False:
            response = input(">> ")
            if len(response) > 0:
                valid_input = True
                CLIENT.sendall(response.encode())
            else:
                print("You pressed enter without typing anything, try again.")

    return

def player_runtime():
    global RUNNING
    buffer = ""

    while RUNNING == True:
        data = CLIENT.recv(1024).decode()
        if data:
            buffer = buffer + data

        while "|" in buffer:
            instruction, buffer = buffer.split("|",1)
            if instruction.strip():
                result = interpret(instruction.strip())
    return

def player():
    global HOST
    global PORT

    global CLIENT

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

    CLIENT = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    CLIENT.connect((HOST, PORT))

    player_runtime()

    CLIENT.close()

    return

#actual entry
def multiplayer():
    choice = menu()
    match choice:
        case 1:
            server()
        case 2:
            player()
        case 3:
            return

multiplayer()