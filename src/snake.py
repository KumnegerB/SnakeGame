import pygame
import random
import sys

WINDOW_WIDTH = 640
WINDOW_HEIGHT = 480
GRID_SIZE = 20
GRID_WIDTH = WINDOW_WIDTH // GRID_SIZE
GRID_HEIGHT = WINDOW_HEIGHT // GRID_SIZE
BACKGROUND_COLOR = (18, 18, 18)
SNAKE_COLOR = (0, 200, 90)
SNAKE_HEAD_COLOR = (0, 230, 120)
FOOD_COLOR = (230, 60, 60)
TEXT_COLOR = (240, 240, 240)
PAUSE_OVERLAY = (0, 0, 0, 140)
INITIAL_SPEED = 10
SPEED_INCREMENT_FOOD = 5
MAX_SPEED = 18

UP = (0, -1)
DOWN = (0, 1)
LEFT = (-1, 0)
RIGHT = (1, 0)

class Snake:
    def __init__(self):
        self.positions = [(GRID_WIDTH // 2, GRID_HEIGHT // 2)]
        self.direction = random.choice([UP, DOWN, LEFT, RIGHT])
        self.pending_growth = 0

    def head(self):
        return self.positions[0]

    def turn(self, dir_vec):
        if (dir_vec[0] == -self.direction[0] and dir_vec[1] == -self.direction[1]):
            return
        self.direction = dir_vec

    def move(self):
        cur = self.head()
        new = ((cur[0] + self.direction[0]) % GRID_WIDTH, (cur[1] + self.direction[1]) % GRID_HEIGHT)
        self.positions.insert(0, new)
        if self.pending_growth > 0:
            self.pending_growth -= 1
        else:
            self.positions.pop()

    def grow(self, amount=1):
        self.pending_growth += amount

    def collides_with_self(self):
        return self.head() in self.positions[1:]

class Food:
    def __init__(self, snake_positions):
        self.position = self.random_position(snake_positions)

    def random_position(self, snake_positions):
        while True:
            pos = (random.randint(0, GRID_WIDTH - 1), random.randint(0, GRID_HEIGHT - 1))
            if pos not in snake_positions:
                return pos

class Game:
    def __init__(self):
        pygame.init()
        pygame.display.set_caption("Snake")
        self.surface = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
        self.clock = pygame.time.Clock()
        self.font = pygame.font.SysFont("consolas", 20)
        self.big_font = pygame.font.SysFont("consolas", 34, bold=True)
        self.reset()

    def reset(self):
        self.snake = Snake()
        self.food = Food(self.snake.positions)
        self.score = 0
        self.speed = INITIAL_SPEED
        self.paused = False
        self.game_over = False

    def draw_cell(self, position, color):
        x = position[0] * GRID_SIZE
        y = position[1] * GRID_SIZE
        rect = pygame.Rect(x, y, GRID_SIZE, GRID_SIZE)
        pygame.draw.rect(self.surface, color, rect)

    def draw_grid(self):
        self.surface.fill(BACKGROUND_COLOR)

    def draw_snake(self):
        if self.snake.positions:
            self.draw_cell(self.snake.positions[0], SNAKE_HEAD_COLOR)
        for pos in self.snake.positions[1:]:
            self.draw_cell(pos, SNAKE_COLOR)

    def draw_food(self):
        self.draw_cell(self.food.position, FOOD_COLOR)

    def draw_hud(self):
        text = self.font.render(f"Score: {self.score}  Speed: {self.speed}", True, TEXT_COLOR)
        self.surface.blit(text, (10, 8))
        if self.paused and not self.game_over:
            overlay = pygame.Surface((WINDOW_WIDTH, WINDOW_HEIGHT), pygame.SRCALPHA)
            overlay.fill(PAUSE_OVERLAY)
            self.surface.blit(overlay, (0, 0))
            msg = self.big_font.render("Paused - Press P", True, TEXT_COLOR)
            rect = msg.get_rect(center=(WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2))
            self.surface.blit(msg, rect)

        if self.game_over:
            overlay = pygame.Surface((WINDOW_WIDTH, WINDOW_HEIGHT), pygame.SRCALPHA)
            overlay.fill(PAUSE_OVERLAY)
            self.surface.blit(overlay, (0, 0))
            msg1 = self.big_font.render("Game Over", True, TEXT_COLOR)
            msg2 = self.font.render("Press Space to restart or Esc to quit", True, TEXT_COLOR)
            r1 = msg1.get_rect(center=(WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2 - 20))
            r2 = msg2.get_rect(center=(WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2 + 20))
            self.surface.blit(msg1, r1)
            self.surface.blit(msg2, r2)

    def spawn_food(self):
        self.food = Food(self.snake.positions)

    def increase_speed(self):
        self.speed = min(MAX_SPEED, INITIAL_SPEED + (self.score // SPEED_INCREMENT_FOOD))

    def handle_input(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit(0)
            if event.type == pygame.KEYDOWN:
                if event.key in (pygame.K_ESCAPE,):
                    pygame.quit()
                    sys.exit(0)
                if event.key in (pygame.K_p,):
                    if not self.game_over:
                        self.paused = not self.paused
                if event.key in (pygame.K_SPACE,) and self.game_over:
                    self.reset()
                if event.key in (pygame.K_UP, pygame.K_w):
                    self.snake.turn(UP)
                elif event.key in (pygame.K_DOWN, pygame.K_s):
                    self.snake.turn(DOWN)
                elif event.key in (pygame.K_LEFT, pygame.K_a):
                    self.snake.turn(LEFT)
                elif event.key in (pygame.K_RIGHT, pygame.K_d):
                    self.snake.turn(RIGHT)

    def update(self):
        if self.paused or self.game_over:
            return
        self.snake.move()
        if self.snake.collides_with_self():
            self.game_over = True
            return
        if self.snake.head() == self.food.position:
            self.score += 1
            self.snake.grow(1)
            self.spawn_food()
            self.increase_speed()

    def render(self):
        self.draw_grid()
        self.draw_food()
        self.draw_snake()
        self.draw_hud()
        pygame.display.flip()

    def run(self):
        while True:
            self.clock.tick(self.speed)
            self.handle_input()
            self.update()
            self.render()

if __name__ == "__main__":
    Game().run()
