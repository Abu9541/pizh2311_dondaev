class Pizza:
    """
    Класс Пицца для инициализации пиццы с ее названием, видом теста,
    соусом, начинкой и ценой.
    Реализованы методы готовки пиццы, ее выпечки, нарезки и упаковки.
    """

    def __init__(self, name: str, dough: str, sauce: str, toppings: list, price: float):
        """
        Конструктор класса. Принимает и присваивает следующие параметры полям класса:
        название пиццы, тесто, соус, начинка, цена.
        """
        self.name = name
        self.dough = dough
        self.sauce = sauce
        self.toppings = toppings
        self.price = price

    def prepare(self):
        """
        Метод, имитирующий готовку пиццы. Ничего не принимает.
        Выводит информацию о стадии готовки пиццы.
        """
        print(f"Готовим {self.name}...")
        print(f"Замешиваем тесто: {self.dough}...")
        print(f"Добавляем соус: {self.sauce}...")
        print(f"Добавляем начинку: {', '.join(self.toppings)}...")
        print("Пицца готова к выпечке.")

    def bake(self):
        """
        Метод, имитирующий выпечку пиццы. Ничего не принимает.
        Выводит информацию о том, что пицца выпекается.
        """
        print(f"Выпекаем {self.name}...")
        print("Пицца выпечена.")

    def cut(self):
        """
        Метод, имитирующий резку пиццы. Ничего не принимает.
        Выводит информацию о том, что пицца режется.
        """
        print(f"Режем {self.name}...")
        print("Пицца разрезана по кускам.")

    def pack(self):
        """
        Метод, имитирующий упаковку пиццы. Ничего не принимает.
        Выводит информацию о том, что пицца упаковывается.
        """
        print(f"Упаковываем {self.name}...")
        print("Пицца упакована.")

    def __str__(self):
        """
        Перегрузка методов класса: вывод объекта через print().
        Возвращает название пиццы и ее стоимость.
        """
        return f"{self.name} - {self.price} руб."


class PepperoniPizza(Pizza):
    """
    Класс Пепперони - наследник класса Пицца.
    Содержит конструктор класса для инициализации пиццы Пепперони.
    """

    def __init__(self):
        """
        Конструктор класса. Инициализирует пиццу с определенным составом.
        """
        super().__init__("Пепперони", "тонкое тесто", "томатный соус", ["пепперони", "сыр моцарелла"], 250.55)


class BarbecuePizza(Pizza):
    """
    Класс Барбекю - наследник класса Пицца.
    Содержит конструктор класса для инициализации пиццы Барбекю.
    """

    def __init__(self):
        """
        Конструктор класса. Инициализирует пиццу с определенным составом.
        """
        super().__init__("Барбекю", "толстое тесто", "соус барбекю", ["курица", "лук", "сыр моцарелла"], 299.99)


class SeafoodPizza(Pizza):
    """
    Класс Дары моря - наследник класса Пицца.
    Содержит конструктор класса для инициализации пиццы Дары моря.
    """

    def __init__(self):
        """
        Конструктор класса. Инициализирует пиццу с определенным составом.
        """
        super().__init__("Дары Моря", "тонкое тесто", "сливочный соус", ["креветки", "мидии", "сыр моцарелла"], 350.55)


class Order:
    """
    Класс заказа. Реализованы методы добавления пиццы в заказ,
    сброса заказа, его вывода и завершения.
    """

    def __init__(self):
        """
        Конструктор класса. Инициализирует поля для списка пицц в заказе и общей суммы.
        """
        self.pizzas = []
        self.total = 0

    def add_pizza(self, pizza):
        """
        Метод, добавляющий в заказ пиццу. Принимает название пиццы и добавляет в список пицц.
        Ничего не возвращает.
        """
        self.pizzas.append(pizza)
        self.total += pizza.price
        print(f"Пицца {pizza.name} добавлена в заказ.")

    def reset(self):
        """
        Метод для сброса заказа. Ничего не принимает.
        Удаляет пиццы из списка пицц и обнуляет общую сумму.
        """
        self.pizzas.clear()
        self.total = 0

    def display_order(self):
        """
        Метод вывода заказа. Ничего не принимает.
        Выводит список пицц в заказе и общую сумму.
        """
        print("Ваш заказ:")
        for pizza in self.pizzas:
            print(f"- {pizza.name}")
        print(f"Итого: {self.total} руб.")

    @staticmethod
    def finish_order():
        """
        Метод завершения заказа. Ничего не принимает.
        Выводит сообщение о том, что заказ выполнен.
        """
        print(f"Заказ выполнен.")

    def __str__(self):
        """
        Перегрузка методов класса: вывод объекта через print().
        Возвращает список заказанных пицц.
        """
        return f"Заказанные пиццы: {self.pizzas}"


class Terminal:
    """
    Класс терминала. Инициализирует терминал для пользователя.
    Реализованы методы отображения меню, оформления и подтверждения заказа.
    """

    def __init__(self):
        """
        Конструктор класса. Инициализирует словарь, где числу соответствует один из классов-наследников класса Pizza.
        """
        self.menu = {
            1: PepperoniPizza(),
            2: BarbecuePizza(),
            3: SeafoodPizza()
        }

    def display_menu(self):
        """
        Метод отображения меню. Ничего не принимает.
        Выводит меню кафе.
        """
        print("Меню:")
        for key, pizza in self.menu.items():
            print(f"{key}. {pizza.name} - {pizza.price} руб.")

    def take_order(self):
        """
        Метод для оформления заказа. Ничего не принимает.
        Возвращает готовый заказ.
        """
        order_1 = Order()
        while True:
            self.display_menu()
            choice = input("Выберите номер пиццы (или 'готово' для завершения, или 'отмена' для отмены): ")
            if choice.lower() == "готово":
                break
            elif choice.lower() == "отмена":
                order_1.reset()
            try:
                choice = int(choice)
                if choice in self.menu:
                    order_1.add_pizza(self.menu[choice])
                else:
                    print("Неверный выбор. Пожалуйста, выберите номер из меню.")
            except ValueError:
                print("Пожалуйста, введите номер пиццы.")
        return order_1

    @staticmethod
    def process_order(ordered):
        """
        Метод для подтверждения заказа. Принимает объект класса Order.
        Ничего не возвращает. Выводит информацию о подтверждении заказа.
        """
        ordered.display_order()
        confirm = input("Подтвердите заказ (да/нет): ")
        if confirm.lower() == 'да':
            print("Заказ подтвержден. Готовим ваши пиццы...")
            for pizza in ordered.pizzas:
                pizza.prepare()
                pizza.bake()
                pizza.cut()
                pizza.pack()
            print("Заказ готов! Спасибо за покупку!")
        else:
            print("Заказ отменен.")


# Пример использования
terminal = Terminal()
order = terminal.take_order()
terminal.process_order(order)
