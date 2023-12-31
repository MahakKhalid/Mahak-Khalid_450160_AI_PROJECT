import tkinter as tk
import random

class SnakeGame:
    # Class variable for obstacles
    obstacles = [(160, 180), (40, 60)]

    def __init__(self, master):
        self.master = master
        self.master.title("Snake Game")
        self.master.geometry("400x420")
        self.master.resizable(False, False)

        self.canvas = tk.Canvas(self.master, bg="black", width=400, height=400)
        self.canvas.pack()

        self.snake = [(100, 100), (90, 100), (80, 100)]
        self.direction = "Right"

        self.food = self.create_food()

        # Two obstacles: one near the middle and another near the top-left corner
        for obstacle in self.obstacles:
            x, y = obstacle
            self.canvas.create_rectangle(x, y, x + 20, y + 20, fill="yellow", tags="obstacle")

        
        # Draw blue boundaries on the canvas
        self.canvas.create_line(0, 0, 400, 0, width=8, fill="blue")  # Top boundary
        self.canvas.create_line(0, 0, 0, 400, width=8, fill="blue")  # Left boundary
        self.canvas.create_line(400, 0, 400, 400, width=8, fill="blue")  # Right boundary
        self.canvas.create_line(0, 400, 400, 400, width=8, fill="blue")  # Bottom boundary

        self.score = 3  # Initial snake length

        # Create score labels
        self.score_label = tk.Label(self.master, text=f"Snake Length: {self.score}", fg="black", font=("Helvetica", 8))
        self.score_label.place(x=150, y=400)

        self.master.bind("<KeyPress>", self.change_direction)

        self.update()

    def create_food(self):
        while True:
            x = random.randint(0, 19) * 20
            y = random.randint(0, 19) * 20
            food_coords = (x, y)

            # Check if food_coords collide with any obstacle
            obstacle_collision = any(food_coords == obstacle for obstacle in self.obstacles)

            if not obstacle_collision:
                break

        food = self.canvas.create_rectangle(x, y, x + 20, y + 20, fill="red")
        return food

    def move_snake(self):
        head = self.snake[0]
        if self.direction == "Right":
            new_head = (head[0] + 20, head[1])
        elif self.direction == "Left":
            new_head = (head[0] - 20, head[1])
        elif self.direction == "Up":
            new_head = (head[0], head[1] - 20)
        elif self.direction == "Down":
            new_head = (head[0], head[1] + 20)

        # Check for boundaries
        if not (0 <= new_head[0] < 400 and 0 <= new_head[1] < 400):
            # Snake hit the boundaries, close the canvas
            self.reset_game("Boundaries")
            return

        # Check for self-collision
        if new_head in self.snake:
            # Snake collided with itself, close the canvas
            self.reset_game("Self-Collision")
            return

        # Check for obstacles
        for obstacle in self.obstacles:
            x, y = obstacle
            if new_head == obstacle:
                # Snake collided with an obstacle, close the canvas
                self.reset_game("Obstacle Collision")
                return

        self.snake.insert(0, new_head)

        # Check for food collision
        food_coords = self.canvas.coords(self.food)
        if head[0] == food_coords[0] and head[1] == food_coords[1]:
            self.snake.append((0, 0))  # Just to increase the length
            self.canvas.delete(self.food)
            self.food = self.create_food()
            self.score += 1
            self.update_score()

        # Remove the last element to keep the snake length constant
        self.snake = self.snake[:len(self.snake) - 1]

    def update(self):
        # Check if the canvas is still available
        if not hasattr(self, 'canvas') or not self.canvas.winfo_exists():
            return

        head = self.snake[0]

        self.move_snake()

        # Check if the canvas is still available after moving the snake
        if not hasattr(self, 'canvas') or not self.canvas.winfo_exists():
            return

        self.canvas.delete("snake")
        for segment in self.snake:
            self.canvas.create_rectangle(segment[0], segment[1], segment[0] + 20, segment[1] + 20, fill="green", tags="snake")

        self.master.after(200, self.update)

    def update_score(self):
        self.score_label.config(text=f"Snake Length: {self.score}")

    def change_direction(self, event):
        if event.keysym == "Right" and not self.direction == "Left":
            self.direction = "Right"
        elif event.keysym == "Left" and not self.direction == "Right":
            self.direction = "Left"
        elif event.keysym == "Up" and not self.direction == "Down":
            self.direction = "Up"
        elif event.keysym == "Down" and not self.direction == "Up":
            self.direction = "Down"

    def reset_game(self, collision_type):
        # Print a message indicating the collision type
        print(f"Collision occurred: {collision_type}")

        # Close the canvas when a collision happens
        self.master.destroy()

if __name__ == "__main__":
    root = tk.Tk()
    game = SnakeGame(root)
    root.mainloop()
