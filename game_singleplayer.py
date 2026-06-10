import random
import socket
import copy
import time
import os

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

#this is the command for clearing the terminal
CLEAR = "clear"
#depending on if the system is a Unix or Unix adjacent or Windows NT device, the clear signal is different
if os.name == "nt":
    os.system("")
    CLEAR = "cls"


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
def clear_screen():
    os.system(CLEAR)

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

def random_setup(board):
    for i in range(0, len(SHIP)):
        valid_placement = False
        while(valid_placement == False):
            row = random.randint(0,9)
            col = random.randint(0,9)
            orient = ORIENTATIONS[random.randint(0,1)]

            valid_placement = place_ship(row, col, SHIP[i],board,orient)
    return

def player_setup():
    choice = 0
    valid_input = False
    while valid_input == False:
        try:
            choice = int((input("Would you like a randomized setup? [1: Yes 2: No]: "))[0])
            if choice == 1 or choice == 2:
                valid_input = True
        except:
            clear_screen()
            print("Your input is invalid, try again.\n")

    if choice == 1:
        random_setup(player_board)
    else:
        for i in range(0, len(SHIP)):
            valid_placement = False
            while(valid_placement == False):
                try:
                    clear_screen()
                    print((board_to_string(player_board)))
                    print((("Setting up for: " + SHIP[i])))
                    
                    reply = input(("Co-ordinates (Letter, Row Number): "))
                    result = input_to_coordinate(reply)
                    if result != None and result != "":
                        row, column = result
                        orientation = input("Orientation [V (Vertical)/ H (Horizontal)]: ")
                        valid_placement = place_ship(row, column, SHIP[i], player_board, orientation)
                except IndexError:
                    clear_screen()
                    print("Please enter a valid placement.")
            clear_screen()
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
                print(("Message: Client's " + SHIP[i] + " has sunk!"))
            elif state is server_ships:
                print(("Message: Host's " + SHIP[i] + " has sunk!\n"))
            else:
                print(("Message: " + SHIP[i] + " has sunk!\n"))
    return

def ship_remaining_to_string(ships):
    text = "Enemy Remaining: "
    for i in range(0,len(ships)):
        if ships[i] == True:
            text = text + SHIP[i]
            text = text + " "
    return text

#=====Algorithm====
#the algorithm has 4 moves to play before it starts attacking the player
pre_AI_moves = [(1,1),(1,8),(8,1),(8,8)]

SHIP_SIZE = [2,3,3,4,5]

#we give biases to the computer for surrounding points next to hits that arent misses
WEIGHT = 5

#We check how many configurations a cell on the board can be
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

#we create a probability matrix
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

#we then choose a move given the probability function
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
#for legacy reasons, the server_runtime() name has not been changed. 
#But server always refers to the computer hosting the application
def server_runtime():
    clear_screen()

    computer_turn_count = 0
    
    player_setup()
    time.sleep(3) #I have problems where sometimes the player and the server gets the same board, so I have to add an delay to reset how random works
    server_setup()

    #this is just used to keep track of old player boards. However, it probably wont be used much
    player_board_copy = copy.deepcopy(player_board)
    server_board_copy = copy.deepcopy(server_board)

    player_loss = False
    server_loss = False
    
    clear_screen()

    #the game happens here
    while player_loss == False and server_loss == False:
        print("YOUR BOARD:")
        print(board_to_string(player_board))
        print("YOUR GUESSING BOARD:\n")
        print(board_to_string(player_guess))
        print("HOST'S REMAINING SHIPS:\n")
        print(ship_remaining_to_string(server_ships))

        reply = ""
        got_hit = False
        shot_hit = False

        #player's turn
        valid_move = False
        while valid_move == False:
            reply = input("Where to hit: ")
            res = input_to_coordinate(reply)
            try:
                row, column = res
                if res != None and res != "":
                    if(player_guess[row][column] != HIT and player_guess[row][column] != MISS):
                        if server_board[row][column] != UNKNOWN:
                            player_guess[row][column] = HIT
                            server_board[row][column] = HIT
                            shot_hit = True
                        elif server_board[row][column] == UNKNOWN:
                            player_guess[row][column] = MISS
                            server_board[row][column] = MISS
                            shot_hit = False
                        else:
                            player_guess[row][column] = "?"
                            server_board[row][column] = "?"
                            shot_hit = None
                        valid_move = True
                    else:
                        print("Try choosing a different co-ordinate")
                else:
                    print("Try inputting a valid co-ordinate")
            except:
                print("Please enter a full input.")
        print("===============================")

        clear_screen()
        if shot_hit == True:
            print(("Message: You have hit a ship at [" + reply[0] + reply[1] + "]"))
        elif shot_hit == False:
            print(("Message: You have missed at [" + reply[0] + reply[1] + "]"))

        #check if any of host's ships has been sunk
        check_sunk(server_board, server_ships)
        #check if player has won
        server_loss = check_loss(server_board)
        
        #server's turn
        if server_loss == False:
            computer_turn_count = computer_turn_count + 1
            AI_row, AI_col = servers_turn(server_guess,computer_turn_count)
            if player_board[AI_row][AI_col] != UNKNOWN:
                server_guess[AI_row][AI_col] = HIT
                player_board[AI_row][AI_col] = HIT
                print(("Message: Computer has hit at [" + str(AI_row) + " " + str(AI_col) + "]"))
            else:
                server_guess[AI_row][AI_col] = MISS
                player_board[AI_row][AI_col] = MISS
                print(("Message: Computer has missed at [" + str(AI_row) + " " + str(AI_col) + "]"))

        check_sunk(player_board, player_ships)
        player_loss = check_loss(player_board)
    
    if player_loss == True:
        print("You lost!")
    elif server_loss == True:
        print("You won!")
    else:
        print("How?\n")
    
    time.sleep(3)

    #this is logic for finalization of the game for the server side

    print("Host's Ships:")
    print(board_to_string(player_board_copy))
    print("Your Ships:")
    print(board_to_string(server_board_copy))

    return

server_runtime()