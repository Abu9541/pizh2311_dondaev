class Transport:
    """
    Базовый класс для всех транспортных средств.
    """

    def __init__(self, name: str, speed: int, year: int):
        """
        Инициализация транспортного средства.
        Принимает название, скорость и год выпуска ТС.
        """
        self._name = name  # Защищенное поле
        self.speed = speed  # Общедоступное поле
        self.__year = year  # Приватное поле

    def drive(self):
        """
        Базовый метод для движения транспортного средства.
        """
        print(f"{self._name} движется со скоростью {self.speed} км/ч.")

    def stop(self):
        """
        Базовый метод для остановки транспортного средства.
        """
        print(f"{self._name} остановился.")

    def __str__(self):
        """
        Перегрузка методов класса: возвращение объекта в виде строки.
        """
        return f"{self._name} (скорость: {self.speed} км/ч, год выпуска: {self.__year})"


class WaterTransport(Transport):
    """
    Класс для водных транспортных средств.
    """

    def __init__(self, name: str, speed: int, year: int, depth: float):
        """
        Инициализация водного транспортного средства.
        Принимает название, скорость, год выпуска и глубину плавания водного ТС.
        """
        super().__init__(name, speed, year)
        self.depth = depth

    def sail(self):
        """
        Метод для движения по воде.
        """
        print(f"{self._name} плывет по воде на глубине {self.depth} метров.")


class WheeledTransport(Transport):
    """
    Класс для колесных транспортных средств.
    """

    def __init__(self, name: str, speed: int, year: int, wheel_count: int):
        """
        Инициализация колесного транспортного средства.
        Принимает название, скорость, год выпуска и количество колес колесного ТС.
        """
        super().__init__(name, speed, year)
        self._wheel_count = wheel_count  # Защищенное поле

    def drive(self):
        """
        Переопределенный метод для движения колесного транспортного средства.
        """
        print(f"{self._name} едет на {self._wheel_count} колесах со скоростью {self.speed} км/ч.")


class Car(WheeledTransport):
    """
    Класс для автомобилей.
    """

    def __init__(self, name: str, speed: int, year: int, wheel_count: int, brand: str):
        """
        Инициализация автомобиля.
        Принимает название, скорость, год выпуска, количество колес и бренд автомобиля.
        """
        super().__init__(name, speed, year, wheel_count)
        self.__brand = brand  # Приватное поле

    def drive(self):
        """
        Переопределенный метод для движения автомобиля.
        """
        print(f'{self._name} "{self.__brand}" едет по дороге со скоростью {self.speed} км/ч.')
