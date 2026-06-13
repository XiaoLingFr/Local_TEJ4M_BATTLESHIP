#this code will be documented as it is the most verbose and more complete version of the project

import random
import socket
import copy
import time
import os

#this is how our clients will interact with each other
#they use a custom language to communicate
ZHAO_LANG_SYNTAX = {
    "PRINT": "PRNT",
    "IMMEDIATE REPLY": "IREP",
    "PRINT WITH REPLY": "PREP",
    "GAME END" : "GEND",
    "CLS" : "CLS"
}

#Since the server and game are required to be on one file,
#I have defined them here
conn = None
addr = None
SERVER = None

HOST = None
PORT = None
CLIENT = None

#this is the command for clearing the terminal
CLEAR = "clear"
#depending on if the system is a Unix or Unix adjacent or Windows NT device, the clear signal is different
if os.name == "nt":
    os.system("")
    CLEAR = "cls"

#This contains foundational data for battleship
#size of the board
SIZE = 10

#ships are defined in this order:
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

#these are representations for the ship
UNKNOWN = '~'
HIT = 'X'
MISS = 'O'

#thesea are constants for setups
VERTICAL = "V"
HORIZONTAL = "H"

ORIENTATIONS = [VERTICAL,HORIZONTAL]

#these are for conversions when the user wants to input a co-ordinate
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

#these are the client and host boards
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
#clears terminal screen
def clear_screen():
    os.system(CLEAR)

#main menu
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
            print("Please enter a valid input")
    return choice

#displays ip address for the user to know what to enter
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

#this is the server side's execution of the language
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

def clear_signal():
    conn.sendall((ZHAO_LANG_SYNTAX["CLS"] + "|").encode())

#this is how boards will be displayed over the internet
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

#this is how we check and place ships on the player's respective boards
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

#when players start shooting shots, this is how we convert it
def input_to_coordinate(text):
    try:
        column = board_header_to_column[text[0]]
        row = int(text[1])
        return (row,column)
    except:
        return None

#=====SETUP=====

#this is if a player wants to minimize time and use a random board
def random_setup(board):
    for i in range(0, len(SHIP)):
        valid_placement = False
        while(valid_placement == False):
            row = random.randint(0,9)
            col = random.randint(0,9)
            orient = ORIENTATIONS[random.randint(0,1)]

            valid_placement = place_ship(row, col, SHIP[i],board,orient)
    return

#client side setup. player_setup() is kept as legacy because im too lazy to change it
def player_setup():
    choice = 0
    valid_input = False
    while valid_input == False:
        try:
            choice = int((send_and_recieve("Would you like a randomized setup? [1: Yes 2: No]\n"))[0])
            if choice == 1 or choice == 2:
                valid_input = True
        except:
            send("Your input is invalid, try again.\n")

    if choice == 1:
        random_setup(player_board)

    else:
        for i in range(0, len(SHIP)):
            valid_placement = False
            while(valid_placement == False):
                try:
                    clear_signal()
                    send((board_to_string(player_board) + "\n"))
                    send((("Setting up for: " + SHIP[i]) + "\n"))
                    
                    reply = send_and_recieve(("Co-ordinates (Letter, Row Number): "))
                    result = input_to_coordinate(reply)
                    if result != None and result != "":
                        row, column = result
                        orientation = send_and_recieve("Orientation [V (Vertical)/ H (Horizontal)]: ")
                        valid_placement = place_ship(row, column, SHIP[i], player_board, orientation)
                except IndexError:
                    clear_signal()
                    send("Please enter a valid placement.\n")
                if valid_placement == False:
                    clear_signal()
                    send("Your current placement overlaps other ship(s) or goes out of bounds.\nTry again.\n")
            clear_signal()
    return

#host's setup. server_setup() is kept as legacy
def server_setup():
    choice = 0
    valid_input = False
    while valid_input == False:
        try:
            choice = int(input("Would you like a randomized setup? [1: Yes 2: No]: \n>>")[0])
            if choice == 1 or choice == 2:
                valid_input = True
        except:
            print("Your input is invalid, try again.\n")

    if choice == 1:
        random_setup(server_board)
    else:
        for i in range(0, len(SHIP)):
            valid_placement = False
            while(valid_placement == False):
                try:
                    clear_screen()
                    print(board_to_string(server_board))
                    print(("Setting up for: " + SHIP[i]))
                    
                    reply = print("Co-ordinates (Letter, Row Number): ")
                    result = input_to_coordinate(input(">> "))
                    if result != None:
                        row, column = result
                        orientation = input("Orientation [V (Vertical)/ H (Horizontal)]: ")
                        valid_placement = place_ship(row, column, SHIP[i], server_board, orientation)
                except IndexError:
                    clear_screen()
                    print("Please enter a valid placement.")
                if valid_placement == False:
                    clear_screen()
                    print("Your current placement overlaps other ship(s) or goes out of bounds.\nTry again.")       
            clear_screen()
    return

