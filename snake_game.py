import tkinter as tk
from tkinter import font as tkfont
import random
import time
from tkinter import messagebox
import os
import winsound

# Constants
WIDTH, HEIGHT = 800, 600
GRID_SIZE = 20
GRID_WIDTH = WIDTH // GRID_SIZE
GRID_HEIGHT = HEIGHT // GRID_SIZE
GAME_SPEED = 100  # Milliseconds between updates (lower = faster)

# Colors
BLACK = "#000000"
WHITE = "#FFFFFF"
GREEN = "#00FF00"
RED = "#FF0000"
BLUE = "#0000FF"
DARK_GREEN = "#008800"
PURPLE = "#800080"
TEAL = "#008080"
GOLD = "#FFD700"
BACKGROUND_COLOR = "#0A141E"
GRID_COLOR = "#283238"

# Game settings
INITIAL_SPEED = 150  # Milliseconds between moves (lower = faster)
MIN_SPEED = 50  # Maximum speed (minimum delay)
ACCELERATION = 5  # How much to reduce delay when eating food
FOOD_SPAWN_RATE = 1

# Create screen
class SnakeGame(tk.Tk):
    def __init__(self):
        super().__init__()
        
        self.title('Tabish Balti Game')
        self.geometry(f"{WIDTH}x{HEIGHT}")
        self.resizable(False, False)
        self.configure(bg=BACKGROUND_COLOR)
        
        # Configure fonts
        self.title_font = tkfont.Font(family="Arial", size=36, weight="bold")
        self.score_font = tkfont.Font(family="Arial", size=14)
        self.button_font = tkfont.Font(family="Arial", size=16, weight="bold")
        self.game_over_font = tkfont.Font(family="Arial", size=40, weight="bold")
        
        # Game variables
        self.high_score = 0
        self.current_frame = None
        
        # Start with menu
        self.show_start_screen()
    
    def clear_screen(self):
        if self.current_frame:
            self.current_frame.destroy()
        self.current_frame = tk.Frame(self, bg=BACKGROUND_COLOR)
        self.current_frame.pack(fill=tk.BOTH, expand=True)
        
    def show_start_screen(self):
        self.clear_screen()
        
        title_label = tk.Label(
            self.current_frame, 
            text="Tabish Balti Game",
            font=self.title_font,
            fg=WHITE,
            bg=BACKGROUND_COLOR
        )
        title_label.pack(pady=(HEIGHT//4, 10))
        
        subtitle_label = tk.Label(
            self.current_frame,
            text="Classic Snake Game with a Modern Twist",
            font=self.score_font,
            fg=TEAL,
            bg=BACKGROUND_COLOR
        )
        subtitle_label.pack(pady=(0, 40))
        
        start_button = tk.Button(
            self.current_frame,
            text="Start Game",
            font=self.button_font,
            bg=TEAL,
            fg=WHITE,
            activebackground=DARK_GREEN,
            activeforeground=WHITE,
            width=15,
            height=2,
            relief=tk.RAISED,
            command=self.start_game
        )
        start_button.pack(pady=10)
        
        quit_button = tk.Button(
            self.current_frame,
            text="Quit",
            font=self.button_font,
            bg=RED,
            fg=WHITE,
            activebackground="#C00000",
            activeforeground=WHITE,
            width=15,
            height=2,
            relief=tk.RAISED,
            command=self.quit
        )
        quit_button.pack(pady=10)
    
    def show_game_over_screen(self, score):
        if score > self.high_score:
            self.high_score = score
            
        self.clear_screen()
        
        # Play game over sound
        try:
            winsound.Beep(300, 300)
            winsound.Beep(200, 300)
        except:
            pass
        
        game_over_label = tk.Label(
            self.current_frame,
            text="GAME OVER",
            font=self.game_over_font,
            fg=RED,
            bg=BACKGROUND_COLOR
        )
        game_over_label.pack(pady=(HEIGHT//4, 20))
        
        score_label = tk.Label(
            self.current_frame,
            text=f"Score: {score}",
            font=self.score_font,
            fg=WHITE,
            bg=BACKGROUND_COLOR
        )
        score_label.pack(pady=5)
        
        high_score_label = tk.Label(
            self.current_frame,
            text=f"High Score: {self.high_score}",
            font=self.score_font,
            fg=GOLD,
            bg=BACKGROUND_COLOR
        )
        high_score_label.pack(pady=(5, 30))
        
        restart_button = tk.Button(
            self.current_frame,
            text="Play Again",
            font=self.button_font,
            bg=TEAL,
            fg=WHITE,
            activebackground=DARK_GREEN,
            activeforeground=WHITE,
            width=15,
            height=2,
            relief=tk.RAISED,
            command=self.start_game
        )
        restart_button.pack(pady=10)
        
        quit_button = tk.Button(
            self.current_frame,
            text="Quit",
            font=self.button_font,
            bg=RED,
            fg=WHITE,
            activebackground="#C00000",
            activeforeground=WHITE,
            width=15,
            height=2,
            relief=tk.RAISED,
            command=self.quit
        )
        quit_button.pack(pady=10)
    
    def start_game(self):
        self.clear_screen()
        self.game_canvas = tk.Canvas(
            self.current_frame,
            width=WIDTH,
            height=HEIGHT,
            bg=BACKGROUND_COLOR,
            highlightthickness=0
        )
        self.game_canvas.pack()
        
        # Draw grid
        for x in range(0, WIDTH, GRID_SIZE):
            for y in range(0, HEIGHT, GRID_SIZE):
                self.game_canvas.create_rectangle(
                    x, y, x + GRID_SIZE, y + GRID_SIZE,
                    outline=GRID_COLOR,
                    fill=BACKGROUND_COLOR
                )
        
        # Create score display
        self.score_text = self.game_canvas.create_text(
            10, 10,
            text="Score: 0",
            font=self.score_font,
            fill=WHITE,
            anchor=tk.NW
        )
        
        self.high_score_text = self.game_canvas.create_text(
            WIDTH - 10, 10,
            text=f"High Score: {self.high_score}",
            font=self.score_font,
            fill=GOLD,
            anchor=tk.NE
        )
        
        # Initialize game
        self.snake = [(GRID_WIDTH // 2, GRID_HEIGHT // 2)]
        self.snake_direction = (1, 0)  # (x, y) direction
        self.new_direction = (1, 0)
        self.food_position = self.create_food()
        self.score = 0
        self.game_speed = INITIAL_SPEED
        self.game_running = True
        
        # Create initial snake
        self.snake_segments = []
        for segment in self.snake:
            self.draw_snake_segment(segment, is_head=True)
        
        # Create initial food
        self.food_object = self.game_canvas.create_oval(
            self.food_position[0] * GRID_SIZE, 
            self.food_position[1] * GRID_SIZE,
            self.food_position[0] * GRID_SIZE + GRID_SIZE, 
            self.food_position[1] * GRID_SIZE + GRID_SIZE,
            fill=RED,
            outline=BLACK
        )
        
        # Register key bindings
        self.bind("<Up>", lambda e: self.change_direction(0, -1))
        self.bind("<Down>", lambda e: self.change_direction(0, 1))
        self.bind("<Left>", lambda e: self.change_direction(-1, 0))
        self.bind("<Right>", lambda e: self.change_direction(1, 0))
        
        # Start game loop
        self.update_game()
    
    def create_food(self):
        while True:
            x = random.randint(0, GRID_WIDTH - 1)
            y = random.randint(0, GRID_HEIGHT - 1)
            if (x, y) not in self.snake:
                return (x, y)
    
    def draw_snake_segment(self, position, is_head=False):
        x, y = position
        if is_head:
            color = DARK_GREEN
        else:
            color = GREEN
            
        segment = self.game_canvas.create_rectangle(
            x * GRID_SIZE, y * GRID_SIZE,
            x * GRID_SIZE + GRID_SIZE, y * GRID_SIZE + GRID_SIZE,
            fill=color,
            outline=BLACK
        )
        
        if is_head:
            # Add eyes based on direction
            eye_size = GRID_SIZE // 5
            offset = GRID_SIZE // 3
            
            # For simplicity, we'll just add two eyes regardless of direction
            eye1 = self.game_canvas.create_oval(
                x * GRID_SIZE + offset, 
                y * GRID_SIZE + offset,
                x * GRID_SIZE + offset + eye_size, 
                y * GRID_SIZE + offset + eye_size,
                fill=BLACK
            )
            
            eye2 = self.game_canvas.create_oval(
                x * GRID_SIZE + GRID_SIZE - offset - eye_size, 
                y * GRID_SIZE + offset,
                x * GRID_SIZE + GRID_SIZE - offset, 
                y * GRID_SIZE + offset + eye_size,
                fill=BLACK
            )
            
            self.snake_segments.append((segment, eye1, eye2))
        else:
            self.snake_segments.append((segment,))
    
    def change_direction(self, dx, dy):
        # Prevent 180-degree turns
        if (dx, dy) != (-self.snake_direction[0], -self.snake_direction[1]):
            self.new_direction = (dx, dy)
    
    def update_game(self):
        if not self.game_running:
            return
            
        # Update direction
        self.snake_direction = self.new_direction
        
        # Calculate new head position
        head_x, head_y = self.snake[0]
        new_x = (head_x + self.snake_direction[0]) % GRID_WIDTH
        new_y = (head_y + self.snake_direction[1]) % GRID_HEIGHT
        new_head = (new_x, new_y)
        
        # Check for collision with self
        if new_head in self.snake:
            self.game_running = False
            self.after(500, lambda: self.show_game_over_screen(self.score))
            return
        
        # Move snake
        self.snake.insert(0, new_head)
        
        # Check if food is eaten
        if new_head == self.food_position:
            # Increase score
            self.score += 10
            self.game_canvas.itemconfig(
                self.score_text,
                text=f"Score: {self.score}"
            )
            
            # Play sound
            try:
                winsound.Beep(1000, 50)
            except:
                pass
            
            # Create new food
            self.food_position = self.create_food()
            self.game_canvas.coords(
                self.food_object,
                self.food_position[0] * GRID_SIZE, 
                self.food_position[1] * GRID_SIZE,
                self.food_position[0] * GRID_SIZE + GRID_SIZE, 
                self.food_position[1] * GRID_SIZE + GRID_SIZE
            )
            
            # Increase speed
            self.game_speed = max(MIN_SPEED, self.game_speed - ACCELERATION)
        else:
            # Remove tail
            tail = self.snake.pop()
            for item in self.snake_segments.pop(0):
                self.game_canvas.delete(item)
        
        # Draw new head
        self.draw_snake_segment(new_head, is_head=True)
        
        # Schedule next update
        self.after(self.game_speed, self.update_game)

if __name__ == "__main__":
    game = SnakeGame()
    game.mainloop()
