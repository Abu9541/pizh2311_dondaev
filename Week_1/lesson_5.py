class Table:

    def __init__(self, width, height):
        self.width = width
        self.height = height

    def __add__(self, other):
        return self.width + other.width


table_1 = Table(5, 2.5)
table_2 = Table(3, 1.5)
print(f'Длина обоих столов вместе: {table_1 + table_2} метров.')
