from OOP.Week_4.task_4_queue import Queue
from task_5_queue_collection import QueueCollection


if __name__ == "__main__":
    # Создание нескольких очередей
    q1 = Queue([1, 2, 3])
    q2 = Queue([4, 5, 6])
    q3 = Queue([7, 8, 9])

    # Создание контейнера и добавление очередей
    collection = QueueCollection()
    collection.add(q1)
    collection.add(q2)
    collection.add(q3)
    print("Контейнер после добавления очередей:", collection)

    # Индексация
    print("Первая очередь в контейнере:", collection[0])
    print("Последняя очередь в контейнере:", collection[-1])

    # Удаление очереди
    collection.remove(1)
    print("Контейнер после удаления второй очереди:", collection)

    # Сохранение и загрузка контейнера
    collection.save("queue_collection.json")
    print("Контейнер сохранен в файл queue_collection.json")

    new_collection = QueueCollection()
    new_collection.load("queue_collection.json")
    print("Контейнер загружен из файла:", new_collection)
