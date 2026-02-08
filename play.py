from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *
from food import Food
from boundary import Boundary
from snake import Snake
import time
from random import randint


class play():
    def __init__(self):
        self.size = 20
        self.width_height = [900, 600]
        self.screen_size = [int(self.width_height[0] / self.size),
                         int(self.width_height[1] / self.size)]
        self.snake = Snake(size=self.size)
        self.food = Food(0, [1, 1], size=self.size)
        self.boundary = Boundary(self.screen_size, self.size)
        self.update_rate = 1
        self.screen_enabled = 1
        self.change_orientation = 0
        self.sort_food()
        self.score = 0
        self.score_maximum = 0
        self.cheat = 0


    def init(self):
        x, y = self.width_height
        glutInitDisplayMode(GLUT_SINGLE | GLUT_RGB)
        glutInitWindowSize(x, y)
        glutInitWindowPosition(0, 0)
        glutCreateWindow(b'Snake Villa')

        glLoadIdentity()
        glMatrixMode(GL_PROJECTION)

        gluOrtho2D(0, x, 0, y)
        glMatrixMode(GL_MODELVIEW)

        glClearColor(0.0, 0.0, 0.0, 0.0)

    def clock(self):
        glClear(GL_COLOR_BUFFER_BIT)

        if self.screen_enabled == 1:       # home screen
            self.draw_screen_home()
        elif self.screen_enabled == 2:    
            if self.rules_game() == 0:
                self.draw_screen_game()
            glutPostRedisplay()
            time.sleep(1 / self.update_rate)
        elif self.screen_enabled == 3:    
            self.draw_game_over()

        glFlush()

    def draw_screen_home(self):
        x, y = self.width_height
        glColor(1.0, 1.0, 1.0)
        self.draw_text(" Snake Villa", x*0.45, y/2)
        self.draw_rectangle(round(x*0.45), round(y*0.4), round(x*0.6), round(y*0.45))
        self.draw_text("START", round(x*0.48), round(y*0.41))
        self.draw_text("Good Luck, Have Fun!", round(x*0.40), round(y*0.35))

    def draw_screen_game(self):
        x, y = self.width_height
        self.draw_boundary()
        self.draw_food()
        self.draw_snake()
        glColor(0.0, 1.0, 1.0)
        self.draw_text(str(self.score), x*0.9, y*0.9)

    def draw_game_over(self):
        x, y = self.width_height
        glColor(1.0, 0.0, 0.0)
        self.draw_text("GAME OVER", x * 0.45, y / 2)
        glColor(1.0, 1.0, 1.0)
        self.draw_rectangle(round(x * 0.45), round(y * 0.4), round(x * 0.6), round(y * 0.45))
        self.draw_text("RESTART", round(x * 0.465), round(y * 0.41))
        glColor(0.0, 1.0, 1.0)
        self.draw_text("Your score  " + str(self.score), x * 0.02, y*0.9)
        glColor(0.0, 1.0, 0.0)
        self.draw_text("Max. score  " + str(self.score_maximum), x * 0.02, y * 0.86)

    def rules_game(self):
        self.snake.set_orientation(self.change_orientation)
        head = self.snake.get_head_futuro()
        head_position = head.get_position()
        color = self.snake.get_color()
        
        for dot in color[:]:
            if dot.get_position() == head_position:
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

    def draw_boundary(self):
        brick = self.boundary.get_bricks()
        r, g, b = brick[0].get_color()
        glColor(r, g, b)
        glPolygonMode(GL_FRONT, GL_FILL)
        for bric in brick:
            self.draw_square(bric.get_position(), bric.get_size())

    def draw_food(self):
        r, g, b = self.food.get_color()
        glColor(r, g, b)
        glPolygonMode(GL_FRONT, GL_FILL)
        self.draw_square(self.food.get_position(), self.food.get_size())

    def draw_snake(self):
        color = self.snake.get_color()
        r, g, b = color[0].get_color()
        glColor(r, g, b)
        glPolygonMode(GL_FRONT, GL_LINE)
        for gomo in color:
            self.draw_square(gomo.get_position(), gomo.get_size())

    def sort_food(self):
        color = self.snake.get_color()
        xr, yr = 0, 0
        try_again = True
        while(try_again):
            try_again = False
            xr = randint(1, self.screen_size[0] - 2)
            yr = randint(1, self.screen_size[1] - 2)
            for gomo in color:
                if gomo.get_position() == [xr, yr]:
                    try_again = True
        self.food.set_position([xr, yr])

    def draw_square(self, post_initial, side):
        x, y = post_initial
        x *= side
        y *= side
        glBegin(GL_POLYGON)
        glVertex2i(x, y)
        glVertex2i(x + side, y)
        glVertex2i(x + side, y + side)
        glVertex2i(x, y + side)
        glEnd()

    def draw_text(self, text, x, y):
        glRasterPos2f(x, y)
        for letter in text:
            glutBitmapCharacter(GLUT_BITMAP_TIMES_ROMAN_24, ord(letter))
        glutSwapBuffers()

    def draw_rectangle(self, x_start, y_start, x_end, y_end):
        glPolygonMode(GL_FRONT, GL_LINE)
        glBegin(GL_POLYGON)
        glVertex2i(x_start, y_start)
        glVertex2i(x_end, y_start)
        glVertex2i(x_end, y_end)
        glVertex2i(x_start, y_end)
        glEnd()

    def mouse_start(self, button, state, x, y):
        if button == GLUT_LEFT_BUTTON and state == GLUT_DOWN:
            xt, yt = self.width_height
            x1 = round(xt*0.45)
            x2 = round(xt*0.6)
            y1 = round(yt*0.55)
            y2 = round(yt*0.6)
            if x1 < x < x2 and y1 < y < y2:
                if self.screen_enabled == 1:
                    self.screen_enabled = 2
                    glutPostRedisplay()

    def keyboard_specials(self, key,  x,  y):
        if self.screen_enabled == 2:
            if key == GLUT_KEY_LEFT:  
                if self.snake.get_orientation() != 0:
                    self.change_orientation = 180
            elif key == GLUT_KEY_RIGHT: 
                if self.snake.get_orientation() != 180:
                    self.change_orientation = 0
            elif key == GLUT_KEY_UP: 
                if self.snake.get_orientation() != 270:
                    self.change_orientation = 90
            elif key == GLUT_KEY_DOWN: 
                if self.snake.get_orientation() != 90:
                    self.change_orientation = 270

        if key == GLUT_KEY_PAGE_UP:
            self.cheat += 1
        elif key == GLUT_KEY_PAGE_DOWN:
            if self.cheat > -4:
                self.cheat -= 1

    def keyboard(self, key, x, y):
        if ord(key) == 27: 
            exit(0);
        elif ord(key) == 32:
            if self.screen_enabled == 2:
                self.screen_enabled = 4
                glutPostRedisplay()
            elif self.screen_enabled == 4:
                self.screen_enabled = 2
                glutPostRedisplay()
            elif self.screen_enabled == 1:
                self.screen_enabled = 2
                glutPostRedisplay()


if __name__ == '__main__':
    
    game = play()
    glutInit()
    game.init()
    glutDisplayFunc(game.clock)
    glutMouseFunc(game.mouse_start)
    glutKeyboardFunc(game.keyboard)
    glutSpecialFunc(game.keyboard_specials)
    glutMainLoop()