#=====Game Stuff=====
#checks if a player has lost based on their board
def check_loss(board):
    #while it is entirely possible to use the data, this is a lot more solid because its cooler lol
    loss = True
    for r in range(0,SIZE):
        for c in range(0,SIZE):
            if board[r][c] != HIT and board[r][c] != MISS and board[r][c] != UNKNOWN:
                return False
    return True

#this is how we track if a player has their ships sunk or not compared to the previous move
player_ships = [True, True, True, True, True]
server_ships = [True, True, True, True, True]

#this is how we check if the ships have sunk. We take the status and we check if its correct, if not, update it.
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

#we then convert the remaining ships to a string for each side to use
def ship_remaining_to_string(ships):
    text = "Enemy Remaining: "
    for i in range(0,len(ships)):
        if ships[i] == True:
            text = text + SHIP[i]
            text = text + " "
    return text

#while this was for the original AI
#I decided to keep it anyways
#because there is a huge chance that a vulnerability was caught because we put the host in their own little sandbox using functions
def servers_turn():
    print("YOUR BOARD:")
    print(board_to_string(server_board))
    print("YOUR GUESSING BOARD:")
    print(board_to_string(server_guess))
    print("CLIENT'S REMAINING SHIPS:")
    print(ship_remaining_to_string(player_ships))

    valid_move = False
    while valid_move == False:
        reply = input("Where to hit: \n>>")
        res = input_to_coordinate(reply)
        try:
            if res != None:
                row, column = res #this might cause an exception if the user enters and incomplete input
                if(server_guess[row][column] != HIT and server_guess[row][column] != MISS):
                    if player_board[row][column] != UNKNOWN:
                        server_guess[row][column] = HIT
                        player_board[row][column] = HIT
                        send(("Message: Host has hit a client ship [" + reply[0] + reply[1] + "]\n"))
                        print(("Message: You have hit a ship! [" + reply[0] + reply[1] + "]"))
                    elif player_board[row][column] == UNKNOWN:
                        server_guess[row][column] = MISS
                        player_board[row][column] = MISS
                        send("Message: Host has missed! [" + reply[0] + reply[1] + "]\n")
                        print("Message: You missed![" + reply[0] + reply[1] + "]")
                    else:
                        server_guess[row][column] = "?"
                        player_board[row][column] = "?"
                    valid_move = True
                else:
                    print("Try choosing a different co-ordinate")
            else:
                print("Try inputting a valid co-ordinate.")
        except:
            print("An invalid input was made, try again.")
    return

