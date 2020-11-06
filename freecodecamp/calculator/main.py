from unittest import main

from freecodecamp.calculator import shape_calculator

if __name__ == "__main__":
    rect = shape_calculator.Rectangle(5, 10)
    print(rect.get_area())
    rect.set_width(3)
    print(rect.get_perimeter())
    print(rect)

    sq = shape_calculator.Square(9)
    print(sq.get_area())
    sq.set_side(4)
    print(sq.get_diagonal())
    print(sq)
    main(module='test_module', exit=False)