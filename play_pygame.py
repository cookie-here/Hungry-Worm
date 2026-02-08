import pygame
import sys
from food import Food
from boundary import Boundary
from snake import Snake
import time
from random import randint


class PlayPygame:
    def __init__(self):
        pygame.init()
        self.size = 20
        self.width_height = [900, 600]
        self.screen_size = [int(self.width_height[0] / self.size),
                           int(self.width_height[1] / self.size)]
        self.screen = pygame.display.set_mode(self.width_height)
        pygame.display.set_caption('Hungry Worm')
        
        self.snake = Snake(size=self.size)
        self.food = Food(0, [1, 1], size=self.size)
        self.boundary = Boundary(self.screen_size, self.size)
        self.update_rate = 5
        self.screen_enabled = 1  # 1=home, 2=game, 3=game over
        self.change_orientation = 0
        self.sort_food()
        self.score = 0
        self.score_maximum = 0
        self.cheat = 0
        self.clock = pygame.time.Clock()
        
        # Colors
        self.BLACK = (0, 0, 0)
        self.WHITE = (255, 255, 255)
        self.RED = (255, 0, 0)
        self.GREEN = (0, 255, 0)
        self.CYAN = (0, 255, 255)
        
    def draw_text_centered(self, text, center_x, center_y, color=(255, 255, 255), size=24):
        font = pygame.font.Font(None, size)
        text_surface = font.render(text, True, color)
        text_rect = text_surface.get_rect(center=(center_x, center_y))
        self.screen.blit(text_surface, text_rect)
        
    def draw_text(self, text, x, y, color=(255, 255, 255), size=24):
        font = pygame.font.Font(None, size)
        text_surface = font.render(text, True, color)
        self.screen.blit(text_surface, (x, y))
        
    def draw_button(self, text, center_x, center_y, width, height, color=(255, 255, 255), text_size=32):
        rect = pygame.Rect(center_x - width // 2, center_y - height // 2, width, height)
        pygame.draw.rect(self.screen, color, rect, 2)
        self.draw_text_centered(text, center_x, center_y, color, text_size)
        return rect
        
    def draw_rectangle(self, x_start, y_start, x_end, y_end, color=(255, 255, 255), filled=False):
        rect = pygame.Rect(x_start, y_start, x_end - x_start, y_end - y_start)
        if filled:
            pygame.draw.rect(self.screen, color, rect)
        else:
            pygame.draw.rect(self.screen, color, rect, 2)
            
    def draw_square(self, position, side, color, filled=True):
        x, y = position
        x *= side
        y *= side
        y = self.width_height[1] - y - side  # Flip Y coordinate
        rect = pygame.Rect(x, y, side, side)
        if filled:
            pygame.draw.rect(self.screen, color, rect)
        else:
            pygame.draw.rect(self.screen, color, rect, 2)
            
    def color_to_rgb(self, r, g, b):
        return (int(r * 255), int(g * 255), int(b * 255))
        
    def draw_screen_home(self):
        x, y = self.width_height
        center_x = x // 2
        center_y = y // 2
        
        # Title
        self.draw_text_centered("Hungry Worm", center_x, center_y - 80, self.WHITE, 64)
        
        # Start button
        self.start_button = self.draw_button("START", center_x, center_y, 180, 50, self.WHITE, 36)
        
        # Instructions
        self.draw_text_centered("Good Luck, Have Fun!", center_x, center_y + 70, self.WHITE, 28)
        self.draw_text_centered("Use Arrow Keys to Move", center_x, center_y + 120, self.CYAN, 24)
        
    def draw_screen_game(self):
        x, y = self.width_height
        self.draw_boundary()
        self.draw_food()
        self.draw_snake()
        self.draw_text(f"Score: {self.score}", int(x * 0.82), 20, self.CYAN, 32)
        
    def draw_game_over(self):
        x, y = self.width_height
        center_x = x // 2
        center_y = y // 2
        
        # Game Over title
        self.draw_text_centered("GAME OVER", center_x, center_y - 60, self.RED, 64)
        
        # Restart button
        self.restart_button = self.draw_button("RESTART", center_x, center_y + 20, 180, 50, self.WHITE, 36)
        
        # Scores
        self.draw_text(f"Your score: {self.score}", 20, 30, self.CYAN, 28)
        self.draw_text(f"Max score: {self.score_maximum}", 20, 60, self.GREEN, 28)
        
    def draw_boundary(self):
        bricks = self.boundary.get_bricks()
        if bricks:
            r, g, b = bricks[0].get_color()
            color = self.color_to_rgb(r, g, b)
            for brick in bricks:
                self.draw_square(brick.get_position(), brick.get_size(), color)
                
    def draw_food(self):
        r, g, b = self.food.get_color()
        color = self.color_to_rgb(r, g, b)
        self.draw_square(self.food.get_position(), self.food.get_size(), color)
        
    def draw_snake(self):
        snake_parts = self.snake.get_color()
        if snake_parts:
            r, g, b = snake_parts[0].get_color()
            color = self.color_to_rgb(r, g, b)
            for part in snake_parts:
                self.draw_square(part.get_position(), part.get_size(), color, filled=False)
                
    def sort_food(self):
        snake_parts = self.snake.get_color()
        xr, yr = 0, 0
        try_again = True
        while try_again:
            try_again = False
            xr = randint(1, self.screen_size[0] - 2)
            yr = randint(1, self.screen_size[1] - 2)
            for part in snake_parts:
                if part.get_position() == [xr, yr]:
                    try_again = True
        self.food.set_position([xr, yr])
        
    def rules_game(self):
        self.snake.set_orientation(self.change_orientation)
        head = self.snake.get_head_futuro()
        head_position = head.get_position()
        snake_parts = self.snake.get_color()
        
        for part in snake_parts:
            if part.get_position() == head_position:
                self.screen_enabled = 3
                return 1
                
        self.snake.move()
        
        if self.boundary.check_collision(head_position):
            self.screen_enabled = 3
            return 1
            
        if self.food.get_position() == head_position:
            self.snake.inlarge(self.food.get_position())
            self.sort_food()
            self.score += 10
            if self.score > self.score_maximum:
                self.score_maximum = self.score
                
        self.update_rate = self.cheat + 5 + self.score / 50
        return 0
        
    def handle_mouse_click(self, pos):
        x, y = pos
        xt, yt = self.width_height
        center_x = xt // 2
        center_y = yt // 2
        
        # Button dimensions
        btn_width = 180
        btn_height = 50
        
        if self.screen_enabled == 1:
            # Start button area
            btn_y = center_y
            if (center_x - btn_width // 2 < x < center_x + btn_width // 2 and
                btn_y - btn_height // 2 < y < btn_y + btn_height // 2):
                self.screen_enabled = 2
        elif self.screen_enabled == 3:
            # Restart button area
            btn_y = center_y + 20
            if (center_x - btn_width // 2 < x < center_x + btn_width // 2 and
                btn_y - btn_height // 2 < y < btn_y + btn_height // 2):
                # Restart game
                self.snake = Snake(size=self.size)
                self.food = Food(0, [1, 1], size=self.size)
                self.sort_food()
                self.score = 0
                self.screen_enabled = 2
                self.change_orientation = 0
                
    def handle_keyboard(self, key):
        if self.screen_enabled == 2:
            if key == pygame.K_LEFT or key == pygame.K_a:
                if self.snake.get_orientation() != 0:
                    self.change_orientation = 180
            elif key == pygame.K_RIGHT or key == pygame.K_d:
                if self.snake.get_orientation() != 180:
                    self.change_orientation = 0
            elif key == pygame.K_UP or key == pygame.K_w:
                if self.snake.get_orientation() != 270:
                    self.change_orientation = 90
            elif key == pygame.K_DOWN or key == pygame.K_s:
                if self.snake.get_orientation() != 90:
                    self.change_orientation = 270
                    
        if key == pygame.K_PAGEUP:
            self.cheat += 1
        elif key == pygame.K_PAGEDOWN:
            if self.cheat > -4:
                self.cheat -= 1
        elif key == pygame.K_SPACE:
            if self.screen_enabled == 1:
                self.screen_enabled = 2
                
    def run(self):
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        running = False
                    else:
                        self.handle_keyboard(event.key)
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1:  # Left click
                        self.handle_mouse_click(event.pos)
                        
            self.screen.fill(self.BLACK)
            
            if self.screen_enabled == 1:
                self.draw_screen_home()
            elif self.screen_enabled == 2:
                if self.rules_game() == 0:
                    self.draw_screen_game()
            elif self.screen_enabled == 3:
                self.draw_game_over()
                
            pygame.display.flip()
            self.clock.tick(int(self.update_rate))
            
        pygame.quit()
        sys.exit()


if __name__ == '__main__':
    game = PlayPygame()
    game.run()