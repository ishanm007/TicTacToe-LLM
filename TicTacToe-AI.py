# python3 -m venv .venv    
# source .venv/bin/activate  
# export OPENAI_API_KEY="your openai api key"
# python TicTacToe-AI.py


import random


# ==================================================
# BOARD DISPLAY
# ==================================================

def print_board(board):
    print()

    for row in range(3):
        start = row * 3

        print(
            f" {board[start]} | "
            f"{board[start + 1]} | "
            f"{board[start + 2]} "
        )

        if row < 2:
            print("---+---+---")

    print()


def show_positions():
    print("\nPosition guide:")
    print(" 1 | 2 | 3 ")
    print("---+---+---")
    print(" 4 | 5 | 6 ")
    print("---+---+---")
    print(" 7 | 8 | 9 ")
    print()


# ==================================================
# GAME RULES
# ==================================================

WINNING_LINES = [
    (0, 1, 2),
    (3, 4, 5),
    (6, 7, 8),
    (0, 3, 6),
    (1, 4, 7),
    (2, 5, 8),
    (0, 4, 8),
    (2, 4, 6),
]


def available_moves(board):
    return [
        i for i, cell in enumerate(board)
        if cell not in ("X", "O")
    ]


def check_winner(board):
    for a, b, c in WINNING_LINES:
        if (
            board[a] == board[b] == board[c]
            and board[a] in ("X", "O")
        ):
            return board[a]

    return None


def is_draw(board):
    return (
        check_winner(board) is None
        and not available_moves(board)
    )


# ==================================================
# HUMAN PLAYER
# ==================================================

def get_human_move(board, player):
    while True:
        choice = input(
            f"Player {player}, choose a position (1-9): "
        ).strip()

        if not choice.isdigit():
            print("Enter a number from 1 to 9.")
            continue

        position = int(choice)

        if not 1 <= position <= 9:
            print("Position must be between 1 and 9.")
            continue

        index = position - 1

        if index not in available_moves(board):
            print("That position is occupied. Try another.")
            continue

        return index


# ==================================================
# PERFECT AI: MINIMAX ALGORITHM
# ==================================================

def minimax(board, is_ai_turn, depth=0):
    """
    Explore every possible future game state.

    AI symbol: O
    Human symbol: X

    Positive score = good for AI.
    Negative score = good for human.
    Zero = draw.
    """

    winner = check_winner(board)

    # AI has won.
    if winner == "O":
        return 10 - depth

    # Human has won.
    if winner == "X":
        return depth - 10

    # No winner and no empty positions means draw.
    moves = available_moves(board)

    if not moves:
        return 0

    # AI tries to maximize its score.
    if is_ai_turn:
        best_score = float("-inf")

        for move in moves:
            # Try this move for the AI.
            board[move] = "O"

            # Explore the human's best response.
            score = minimax(
                board,
                is_ai_turn=False,
                depth=depth + 1
            )

            # Undo the move to explore other possibilities.
            board[move] = str(move + 1)

            best_score = max(best_score, score)

        return best_score

    # Human is assumed to play optimally,
    # so choose the response that minimizes the AI's score.
    else:
        best_score = float("inf")

        for move in moves:
            # Try this move for the human.
            board[move] = "X"

            # Explore the AI's next response.
            score = minimax(
                board,
                is_ai_turn=True,
                depth=depth + 1
            )

            # Undo the move.
            board[move] = str(move + 1)

            best_score = min(best_score, score)

        return best_score


def get_ai_move(board):
    """
    Examine every legal AI move and select one
    with the highest possible Minimax score.
    """

    moves = available_moves(board)

    if not moves:
        return None

    best_score = float("-inf")
    best_moves = []

    for move in moves:
        # Simulate the AI choosing this position.
        board[move] = "O"

        # Evaluate all possible responses from this position.
        score = minimax(
            board,
            is_ai_turn=False,
            depth=1
        )

        # Restore the original empty position.
        board[move] = str(move + 1)

        # Keep every move that achieves the best score.
        if score > best_score:
            best_score = score
            best_moves = [move]

        elif score == best_score:
            best_moves.append(move)

    # If several moves are equally good, choose randomly.
    return random.choice(best_moves)


# ==================================================
# GAME MODES
# ==================================================

def play_game(mode):
    board = [str(i) for i in range(1, 10)]
    current_player = "X"

    print("\n" + "=" * 38)
    print("           TIC-TAC-TOE")
    print("=" * 38)

    show_positions()

    if mode == "1":
        print("Player 1 = X | Player 2 = O")
    else:
        print("You = X | Perfect AI = O")

    while True:
        print_board(board)

        # Player vs Player
        if mode == "1":
            move = get_human_move(board, current_player)

        # Player vs AI: human's turn
        elif current_player == "X":
            move = get_human_move(board, "X")

        # Player vs AI: computer's turn
        else:
            print("AI is calculating the best move...")

            move = get_ai_move(board)

            if move is not None:
                print(f"AI chooses position {move + 1}.")

        # Safety check
        if move is None or move not in available_moves(board):
            print("No legal move available. Ending this game.")
            break

        # Place the selected symbol on the board.
        board[move] = current_player

        # Check whether someone has won.
        winner = check_winner(board)

        if winner:
            print_board(board)

            if mode == "1":
                print(f"Player {winner} wins!")

            elif winner == "X":
                print("Congratulations! You beat the AI!")

            else:
                print("The Perfect AI wins!")

            break

        # Check for a draw.
        if is_draw(board):
            print_board(board)
            print("It's a draw!")
            break

        # Switch players.
        current_player = (
            "O" if current_player == "X" else "X"
        )


# ==================================================
# MAIN MENU
# ==================================================

def main():
    while True:
        print("\n" + "=" * 38)
        print("          TIC-TAC-TOE MENU")
        print("=" * 38)

        print("1. Player vs Player")
        print("2. Player vs Perfect AI")
        print("3. Show position guide")
        print("4. Exit")

        choice = input("\nChoose an option (1-4): ").strip()

        if choice == "1":
            play_game("1")

        elif choice == "2":
            play_game("2")

        elif choice == "3":
            show_positions()

        elif choice == "4":
            print("Thanks for playing!")
            break

        else:
            print("Invalid choice. Enter 1, 2, 3, or 4.")


# ==================================================
# PROGRAM ENTRY POINT
# ==================================================

if __name__ == "__main__":
    main()
