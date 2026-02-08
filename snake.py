import colors as Colors
from object import Object
import math

class Snake():
    def __init__(self, initial_position=[10,10], color=Colors.yellow, initial_size=3, size=30):
        x_initial, y_initial = initial_position
        self.__color_profile = [Object(0, [x, y_initial], color, size) for x in range(x_initial, x_initial + initial_size)]
        self.__color = color
        self.__size = size
        self.eat = 0

    def get_color(self):
        return self.__color_profile
    def get_head(self):
        return self.__color_profile[-1]
    def get_rabo(self):
        return self.__color_profile[0]
    def get_orientation(self):
        return self.get_head().get_orientation()
    def get_head_futuro(self):
        head = self.get_head()
        x = int(math.cos(math.radians(head.get_orientation())))
        y = int(math.sin(math.radians(head.get_orientation())))
        xc, yc = head.get_position()
        return Object(head.get_orientation(), [xc+x, yc+y], self.__color, self.__size) 
    def set_orientation(self, orientation):
        self.__color_profile[-1].set_orientation(orientation)
    def move(self):
        # creating new square (head):
        head = self.get_head()
        x = int(math.cos(math.radians(head.get_orientation())))
        y = int(math.sin(math.radians(head.get_orientation())))
        xc, yc = head.get_position()
        self.__color_profile.append(Object(head.get_orientation(), [xc+x, yc+y], self.__color, self.__size))

        if self.eat:
            self.eat = 0
        else:
            del self.__color_profile[0]
    def inlarge(self, ponto):
        self.eat = 1