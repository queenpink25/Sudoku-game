import tkinter as tk
from tkinter import simpledialog, messagebox

# --- Sorting algorithms ---
def selection_sort(arr):
    a = arr.copy()
    for i in range(len(a)):
        min_idx = i
        for j in range(i + 1, len(a)):
            if a[j] < a[min_idx]:
                min_idx = j
        a[i], a[min_idx] = a[min_idx], a[i]
    return a

def bubble_sort(arr):
    a = arr.copy()
    for i in range(len(a)):
        for j in range(0, len(a) - i - 1):
            if a[j] > a[j + 1]:
                a[j], a[i] = a[i], a[j]
    return a

def insertion_sort(arr):
    a = arr.copy()
    for i in range(1, len(a)):
        key = a[i]
        j = i - 1
        while j >= 0 and key < a[j]:
            a[j + 1] = a[j]
            j -= 1
        a[j + 1] = key
    return a

# --- Sudoku logic ---
def is_valid(board, row, col, num):
    if num in board[row]:
        return False
    for i in range(9):
        if board[i][col] == num:
            return False
    box_row, box_col = 3 * (row // 3), 3 * (col // 3)
    for i in range(3):
        for j in range(3):
            if board[box_row + i][box_col + j] == num:
                return False
    return True

def get_unsorted_candidates(board, row, col):
    return [num for num in range(1, 10) if is_valid(board, row, col, num)]

def is_complete(board):
    return all(cell != 0 for row in board for cell in row)

# --- GUI ---
class SudokuApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Sudoku with Sorting")
        self.entries = {}
        self.init_board()
        self.create_grid()

    def init_board(self):
        self.board = [
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

    def create_grid(self):
        grid_frame = tk.Frame(self.root)
        grid_frame.pack(padx=30, pady=30)

        for row in range(9):
            for col in range(9):
                e = tk.Entry(grid_frame, width=2, font=('Arial', 18), justify='center')
                e.grid(row=row, column=col, padx=10, pady=10)
                if self.board[row][col] != 0:
                    e.insert(0, str(self.board[row][col]))
                    e.config(state='disabled', disabledforeground='black')
                else:
                    e.bind("<Button-1>", lambda event, r=row, c=col: self.on_cell_click(r, c))
                self.entries[(row, col)] = e

    def on_cell_click(self, row, col):
        candidates = get_unsorted_candidates(self.board, row, col)
        if not candidates:
            messagebox.showerror("No Moves", "No valid numbers for this cell.")
            return

        sort_choice = simpledialog.askinteger(
            "Sorting Choice",
            "Choose sorting method:\n1 - Selection Sort\n2 - Bubble Sort\n3 - Insertion Sort",
            minvalue=1, maxvalue=3
        )

        if sort_choice == 1:
            sorted_candidates = selection_sort(candidates)
        elif sort_choice == 2:
            sorted_candidates = bubble_sort(candidates)
        elif sort_choice == 3:
            sorted_candidates = insertion_sort(candidates)
        else:
            messagebox.showinfo("Default", "Invalid choice. Using Insertion Sort.")
            sorted_candidates = insertion_sort(candidates)

        num = simpledialog.askinteger(
            "Choose Number",
            f"Valid numbers for ({row+1},{col+1}): {sorted_candidates}\nEnter your choice:",
            minvalue=1, maxvalue=9
        )

        if num not in sorted_candidates:
            messagebox.showerror("Invalid", "Number not in the candidate list.")
            return

        self.board[row][col] = num
        entry = self.entries[(row, col)]
        entry.delete(0, tk.END)
        entry.insert(0, str(num))
        entry.config(state='disabled', disabledforeground='blue')

        if is_complete(self.board):
            messagebox.showinfo("Puzzle Complete", "You completed the Sudoku puzzle!")
            self.reset_board()

    def reset_board(self):
        for widget in self.root.winfo_children():
            widget.destroy()
        self.init_board()
        self.create_grid()

# --- Run the app ---
if __name__ == "__main__":
    root = tk.Tk()
    app = SudokuApp(root)
    root.mainloop()
