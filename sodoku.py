import tkinter as tk
from tkinter import messagebox
import random
from copy import deepcopy
import winsound
import time
import threading
import pygame  

BG_BLACK = "#000000"         
CARD_BG = "#1a1d23"          
CELL_BG = "#2d333b"          
TEXT_WHITE = "#ffffff"       
ACCENT_CYAN = "#00e5ff"      
TEXT_ORANGE = "#ff9f43"      
SUCCESS_GREEN = "#00c853"    
ERROR_RED = "#ff5252"        

SIZE = 9

class KadukoUltraPro:
    def __init__(self, root):
        self.root = root
        self.root.title("KADUKO ULTRA PRO")
        self.root.geometry("600x800") 
        self.root.configure(bg=BG_BLACK)
        
        pygame.mixer.init()
        
        self.cells = {}
        self.lives = 6
        self.game_active = True
        self.start_time = time.time()
        
        self.setup_ui()
        self.new_game()
        
        self.play_my_music("Jeremy Korpas - Sour Rock ♫ NO COPYRIGHT 8-bit Music - Free Music (youtube).mp3")
        
        self.update_timer()

    def play_my_music(self, arquivo):
        try:
            pygame.mixer.music.load(arquivo)
            pygame.mixer.music.set_volume(0.2)
            pygame.mixer.music.play(-1) 
        except:
            pass

    def setup_ui(self):
        self.header_frame = tk.Frame(self.root, bg=BG_BLACK)
        self.header_frame.pack(fill="x", padx=40, pady=(15, 0))

        self.label_lives = tk.Label(
            self.header_frame, text="LIVES: " + "❤"*self.lives,
            font=("Impact", 12), bg=BG_BLACK, fg=ERROR_RED
        )
        self.label_lives.pack(side="left")

        self.label_timer = tk.Label(
            self.header_frame, text="TIME: 00:00",
            font=("Impact", 12), bg=BG_BLACK, fg=ACCENT_CYAN
        )
        self.label_timer.pack(side="right")

        tk.Label(
            self.root, text="KADUKO ULTRA PRO",
            font=("Impact", 22), bg=BG_BLACK, fg=ACCENT_CYAN
        ).pack(pady=5)

        self.main_card = tk.Frame(self.root, bg=CARD_BG, padx=10, pady=10)
        self.main_card.pack(padx=20, pady=5)

        self.board_frame = tk.Frame(self.main_card, bg="#3e4451", bd=2)
        self.board_frame.pack()

        for r in range(SIZE):
            for c in range(SIZE):
                px = (3, 1) if c % 3 == 0 and c != 0 else 1
                py = (3, 1) if r % 3 == 0 and r != 0 else 1

                cell = tk.Entry(
                    self.board_frame, width=2, font=("Arial", 18, "bold"),
                    justify="center", bg=CELL_BG, fg=TEXT_WHITE,
                    insertbackground=TEXT_WHITE, relief="flat",
                    highlightthickness=1, highlightbackground="#1a1d23"
                )
                cell.grid(row=r, column=c, padx=px, pady=py, ipady=6, ipadx=4)
                cell.bind("<KeyRelease>", lambda e, r=r, c=c: self.on_input(r, c))
                self.cells[(r, c)] = cell

        self.btn_frame = tk.Frame(self.root, bg=BG_BLACK)
        self.btn_frame.pack(pady=15, side="bottom")

        tk.Button(
            self.btn_frame, text="NOVO JOGO", command=self.new_game,
            font=("Arial", 11, "bold"), bg=ACCENT_CYAN, fg=BG_BLACK,
            width=12, relief="flat", cursor="hand2"
        ).grid(row=0, column=0, padx=10)

        tk.Button(
            self.btn_frame, text="REINICIAR", command=self.reset_current,
            font=("Arial", 11, "bold"), bg="#7f8c8d", fg=TEXT_WHITE,
            width=12, relief="flat", cursor="hand2"
        ).grid(row=0, column=1, padx=10)

    def update_timer(self):
        if self.game_active:
            elapsed = int(time.time() - self.start_time)
            mins, secs = divmod(elapsed, 60)
            self.label_timer.config(text=f"TIME: {mins:02d}:{secs:02d}")
        self.root.after(1000, self.update_timer)

    def new_game(self):
        self.lives = 6
        self.game_active = True
        self.start_time = time.time()
        self.label_lives.config(text="LIVES: " + "❤"*self.lives)
        self.solution = [[0]*SIZE for _ in range(SIZE)]
        self.solve(self.solution)
        self.puzzle = deepcopy(self.solution)
        for _ in range(45):
            r, c = random.randint(0, 8), random.randint(0, 8)
            self.puzzle[r][c] = 0
        self.draw_puzzle()

    def draw_puzzle(self):
        for (r, c), cell in self.cells.items():
            cell.config(state="normal", bg=CELL_BG)
            cell.delete(0, tk.END)
            val = self.puzzle[r][c]
            if val != 0:
                cell.insert(0, val)
                cell.config(state="disabled", disabledbackground=CELL_BG, disabledforeground=TEXT_ORANGE)
            else:
                cell.config(fg=TEXT_WHITE)

    def on_input(self, r, c):
        if not self.game_active: return
        cell = self.cells[(r, c)]
        val = cell.get()
        if not val: return
        char = val[-1]
        if char not in "123456789":
            cell.delete(0, tk.END)
            return
        cell.delete(0, tk.END)
        cell.insert(0, char)
        if int(char) == self.solution[r][c]:
            cell.config(state="disabled", disabledbackground=SUCCESS_GREEN, disabledforeground=BG_BLACK)
            winsound.Beep(1000, 100)
            self.check_victory()
        else:
            self.lives -= 1
            self.label_lives.config(text="LIVES: " + "❤"*self.lives)
            winsound.Beep(300, 200)
            cell.config(bg=ERROR_RED)
            self.root.after(300, lambda: [cell.delete(0, tk.END), cell.config(bg=CELL_BG)])
            if self.lives <= 0: messagebox.showinfo("FIM", "Sem vidas!"); self.new_game()

    def check_victory(self):
        full = True
        for (r,c), cell in self.cells.items():
            if not cell.get().isdigit():
                full = False
                break
        if full:
            messagebox.showinfo("VITÓRIA", "KADUKO COMPLETADO!")
            self.game_active = False

    def reset_current(self):
        self.draw_puzzle()
        self.lives = 6
        self.start_time = time.time()
        self.label_lives.config(text="LIVES: " + "❤"*self.lives)

    def solve(self, board):
        for r in range(SIZE):
            for c in range(SIZE):
                if board[r][c] == 0:
                    nums = list(range(1, 10))
                    random.shuffle(nums)
                    for n in nums:
                        if self.is_valid(board, n, (r, c)):
                            board[r][c] = n
                            if self.solve(board): return True
                            board[r][c] = 0
                    return False
        return True

    def is_valid(self, board, n, pos):
        for i in range(SIZE):
            if board[pos[0]][i] == n or board[i][pos[1]] == n: return False
        br, bc = (pos[0]//3)*3, (pos[1]//3)*3
        for i in range(br, br+3):
            for j in range(bc, bc+3):
                if board[i][j] == n: return False
        return True

if __name__ == "__main__":
    root = tk.Tk()
    app = KadukoUltraPro(root)
    root.mainloop()