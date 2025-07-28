from bisect import insort

def print_board(board):
    print("\n   Sudoku Board")
    for i in range(9):
        if i % 3 == 0 and i != 0:
            print("-" * 21)
        for j in range(9):
            if j % 3 == 0 and j != 0:
                print("|", end=" ")
            cell = board[i][j]
            print(cell if cell != 0 else ".", end=" ")
        print()
    print()


def is_valid(board, row, col, num):
    if num in board[row]:
        return False
    for i in range(9):
        if board[i][col] == num:
            return False
    start_row, start_col = 3 * (row // 3), 3 * (col // 3)
    for i in range(3):
        for j in range(3):
            if board[start_row + i][start_col + j] == num:
                return False
    return True


def is_complete(board):
    for row in board:
        if 0 in row:
            return False
    return True


def get_sorted_candidates(board, row, col):
    """Use a sorted list to track valid numbers for a given cell."""
    candidates = []
    for num in range(1, 10):
        if is_valid(board, row, col, num):
            insort(candidates, num)  # insert while keeping list sorted
    return candidates


def play_sudoku():
    board = [
        [5, 3, 0, 0, 7, 0, 0, 0, 0],
        [6, 0, 0, 1, 9, 5, 0, 0, 0],
        [0, 9, 8, 0, 0, 0, 0, 6, 0],
        [8, 0, 0, 0, 6, 0, 0, 0, 3],
        [4, 0, 0, 8, 0, 3, 0, 0, 1],
        [7, 0, 0, 0, 2, 0, 0, 0, 6],
        [0, 6, 0, 0, 0, 0, 2, 8, 0],
        [0, 0, 0, 4, 1, 9, 0, 0, 5],
        [0, 0, 0, 0, 8, 0, 0, 7, 9]
    ]

    while not is_complete(board):
        print_board(board)
        try:
            print("Enter your move (or 0 to quit):")
            row = int(input("Row (1-9): "))
            if row == 0:
                print("👋 Exiting game.")
                return
            col = int(input("Column (1-9): "))
            if col == 0:
                print("👋 Exiting game.")
                return

            if board[row - 1][col - 1] != 0:
                print("❌ That cell is already filled.")
                continue

            # Show valid options using sorted list
            sorted_candidates = get_sorted_candidates(board, row - 1, col - 1)
            if not sorted_candidates:
                print("❌ No valid numbers for this cell.")
                continue

            print(f"✅ Valid numbers for cell ({row},{col}): {sorted_candidates}")
            num = int(input("Enter number to place: "))
            if num == 0:
                print("👋 Exiting game.")
                return

            if num not in sorted_candidates:
                print("❌ Invalid move. Not in the candidate list.")
                continue

            board[row - 1][col - 1] = num
            print("✅ Move accepted!")

        except ValueError:
            print("❌ Invalid input. Please use numbers only.")

    print_board(board)
    print("🎉 You completed the puzzle!")


if __name__ == "__main__":
    play_sudoku()
