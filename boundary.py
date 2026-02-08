from object import Object
import colors as Colors

class Boundary():
    def __init__(self, canvas_size, size=30):
        [xscreen, yscreen] = canvas_size
        self.__brick = []
        self.__color_brick = Colors.midnight_blue
        for x in range(xscreen):
            self.__brick.append(Object(0, [x, 0], self.__color_brick, size))
            self.__brick.append(Object(0, [x, yscreen - 1], Colors.green, size))
        for y in range(yscreen):
            self.__brick.append((Object(0, [0, y], self.__color_brick, size)))
            self.__brick.append((Object(0, [xscreen - 1, y], Colors.green, size)))

    def check_collision(self, position):
        for bric in self.__brick:
            if bric.get_position() == position:
                return True

        return False

    def get_bricks(self):
        return self.__brick