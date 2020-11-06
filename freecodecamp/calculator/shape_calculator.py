import math


class Rectangle:

    def __init__(self, width, height):
        self.width = width
        self.height = height

    def set_width(self, n_width):
        self.width = n_width

    def set_height(self, n_height):
        self.height = n_height

    def get_area(self):
        return self.height * self.width

    def get_perimeter(self):
        return 2 * (self.width + self.height)

    def get_diagonal(self):
        return math.sqrt(self.width ** 2 + self.height ** 2)

    def get_picture(self):
        picture = ''
        if self.width > 50 or self.height > 50:
            return "Too big for picture."

        for i in range(self.height):
            for j in range(self.width):
                picture += "*"
            picture += "\n"
        return picture

    def get_amount_inside(self):
        pass

    def __str__(self):
        return f'Rectangle(width={self.width}, height={self.height})'


class Square(Rectangle):

    def __init__(self, side):
        Rectangle.__init__(self, side, side)
        self.side = side

    def __str__(self):
        return f'Square(side={self.side})'

    def get_area(self):
        return self.height ** 2

    def get_perimeter(self):
        return 4 * self.side

    def get_diagonal(self):
        return math.sqrt(2 * self.width ** 2)

    def set_side(self, n_side):
        self.side = n_side
        self.height = n_side
        self.width = n_side

    def set_width(self, n_width):
        self.side = n_width

    def set_height(self, n_height):
        self.side = n_height
