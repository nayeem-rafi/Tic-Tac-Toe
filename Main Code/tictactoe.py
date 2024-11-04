from random import randrange, choice

def display_board(board):
    print("+-------" * 3, "+", sep="")
    for row in range(3):
        print("|       " * 3, "|", sep="")
        for col in range(3):
            print("|   " + str(board[row][col]) + "   ", end="")
        print("|")
        print("|       " * 3, "|", sep="")
        print("+-------" * 3, "+", sep="")

def enter_move(board):
    while True:
        move = input("Enter your move (1-9): ")
        if move.isdigit() and 1 <= int(move) <= 9:
            move = int(move) - 1
            row, col = divmod(move, 3)
            if board[row][col] not in ['O', 'X']:
                board[row][col] = 'O'
                break
            else:
                print("Field already occupied - try again!")
        else:
            print("Invalid input - try again!")

def make_list_of_free_fields(board):
    free = []
    for row in range(3):
        for col in range(3):
            if board[row][col] not in ['O', 'X']:
                free.append((row, col))
    return free

def victory_for(board, sgn):
    for rc in range(3):
        if all(board[rc][col] == sgn for col in range(3)) or all(board[row][rc] == sgn for row in range(3)):
            return True
    if all(board[i][i] == sgn for i in range(3)) or all(board[i][2 - i] == sgn for i in range(3)):
        return True
    return False

def draw_move(board):
    free = make_list_of_free_fields(board)

    # Check if the bot can win
    for row, col in free:
        board[row][col] = 'X'
        if victory_for(board, 'X'):
            return
        board[row][col] = row * 3 + col + 1  # reset

    # Block the player's winning move
    for row, col in free:
        board[row][col] = 'O'
        if victory_for(board, 'O'):
            board[row][col] = 'X'
            return
        board[row][col] = row * 3 + col + 1  # reset

    # Otherwise, choose a random free spot
    row, col = choice(free)
    board[row][col] = 'X'

def main():
    board = [[3 * j + i + 1 for i in range(3)] for j in range(3)]

    # Randomize who starts
    human_turn = choice([True, False])

    # If the bot starts, make a single initial move
    if not human_turn:
        row, col = choice(make_list_of_free_fields(board))
        board[row][col] = 'X'
        human_turn = True  # Pass turn to the user after bot's initial move

    while True:
        display_board(board)
        if human_turn:
            enter_move(board)
            if victory_for(board, 'O'):
                display_board(board)
                print("You won!")
                break
        else:
            draw_move(board)
            if victory_for(board, 'X'):
                display_board(board)
                print("I won!")
                break

        human_turn = not human_turn
        if not make_list_of_free_fields(board):
            display_board(board)
            print("It's a tie!")
            break

main()
