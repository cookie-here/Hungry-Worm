class Object():
    
    def __init__(self, orientation, position, color, size):
        self.__orientation = orientation
        self.__position = position
        self.__color = color
        self.__size = size

    def get_orientation(self):
        return self.__orientation

    def get_position(self):
        return self.__position

    def get_color(self):
        return self.__color

    def get_size(self):
        return self.__size

    def set_orientation(self, orientation):
        self.__orientation = orientation

    def set_position(self, position):
        self.__position = position

    def set_color(self, color):
        self.__color = color

    def set_size(self, size):
        self.__size = size