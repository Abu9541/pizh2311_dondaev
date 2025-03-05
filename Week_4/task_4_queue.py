import json


class Queue:
    """
    Класс, представляющий очередь Queue (FIFO).
    """

    def __init__(self, items: list = None):
        """
        Инициализация очереди.
        Принимает список значений очереди.
        """
        if items is None:
            self.items = []
        else:
            self.items = list(items)

    def __str__(self):
        """
        Метод перегрузки класса.
        Возвращает строковое представление очереди.
        """
        return f"Queue({self.items})"

    def __len__(self):
        """
        Метод перегрузки класса.
        Возвращает количество элементов в очереди.
        """
        return len(self.items)

    def enqueue(self, item):
        """
        Добавляет элемент в конец очереди.
        Принимает элемент, который необходимо добавить.
        """
        self.items.append(item)

    def dequeue(self):
        """
        Удаляет и возвращает элемент из начала очереди.
        """
        if self.is_empty():
            raise IndexError("Очередь пуста")
        return self.items.pop(0)

    def is_empty(self):
        """
        Проверяет, пуста ли очередь.
        Возвращает значение логического выражения.
        """
        return len(self.items) == 0

    def peek(self):
        """
        Возвращает элемент из начала очереди без его удаления.
        """
        if self.is_empty():
            raise IndexError("Очередь пуста")
        return self.items[0]

    def save(self, filename: str):
        """
        Сохраняет очередь в JSON-файл.
        Принимает название файла, в который необходимо загрузить очередь.
        """
        with open(filename, 'w') as f:
            json.dump(self.items, f)

    @classmethod
    def from_string(cls, str_value: str):
        """
        Создает очередь из строки.
        Принимает строку и на ее основании возвращает объект класса Queue.
        """
        items = str_value.strip('[]').split(',')
        items = [item.strip() for item in items]
        return cls(items)

    def load(self, filename: str):
        """
        Загружает очередь из JSON-файла.
        Принимает название файла, из которого необходимо загрузить очередь.
        """
        with open(filename, 'r') as f:
            self.items = json.load(f)

    def __add__(self, other):
        """
        Метод перегрузки классов: сложение.
        Добавляет к каждому элементу очереди значение other.
        Возвращает измененную очередь.
        """
        try:
            sum_queue = [(self.items[i] + other) for i in range(len(self))]
            return Queue(sum_queue)
        except TypeError:
            print('Невозможно сложить!')

    def __sub__(self, other):
        """
        Метод перегрузки классов: вычитание.
        Вычитает от каждого элемента очереди значение other.
        Возвращает измененную очередь.
        """
        try:
            sum_queue = [(self.items[i] - other) for i in range(len(self))]
            return Queue(sum_queue)
        except TypeError:
            print('Невозможно вычесть!')

    def __mul__(self, other):
        """
        Метод перегрузки классов: умножение.
        Умножает каждый элемент очереди на значение other.
        Возвращает измененную очередь.
        """
        try:
            sum_queue = [(self.items[i] * other) for i in range(len(self))]
            return Queue(sum_queue)
        except TypeError:
            print('Невозможно умножить!')

    def __truediv__(self, other):
        """
        Метод перегрузки классов: деление.
        Делит каждый элемент очереди на значение other.
        Возвращает измененную очередь.
        """
        try:
            sum_queue = [(self.items[i] / other) for i in range(len(self))]
            return Queue(sum_queue)
        except TypeError:
            print('Невозможно делить!')
