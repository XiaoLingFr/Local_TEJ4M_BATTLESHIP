import random

GAME_END = "GM_END"
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
                print(board_to_string(player_board))
                print("Setting up for: " + SHIP[i])

                print("Co-ordinates (Letter, Row Number): ",end="")
                reply = input()
                result = input_to_coordinate(reply)
                if result != None:
                    row, column = result
                    print("Orientation [V (Vertical)/ H (Horizontal)]: ", end="")
                    orientation = input()
                    valid_placement = place_ship(row, column, SHIP[i], player_board, orientation)
            except IndexError:
                print("Try again")
    return

def server_setup():
    for i in range(0, len(SHIP)):
        valid_placement = False
        while(valid_placement == False):
            row = random.randint(0,9)
            col = random.randint(0,9)
            orient = ORIENTATIONS[random.randint(0,1)]

            valid_placement = place_ship(row, col, SHIP[i],server_board,orient)
            if valid_placement == False:
                print("Try again")
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
            print(SHIP[i] + " has sunk!")
    return

def servers_turn(board):
    row = 0
    column = 0

    return (row, column)

#=====Runtime=====
def runtime():
    player_setup()
    server_setup()

    player_loss = False
    server_loss = False
    
    while player_loss == False and server_loss == False:
        print(board_to_string(player_board))
        print(board_to_string(player_guess))

        #player's turn
        valid_move = False
        while valid_move == False:
            print("Where to hit?")
            reply = input()
            res = input_to_coordinate(reply)
            if res != None:
                row, column = res
                print(row)
                print(column)
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
                    print("Try again")
            else:
                print("Try inputting a valid co-ordinate")
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
        print("You lost! Reconnect to try again.")
    elif server_loss == True:
        print("You won! Reconnect to play again!")
    else:
        print("How?")
        
def menu():
    valid_input == False
    choice == 0
    print("Welcome To Battleship\n1.Setup Server\n2. Setup as player")
    while valid_input == False:
        try:
            choice = int(input(">> "))
            if choice == 1 or choice == 2:
               valid_input = True 
        except:
            print("Try again")
    return choice

def main():
    choice = menu()

    runtime()

if __name__ == "__main__":
    main()