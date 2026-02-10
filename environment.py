import pygame
import random
from utils import *

class Board:
    """
    Represent the game board, including the snake, 
    food, and obstacles. Handles game logic such as movement, 
    collision detection, and state updates.
    """
    def __init__(self, visual=True):
        """init the board with the snake, food, and obstacles"""
        self.visual = visual
        self.width = GRID_SIZE
        self.height = GRID_SIZE

        if self.visual:
            pygame.init()
            self.screen = pygame.display.set_mode((WINDOW_SIZE, WINDOW_SIZE))
            pygame.display.set_caption("Learn2Slither")
            self.clock = pygame.time.Clock()
            self.font = pygame.font.SysFont(None, 24)
        self.reset()

    def reset(self):
        """reset the game state to the initial configuration"""
        self.snake = [(5,5), (5,6), (5,7)]
        self.direction = UP
        self.green_apple = []
        self.red_apple = []
        self._spawn_food()
        self.score = 0
        self.steps = 0
        return self.get_state()
    
    def _spawn_food(self):
        """spawn green and red apples at random positions on the board"""
        while len(self.green_apple) < 2:
            pos = (random.randint(0, self.width-1), random.randint(0, self.height-1))
            if pos not in self.snake and pos not in self.red_apple and pos not in self.green_apple:
                self.green_apple.append(pos)
        while len(self.red_apple) < 1:
            pos = (random.randint(0, self.width-1), random.randint(0, self.height-1))
            if pos not in self.snake and pos not in self.green_apple and pos not in self.red_apple:
                self.red_apple.append(pos)
    
    def get_state(self, red_apple=False):
        """return the current state of the board as a 2D array"""
        if red_apple:
            return tuple()
        head_x, head_y = self.snake[0]
        vision = []

        check_points = [
            (head_x, head_y - 1),  # UP
            (head_x + 1, head_y),  # RIGHT
            (head_x, head_y + 1),  # DOWN
            (head_x - 1, head_y)   # LEFT
        ]

        for x, y in check_points:
            if x < 0 or x >= GRID_SIZE or y < 0 or y >= GRID_SIZE:
                vision.append(WALL)
            elif (x, y) in self.snake:
                vision.append(BODY)
            elif (x, y) in self.green_apple:
                vision.append(GREEN_APPLE)
            elif (x, y) in self.red_apple:
                vision.append(RED_APPLE)
            else:
                vision.append(EMPTY)
        return tuple(vision)
    
    def step(self, action):
        """update the game state based on the action taken by the agent"""
        self.steps += 1
        if (action == UP and self.direction == DOWN) or \
           (action == DOWN and self.direction == UP) or \
           (action == LEFT and self.direction == RIGHT) or \
           (action == RIGHT and self.direction == LEFT):
            action = self.direction  # Ignore the action that would reverse the snake
        self.direction = action
        head_x, head_y = self.snake[0]
        dx, dy = 0, 0
        if action == UP:
            dy = -1
        elif action == RIGHT:
            dx = 1
        elif action == DOWN:
            dy = 1
        elif action == LEFT:
            dx = -1
        
        new_head = (head_x + dx, head_y + dy)

        reward = -0.1 # Small negative reward for each step to encourage shorter paths
        done = False

        #wall collision
        if new_head[0] < 0 or new_head[0] >= GRID_SIZE or new_head[1] < 0 or new_head[1] >= GRID_SIZE:
            return self.get_state(), -100, True, self.score
        #self collision
        if new_head in self.snake[:-1]:
            return self.get_state(), -100, True, self.score
        
        self.snake.insert(0, new_head)

        if new_head in self.green_apple:
            reward = 10
            self.score += 1
            self.green_apple.remove(new_head)
            self._spawn_food()
        elif new_head in self.red_apple:
            reward = -10
            self.score -=1
            self.red_apple.remove(new_head)
            self.snake.pop()
            if len(self.snake) > 0:
                self.snake.pop()
            if len(self.snake) == 0:
                return self.get_state(True), -100, True, self.score
            
            self._spawn_food()
        else:
            self.snake.pop()
        
        if self.steps > 500:
            done = True
        
        return self.get_state(), reward, done, self.score
    
    def render(self):
        """render the current state of the board using Pygame"""
        if not self.visual:
            return
        
        self.screen.fill(WHITE)

        for x in range(self.width):
            for y in range(self.height):
                rect = pygame.Rect(x * CELL_SIZE, y * CELL_SIZE, CELL_SIZE, CELL_SIZE)
                if (x, y) in self.snake:
                    pygame.draw.rect(self.screen, BLUE, rect)
                elif (x, y) in self.green_apple:
                    pygame.draw.rect(self.screen, GREEN, rect)
                elif (x, y) in self.red_apple:
                    pygame.draw.rect(self.screen, RED, rect)
                else:
                    pygame.draw.rect(self.screen, GRAY, rect, 1)

        score_text = self.font.render(f'Score: {self.score}', True, BLACK)
        self.screen.blit(score_text, (10, 10))

        pygame.display.flip()
        self.clock.tick(10)
