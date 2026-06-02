def server_setup():
    for i in range(0, len(SHIP)):
        valid_placement = False
        while(valid_placement == False):
            row = random.randint(0,9)
            col = random.randint(0,9)
            orient = ORIENTATIONS[random.randint(0,1)]

            valid_placement = place_ship(row, col, SHIP[i],server_board,orient)
    return

#=====Algorithm=====
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
                if (SIZE-1) and original[r+1][c] != MISS and original[r+1][c] != HIT :
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
    
    for i in range(0,SIZE):
        print(probability_density[i])

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