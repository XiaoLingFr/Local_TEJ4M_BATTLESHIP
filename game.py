import player
import server
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

def _start():
    choice = menu()
    match choice:
        case 1:
            server()
        case 2:
            player()
    runtime()

