from task_6_transport import Transport, WaterTransport, WheeledTransport, Car

if __name__ == "__main__":
    # Создание объектов
    boat = WaterTransport("Лодка", 50, 2010, 2)
    bicycle = WheeledTransport("Велосипед", 20, 2021, 2)
    car = Car("Автомобиль", 120, 2024, 4, "Toyota")

    # Демонстрация работы методов
    boat.drive()
    boat.sail()

    bicycle.drive()
    bicycle.stop()

    car.drive()
    car.stop()

    # Вывод строкового представления объектов
    print(boat)
    print(bicycle)
    print(car)
