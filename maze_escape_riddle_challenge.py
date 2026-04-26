import tkinter as tk
import random
from collections import deque
from tkinter import messagebox, simpledialog

CELL_SIZE = 40
ROWS, COLS = 10, 10

# Riddles database
riddles = [
    ("What has keys but can't open locks?", "keyboard"),
    ("What runs but never walks?", "water"),
    ("I speak without a mouth and hear without ears. What am I?", "echo"),
    ("What has a heart that doesn’t beat?", "artichoke"),
]

# BFS
def bfs_path(maze, start, goal):
    queue = deque([(start, [])])
    visited = set([start])

    while queue:
        (r, c), path = queue.popleft()

        if (r, c) == goal:
            return path + [(r, c)]

        for dr, dc in [(1,0),(-1,0),(0,1),(0,-1)]:
            nr, nc = r + dr, c + dc
            if 0 <= nr < ROWS and 0 <= nc < COLS:
                if maze[nr][nc] == 0 and (nr, nc) not in visited:
                    visited.add((nr, nc))
                    queue.append(((nr, nc), path + [(r, c)]))
    return None

# Generate maze
def generate_maze():
    while True:
        maze = [[0 if random.random() > 0.3 else 1 for _ in range(COLS)] for _ in range(ROWS)]
        maze[0][0] = 0
        maze[ROWS-1][COLS-1] = 0

        if bfs_path(maze, (0,0), (ROWS-1, COLS-1)):
            return maze

maze = generate_maze()
player_pos = [0, 0]
goal = (ROWS-1, COLS-1)
moves = 0

# Random obstacle positions
obstacles = set()
while len(obstacles) < 5:
    r, c = random.randint(1, ROWS-2), random.randint(1, COLS-2)
    if (r, c) != (0,0) and (r,c) != goal and maze[r][c] == 0:
        obstacles.add((r,c))

# GUI
root = tk.Tk()
root.title("Maze Escape: Riddle Challenge")

canvas = tk.Canvas(root, width=COLS*CELL_SIZE, height=ROWS*CELL_SIZE)
canvas.pack()

# Draw
def draw(path_hint=None):
    canvas.delete("all")

    for i in range(ROWS):
        for j in range(COLS):
            x1, y1 = j*CELL_SIZE, i*CELL_SIZE
            x2, y2 = x1+CELL_SIZE, y1+CELL_SIZE

            if maze[i][j] == 1:
                canvas.create_rectangle(x1,y1,x2,y2, fill="black")
            else:
                canvas.create_rectangle(x1,y1,x2,y2, fill="white")

    # Obstacles
    for r, c in obstacles:
        canvas.create_rectangle(c*CELL_SIZE+10, r*CELL_SIZE+10,
                                c*CELL_SIZE+30, r*CELL_SIZE+30,
                                fill="orange")

    # Hint
    if path_hint:
        for r, c in path_hint:
            canvas.create_rectangle(c*CELL_SIZE+15, r*CELL_SIZE+15,
                                    c*CELL_SIZE+25, r*CELL_SIZE+25,
                                    fill="yellow")

    # Player
    canvas.create_oval(player_pos[1]*CELL_SIZE+5,
                       player_pos[0]*CELL_SIZE+5,
                       player_pos[1]*CELL_SIZE+35,
                       player_pos[0]*CELL_SIZE+35,
                       fill="blue")

    # Goal
    canvas.create_rectangle(goal[1]*CELL_SIZE,
                            goal[0]*CELL_SIZE,
                            goal[1]*CELL_SIZE+CELL_SIZE,
                            goal[0]*CELL_SIZE+CELL_SIZE,
                            fill="green")

# Riddle trigger
def ask_riddle():
    question, answer = random.choice(riddles)
    user = simpledialog.askstring("Riddle Challenge 🤔", question)

    if user and user.lower() == answer:
        messagebox.showinfo("Correct! ", "You may proceed!")
        return True
    else:
        messagebox.showerror("Wrong ", "Penalty! +3 moves")
        return False

# Move
def move(dx, dy):
    global moves
    nr = player_pos[0] + dx
    nc = player_pos[1] + dy

    if 0 <= nr < ROWS and 0 <= nc < COLS and maze[nr][nc] == 0:
        player_pos[0], player_pos[1] = nr, nc
        moves += 1

        # Check obstacle
        if (nr, nc) in obstacles:
            if not ask_riddle():
                moves += 3
            obstacles.remove((nr, nc))

        # Check win
        if (nr, nc) == goal:
            show_victory()

    draw()

# Victory Screen
def show_victory():
    win = tk.Toplevel(root)
    win.title("🎉 Victory Dashboard")
    win.geometry("400x300")
    win.configure(bg="purple")

    tk.Label(win, text="🏆 YOU WON! 🏆", font=("Arial", 20, "bold"),
             fg="yellow", bg="purple").pack(pady=20)

    tk.Label(win, text=f"Total Moves: {moves}",
             font=("Arial", 14), fg="white", bg="purple").pack(pady=10)

    tk.Label(win, text="Amazing Problem Solving! ",
             font=("Arial", 12), fg="cyan", bg="purple").pack(pady=10)

# Controls
def key_press(event):
    if event.keysym == "Up":
        move(-1,0)
    elif event.keysym == "Down":
        move(1,0)
    elif event.keysym == "Left":
        move(0,-1)
    elif event.keysym == "Right":
        move(0,1)

# AI Hint
def show_hint():
    path = bfs_path(maze, tuple(player_pos), goal)
    draw(path_hint=path)

# Restart
def restart():
    global maze, player_pos, moves, obstacles
    maze = generate_maze()
    player_pos = [0, 0]
    moves = 0
    obstacles = set()
    while len(obstacles) < 5:
        r, c = random.randint(1, ROWS-2), random.randint(1, COLS-2)
        if maze[r][c] == 0:
            obstacles.add((r,c))
    draw()

# Buttons
frame = tk.Frame(root)
frame.pack()

tk.Button(frame, text=" Hint", command=show_hint).pack(side="left", padx=5)
tk.Button(frame, text=" Restart", command=restart).pack(side="left", padx=5)

root.bind("<Key>", key_press)

draw()
root.mainloop()
