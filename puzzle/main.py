import tkinter as tk
from tkinter import filedialog, messagebox
import time
from solver import a_star, is_solvable
from utils import read_puzzle_from_file

class PuzzleGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("8 Puzzle & 15 Puzzle Solver")
        self.size = 3  # mặc định
        self.tile_size = 80
        self.margin = 20
        self.canvas = tk.Canvas(root, width=400, height=400, bg="white")
        self.canvas.grid(row=5, column=0, columnspan=3, pady=10)
        self.canvas.bind("<Button-1>", self.user_click)

        self.state = []
        self.goal = []
        self.path = []
        self.step = 0

        # Widgets
        tk.Button(root, text="Chọn 8 Puzzle", command=lambda: self.set_size(3)).grid(row=0, column=0)
        tk.Button(root, text="Chọn 15 Puzzle", command=lambda: self.set_size(4)).grid(row=0, column=1)
        tk.Button(root, text="Đọc file input", command=self.load_file).grid(row=1, column=0)
        tk.Button(root, text="Giải Puzzle", command=self.solve).grid(row=1, column=1)
        tk.Button(root, text="Auto Solve", command=self.auto_solve).grid(row=2, column=0)

        self.status = tk.Label(root, text="Trạng thái")
        self.status.grid(row=3, column=0, columnspan=2)

    def set_size(self, size):
        self.size = size
        self.status.config(text=f"Đang dùng: {size}x{size}")
        self.canvas.delete("all")

    def draw(self, state):
        self.canvas.delete("all")
        for i in range(self.size):
            for j in range(self.size):
                val = state[i * self.size + j]
                x0 = self.margin + j * self.tile_size
                y0 = self.margin + i * self.tile_size
                x1 = x0 + self.tile_size
                y1 = y0 + self.tile_size
                if val == 0:
                    color = "white"
                else:
                    correct_val = self.goal[i * self.size + j] if self.goal else val
                    color = "lightgreen" if val == correct_val else "tomato"
                self.canvas.create_rectangle(x0, y0, x1, y1, fill=color, outline="black")
                if val != 0:
                    self.canvas.create_text((x0 + x1) / 2, (y0 + y1) / 2,
                                            text=str(val), font=("Arial", 20, "bold"))

    def load_file(self):
        path = filedialog.askopenfilename(title="Chọn file bắt đầu")
        goal_path = filedialog.askopenfilename(title="Chọn file đích")
        if not path or not goal_path:
            return
        try:
            self.state = read_puzzle_from_file(path)
            self.goal = read_puzzle_from_file(goal_path)
            if len(self.state) != self.size * self.size:
                raise ValueError("Sai kích thước.")
            self.draw(self.state)
            self.status.config(text="Đã đọc file.")
        except Exception as e:
            messagebox.showerror("Lỗi", str(e))

    def solve(self):
        if not self.state or not self.goal:
            return
        if not is_solvable(self.state, self.size):
            messagebox.showinfo("Kết quả", "Puzzle không thể giải.")
            return
        self.path = a_star(self.state, self.goal, self.size)
        self.step = 0
        self.status.config(text=f"Tìm thấy {len(self.path)-1} bước.")
        self.draw(self.path[0])

    def auto_solve(self):
        if not self.path:
            return
        for i, state in enumerate(self.path):
            self.draw(state)
            self.status.config(text=f"Bước {i}/{len(self.path)-1}")
            self.root.update()
            time.sleep(0.5)

    def user_click(self, event):
        if not self.state:
            return
        row = (event.y - self.margin) // self.tile_size
        col = (event.x - self.margin) // self.tile_size
        idx = row * self.size + col
        if 0 <= row < self.size and 0 <= col < self.size:
            zero_idx = self.state.index(0)
            x0, y0 = divmod(zero_idx, self.size)
            x1, y1 = divmod(idx, self.size)
            if abs(x0 - x1) + abs(y0 - y1) == 1:
                state = list(self.state)
                state[zero_idx], state[idx] = state[idx], state[zero_idx]
                self.state = tuple(state)
                self.draw(self.state)
                if self.state == self.goal:
                    messagebox.showinfo("Chúc mừng", "Bạn đã giải xong puzzle!")

if __name__ == "__main__":
    root = tk.Tk()
    app = PuzzleGUI(root)
    root.mainloop()
