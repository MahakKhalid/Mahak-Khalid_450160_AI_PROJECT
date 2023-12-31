import tkinter as tk
import random
import time

class SnakeGame:
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

        self.enemy_snake = [(300, 300), (310, 300), (320, 300)]
        self.enemy_direction = "Left"

        self.food = self.create_food()

        for obstacle in self.obstacles:
            x, y = obstacle
            self.canvas.create_rectangle(x, y, x + 20, y + 20, fill="yellow", tags="obstacle")

        self.canvas.create_line(0, 0, 400, 0, width=8, fill="blue")  # Top boundary
        self.canvas.create_line(0, 0, 0, 400, width=8, fill="blue")  # Left boundary
        self.canvas.create_line(400, 0, 400, 400, width=8, fill="blue")  # Right boundary
        self.canvas.create_line(0, 400, 400, 400, width=8, fill="blue")  # Bottom boundary

        self.player_score = 0
        self.enemy_score = 0

        self.score_label = tk.Label(self.master, text=f"Player Score: {self.player_score}  Enemy Score: {self.enemy_score}",
                                    fg="black", font=("Helvetica", 8))
        self.score_label.place(x=150, y=400)

        self.end_time = time.time() + 60  # 60 seconds for the competition

        self.master.bind("<KeyPress>", self.change_direction)

        self.update()

    def create_food(self):
        while True:
            x = random.randint(0, 19) * 20
            y = random.randint(0, 19) * 20
            food_coords = (x, y)

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

        if not (0 <= new_head[0] < 400 and 0 <= new_head[1] < 400):
            self.reset_game("Boundaries")
            return

        if new_head in self.snake or new_head in self.enemy_snake:
            self.reset_game("Self-Collision")
            return

        for obstacle in self.obstacles:
            x, y = obstacle
            if new_head == obstacle:
                self.reset_game("Obstacle Collision")
                return

        self.snake.insert(0, new_head)

        food_coords = self.canvas.coords(self.food)
        if head[0] == food_coords[0] and head[1] == food_coords[1]:
            self.snake.append((0, 0))
            self.canvas.delete(self.food)
            self.food = self.create_food()
            self.player_score += 1
            self.update_score()

        self.snake = self.snake[:len(self.snake) - 1]

    def move_enemy_snake(self):
        enemy_head = self.enemy_snake[0]
        valid_directions = self.get_valid_directions(enemy_head)
        distances = {
            'Right': self.calculate_distance(self.calculate_next_head_coordinates(enemy_head, 'Right'),
                                             self.canvas.coords(self.food)),
            'Left': self.calculate_distance(self.calculate_next_head_coordinates(enemy_head, 'Left'),
                                            self.canvas.coords(self.food)),
            'Up': self.calculate_distance(self.calculate_next_head_coordinates(enemy_head, 'Up'),
                                          self.canvas.coords(self.food)),
            'Down': self.calculate_distance(self.calculate_next_head_coordinates(enemy_head, 'Down'),
                                            self.canvas.coords(self.food)),
            'food': self.calculate_distance(enemy_head, self.canvas.coords(self.food))
        }

        if distances.get('food') is not None:
            distances['Left'] = 0  # Add 'Left' with a default distance value (0) if it doesn't exist

            best_direction = min(valid_directions, key=lambda direction: distances[direction])
            new_head = self.calculate_next_head_coordinates(enemy_head, best_direction)
            self.enemy_snake.insert(0, new_head)

            food_coords = self.canvas.coords(self.food)
            if enemy_head[0] == food_coords[0] and enemy_head[1] == food_coords[1]:
                self.enemy_snake.append((0, 0))
                self.canvas.delete(self.food)
                self.food = self.create_food()
                self.enemy_score += 1
                self.update_score()

            self.enemy_snake = self.enemy_snake[:len(self.enemy_snake) - 1]

    def update(self):
        if time.time() < self.end_time:
            if not hasattr(self, 'canvas') or not self.canvas.winfo_exists():
                return

            self.move_snake()
            self.move_enemy_snake()

            if not hasattr(self, 'canvas') or not self.canvas.winfo_exists():
                return

            self.canvas.delete("snake")
            for segment in self.snake:
                self.canvas.create_rectangle(segment[0], segment[1], segment[0] + 20, segment[1] + 20,
                                             fill="green", tags="snake")

            self.canvas.delete("enemy_snake")
            for segment in self.enemy_snake:
                self.canvas.create_rectangle(segment[0], segment[1], segment[0] + 20, segment[1] + 20,
                                             fill="orange", tags="enemy_snake")

            self.master.after(200, self.update)
        else:
            self.declare_winner()

    def declare_winner(self):
        if self.player_score > self.enemy_score:
            print("Player wins!")
        elif self.player_score < self.enemy_score:
            print("Enemy wins!")
        else:
            print("It's a tie!")

    def update_score(self):
        self.score_label.config(text=f"Player Score: {self.player_score}  Enemy Score: {self.enemy_score}")

    def change_direction(self, event):
        if event.keysym == "Right" and not self.direction == "Left":
            self.direction = "Right"
        elif event.keysym == "Left" and not self.direction == "Right":
            self.direction = "Left"
        elif event.keysym == "Up" and not self.direction == "Down":
            self.direction = "Up"
        elif event.keysym == "Down" and not self.direction == "Up":
            self.direction = "Down"

    def calculate_distance(self, point1, point2):
        return abs(point1[0] - point2[0]) + abs(point1[1] - point2[1])

    def calculate_next_head_coordinates(self, head, direction):
        if direction == "Right":
            return head[0] + 20, head[1]
        elif direction == "Left":
            return head[0] - 20, head[1]
        elif direction == "Up":
            return head[0], head[1] - 20
        elif direction == "Down":
            return head[0], head[1] + 20

    def get_valid_directions(self, head):
        valid_directions = ["Right", "Left", "Up", "Down"]
        invalid_directions = []
        for direction in valid_directions:
            next_head = self.calculate_next_head_coordinates(head, direction)
            if not (0 <= next_head[0] < 400 and 0 <= next_head[1] < 400) or next_head in self.snake \
                    or next_head in self.enemy_snake or next_head in self.obstacles:
                invalid_directions.append(direction)

        for direction in invalid_directions:
            valid_directions.remove(direction)

        return valid_directions

    def reset_game(self, collision_type):
        print(f"Collision occurred: {collision_type}")
        self.master.destroy()


if __name__ == "__main__":
    root = tk.Tk()
    game = SnakeGame(root)
    root.mainloop()
