import copy
SIZE = 10

UNKNOWN = '~'
HIT = 'X'
MISS = 'O'

pre_AI = True
pre_AI_moves = [(1,1),(1,8),(8,1),(8,8)]

SHIP_SIZE = [2,3,3,4,5]

def check_count(board, row, col, ship_size):
    count = 0
    #vertical case
    vertical = True
    horizontal = True
    try:
        for i in range(0, ship_size):
            if(board[row+i][col] == MISS):
                vertical = False
                break
    except IndexError:
        pass 

    #horizontal case:
    try:
        for i in range(0, ship_size):
            if (board[row][col+i] == MISS):
                horizontal = False
                break
    except IndexError:
        pass

    if horizontal == True:
        count = count + 1
    if vertical == True:
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
                if (SIZE-1) and original[r+1][c] != MISS and original[r+1][c] != HIT :
                    probability_density[r+1][c] = probability_density[r+1][c] + 50

                if c<(SIZE-1) and original[r][c+1] != MISS and original[r][c+1] != HIT:
                    probability_density[r][c+1] = probability_density[r][c+1] + 50

                if r > 0 and original[r-1][c] != MISS and original[r-1][c] != HIT:
                    probability_density[r-1][c] = probability_density[r-1][c] + 50
                
                if c > 0 and original[r][c-1] != MISS and original[r][c-1] != HIT:
                    probability_density[r][c-1] = probability_density[r][c-1] + 50
    
    for i in range(0,SIZE):
        print(probability_density[i])

    return probability_density

def servers_turn(board, move_no):
    if move_no < len(pre_AI_moves):
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

server_guess = server_guess = [
    ['~','~','~','~','~','~','~','~','~','~'],
    ['~','X','X','~','~','~','~','~','O','~'],
    ['~','~','~','~','~','~','~','~','~','~'],
    ['~','~','~','~','~','~','~','~','~','~'],
    ['~','~','~','~','~','~','~','~','~','~'],
    ['~','~','~','~','~','~','~','~','~','~'],
    ['~','~','~','~','~','~','~','~','~','~'],
    ['~','~','~','~','~','~','~','~','~','~'],
    ['~','O','~','~','~','~','~','~','O','~'],
    ['~','~','~','~','~','~','~','~','~','~']
]

row, col = servers_turn(server_guess, 6)

for i in range(0,SIZE):
    print(server_guess[i])

print (row)
print (col)