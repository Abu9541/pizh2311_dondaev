import json
from OOP.Week_4.task_4_queue import Queue


class QueueCollection:
    """
    Класс-контейнер для хранения и управления набором объектов Queue.
    """

    def __init__(self, queues=None):
        """
        Инициализация контейнера.
        Принимает список объектов Queue и присваивает их полю _data.
        """
        if queues is None:
            self._data = []
        else:
            self._data = list(queues)

    def __str__(self):
        """
        Метод перегрузки класса: возвращение объекта в виде строки.
        Возвращает строковое представление контейнера.
        """
        return f"QueueCollection({[str(queue) for queue in self._data]})"

    def __getitem__(self, index):
        """
        Метод перегрузки класса: получение элемента по индексу.
        Принимает индекс возвращаемого элемента.
        """
        return self._data[index]

    def add(self, queue: Queue):
        """
        Добавляет объект Queue в контейнер.
        """
        if isinstance(queue, Queue):
            self._data.append(queue)
        else:
            raise TypeError("Можно добавлять только объекты типа Queue")

    def remove(self, index: int):
        """
        Удаляет объект Queue из контейнера по индексу.
        Принимает индекс удаляемого элемента.
        """
        if 0 <= index < len(self._data):
            self._data.pop(index)
        else:
            raise IndexError("Индекс вне диапазона")

    def save(self, filename: str):
        """
        Сохраняет контейнер в JSON-файл.
        """
        with open(filename, 'w') as f:
            json.dump([queue.items for queue in self._data], f)

    def load(self, filename: str):
        """
        Загружает контейнер из JSON-файла.
        """
        with open(filename, 'r') as f:
            data = json.load(f)
            self._data = [Queue(items) for items in data]
