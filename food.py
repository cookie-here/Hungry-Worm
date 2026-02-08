import colors as Colors
from object import Object

class Food(Object):
    def __init__(self, orientation=0, position=[1, 1], color=Colors.red, size=30 ):
        super().__init__(orientation, position, color, size)