#=====Runtimes=====
#main server runtime
def server_runtime():
    clear_screen()
    
    RUNNING = True
    computer_turn_count = 0
    
    player_setup()
    server_setup()

    clear_screen()
    clear_signal()

    #this is just used to keep track of old player boards. However, it probably wont be used much
    player_board_copy = copy.deepcopy(player_board)
    server_board_copy = copy.deepcopy(server_board)

    player_loss = False
    server_loss = False
    
    #the game happens here
    while player_loss == False and server_loss == False and RUNNING == True:
        #handling players leaving mid match
        try:
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
                                send(("Message: You have hit a ship[" + reply[0] + reply[1] + "]\n"))
                                print(("Message: Client has hit a ship[" + reply[0] + reply[1] + "]"))
                            elif server_board[row][column] == UNKNOWN:
                                player_guess[row][column] = MISS
                                server_board[row][column] = MISS
                                send(("Message: You have missed[" + reply[0] + reply[1] + "]\n"))
                                print(("Message: Client has missed[" + reply[0] + reply[1] + "]"))
                            else:
                                player_guess[row][column] = "?"
                                server_board[row][column] = "?"
                            valid_move = True
                        else:
                            send("Please enter a different co-ordinate.\n")
                    else:
                        send("Try inputting a valid co-ordinate\n")
                except:
                    send("An invalid input was made. Try again.\n")
            
            clear_screen()
            
            #check states of players and ships for the server
            check_sunk(server_board, server_ships)
            server_loss = check_loss(server_board)

            #server's turn
            if server_loss == False:
                servers_turn()

            player_loss = check_loss(player_board)
            check_sunk(player_board, player_ships)
            
            #clear screen
            clear_signal()

        #handle mid disconnects
        except ConnectionResetError:
            print(f"Connection forcibly reset")
            RUNNING = False
            return False
        except ConnectionAbortedError:
            print(f"Connection aborted.")
            RUNNING = False
            return False

    time.sleep(3)

    #attempt to do endgame stuff
    try:
        clear_screen()
        clear_signal()
        if player_loss == True:
            send("You lost! Reconnect to try again.\n")
            print("You won! Start up the program to play again!")
        elif server_loss == True:
            send("You won! Reconnect to play again!\n")
            print("You lost! Start up the program to play again!")

        time.sleep(2)

        #this is logic for finalization of the game for the server side

        print("Client's Ships: ")
        print(board_to_string(player_board_copy))
        print("Your guesses: ")
        print(board_to_string(server_guess))
        print("Your Ships: ")
        print(board_to_string(server_board_copy))

        send("Host's Ships: \n")
        send((board_to_string(server_board_copy) + "\n"))
        send("Your guesses: \n")
        send((board_to_string(player_guess)))
        send("Your Ships: \n")
        send((board_to_string(player_board_copy) + "\n"))
        
        end_signal()
    #of course, on a broken connection, send() wont work, and it would jump to these
    except ConnectionResetError:
        return False
    except ConnectionAbortedError:
        return False

    return True

#server entrypoint and setup
def server():
    clear_screen()

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

    clear_screen()

    print("IP Address: " + HOST)
    print("PORT: " + str(PORT))

    #find client:
    SERVER = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    SERVER.bind((HOST,PORT))
    SERVER.listen(1)

    print("Waiting for player to connect....")
    conn,addr = SERVER.accept()
    print("Connected to: ", addr)

    clear_screen()
    end = server_runtime()

    conn.close()
    SERVER.close()

    return end

#client part of the script

#the client is simple, it is only designed to do two things:
#1. Print when told to
#2. Respond when told to
#3. End the game when told to

RUNNING = True

#this is how my language is interpreted by the client
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
                print("You entered without typing. Try again.")
    
    elif parse[0] == ZHAO_LANG_SYNTAX["PRINT WITH REPLY"]:
        print(parse[1])
        while valid_input == False:
            response = input(">> ")
            if len(response) > 0:
                valid_input = True
                CLIENT.sendall(response.encode())
            else:
                print("You entered without typing. Try again.")
    
    elif parse[0] == ZHAO_LANG_SYNTAX["CLS"]:
        clear_screen()

    return

#client runtime player_runtime() is legacy naming, client's version instead
def player_runtime():
    global RUNNING
    buffer = ""

    clear_screen()

    while RUNNING == True:
        try:
            data = CLIENT.recv(1024).decode()
        except:
            return False
        if data:
            buffer = buffer + data

        while "|" in buffer:
            instruction, buffer = buffer.split("|",1)
            if instruction.strip():
                result = interpret(instruction.strip())
    return True

#entrypoint for the client
def player():
    clear_screen()
    global HOST
    global PORT

    global CLIENT

    valid_IP = False
    while valid_IP == False:
        try:
            print("Host IP: ",end="")
            HOST = input()
            CLIENT = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            socket.inet_aton(HOST)
            valid_IP = True
        except: 
            print("Enter a valid IP Address")

    valid_port = False
    while valid_port == False:
        try:
            print("Host PORT: ",end="")
            PORT = int(input())
            print("\n",end="")
            valid_port = True
        except:
            print("Please try inputting a valid port")
    try:
        CLIENT.connect((HOST, PORT))
    except:
        print("An error has occured")
        return False
    
    end = player_runtime()

    CLIENT.close()

    return end 

#All code starts from here
def multiplayer():
    clear_screen()
    choice = menu()
    clear_screen()
    match choice:
        case 1:
            return server()
        case 2:
            return player()
        case 3:
            return True

end = multiplayer()

if end == True:
    print("Game exited with True status: Success")
else:
    print("Game exited with False status: Error")