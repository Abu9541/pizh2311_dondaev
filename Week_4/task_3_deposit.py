class TimeDeposit:
    """
    Абстрактный класс - срочный вклад.
    Поля:
      - self.name (str): наименование;
      - self._interest_rate (float): процент по вкладу (0; 100];
      - self._period_limit (tuple (int, int)):
            допустимый срок вклада в месяцах [от; до);
      - self._sum_limit (tuple (float, float)):
            допустимая сумма вклада [от; до).
    Свойства:
      - self.currency (str): знак/наименование валюты.
    Методы:
      - self._check_self(initial_sum, period): проверяет соответствие данных
            ограничениям вклада;
      - self.get_profit(initial_sum, period): возвращает прибыль по вкладу;
      - self.get_sum(initial_sum, period):
            возвращает сумму по окончании вклада.
    """

    def __init__(self, name: str, interest_rate: float, period_limit: tuple, sum_limit: tuple):
        """
        Инициализировать атрибуты класса.
        """
        self.name = name
        self._interest_rate = interest_rate
        self._period_limit = period_limit
        self._sum_limit = sum_limit
        self._check_self()

    def __str__(self):
        """
        Вернуть строкое представление депозита.
        Формат вывода:

        Наименование:       Срочный Вклад
        Валюта:             руб.
        Процентная ставка:  5
        Срок (мес.):        [6; 18)
        Сумма:              [1,000; 100,000)
        """
        return (f"Наименование:       {self.name}\n"
                f"Валюта:             {self.currency}\n"
                f"Процентная ставка:  {self._interest_rate}\n"
                f"Срок (мес.):        [{self._period_limit[0]}; {self._period_limit[1]})\n"
                f"Сумма:              [{self._sum_limit[0]:,.0f}; {self._sum_limit[1]:,.0f})")

    @property
    def currency(self):
        return "руб."

    def _check_self(self):
        """
        Проверить, что данные депозита являются допустимыми.
        """
        assert 0 < self._interest_rate <= 100, "Неверно указан процент по вкладу!"
        assert 1 <= self._period_limit[0] < self._period_limit[1], "Неверно указаны ограничения по сроку вклада!"
        assert 0 < self._sum_limit[0] <= self._sum_limit[1], "Неверно указаны ограничения по сумме вклада!"

    def _check_user_params(self, initial_sum: float, period: int):
        """
        Проверить, что данные депозита соответствуют его ограничениям.
        """
        is_sum_ok = self._sum_limit[0] <= initial_sum < self._sum_limit[1]
        is_period_ok = self._period_limit[0] <= period < self._period_limit[1]
        assert is_sum_ok and is_period_ok, "Условия вклада не соблюдены!"

    def get_profit(self, initial_sum: float, period: int):
        """
        Вернуть прибыль по вкладу вклада клиента.
        Параметры:
          - initial_sum (float): первоначальная сумма;
          - period (int): количество месяцев размещения вклада.
        Формула:
          первоначальная_сумма * % / 100 * период / 12
        """
        self._check_user_params(initial_sum, period)
        return initial_sum * self._interest_rate / 100 * period / 12

    def get_sum(self, initial_sum: float, period: int):
        """
        Вернуть сумму вклада клиента после начисления прибыли.
        Параметры:
          - initial_sum (float): первоначальная сумма;
          - period (int): количество месяцев размещения вклада.
        """
        return initial_sum + self.get_profit(initial_sum, period)


class BonusTimeDeposit(TimeDeposit):
    """
    Cрочный вклад c получением бонуса к концу срока вклада.
    Бонус начисляется как % от прибыли, если вклад больше определенной суммы.
    Атрибуты:
      - self._bonus (dict ("percent"=int, "sum"=float)):
        % от прибыли, мин. сумма;
    """

    def __init__(self, name: str, interest_rate: float, period_limit: tuple, sum_limit: tuple, bonus: dict):
        """
        Инициализировать атрибуты класса.
        """
        self._bonus = bonus
        super().__init__(name, interest_rate, period_limit, sum_limit)
        self._check_self()

    def __str__(self):
        """
        Вернуть строкое представление депозита.
        К информации о родителе добавляется информацию о бонусе.
        Формат вывода:

        Наименование:       Бонусный Вклад
        Валюта:             руб.
        Процентная ставка:  5
        Срок (мес.):        [6; 18)
        Сумма:              [1,000; 100,000)
        Бонус (%):          5
        Бонус (мин. сумма): 2,000
        """
        return (super().__str__() + "\n" +
                f"Бонус (%):          {self._bonus['percent']}\n"
                f"Бонус (мин. сумма): {self._bonus['sum']:,.0f}")

    def _check_self(self):
        """
        Проверить, что данные депозита являются допустимыми.
        Дополняем родительский метод проверкой бонуса.
        """
        super()._check_self()
        assert 0 < self._bonus['percent'] <= 100, "Неверно указан процент бонуса!"
        assert 0 < self._bonus['sum'], "Неверно указана минимальная сумма для бонуса!"

    def get_profit(self, initial_sum: float, period: int):
        """
        Вернуть прибыль по вкладу вклада клиента.
        Параметры:
          - initial_sum (float): первоначальная сумма;
          - period (int): количество месяцев размещения вклада.
        Формула:
          - прибыль = сумма * процент / 100 * период / 12
        Для подсчета прибыли используется родительский метод.
        Далее, если первоначальная сумма > необходимой,
        начисляется бонус.
        """
        profit = super().get_profit(initial_sum, period)
        if initial_sum > self._bonus['sum']:
            profit += profit * self._bonus['percent'] / 100
        return profit


class CompoundTimeDeposit(TimeDeposit):
    """
    Срочный вклад c ежемесячной капитализацией процентов.
    """

    def __str__(self):
        """
        Вернуть строкое представление депозита.
        К информации о родителе добавляется информация о капитализации.
        Формат вывода:

        Наименование:       Вклад с Капитализацией
        Валюта:             руб.
        Процентная ставка:  5
        Срок (мес.):        [6; 18)
        Сумма:              [1,000; 100,000)
        Капитализация %   : Да
        """
        return super().__str__() + "\nКапитализация %   : Да"

    def get_profit(self, initial_sum: float, period: int):
        """
        Вернуть прибыль по вкладу вклада клиента.
        Параметры:
          - initial_sum (float): первоначальная сумма;
          - period (int): количество месяцев размещения вклада.
        Родительский метод для подсчета прибыли использовать не нужно,
        переопределив его полностью - расчет осуществляется по новой формуле.
        Капитализация процентов осуществляется ежемесячно.
        Нужно не забыть про самостоятельный вызов проверки параметров.
        Формула:
          первоначальная_сумма * (1 + % / 100 / 12) ** период -
          первоначальная_сумма
        """
        self._check_user_params(initial_sum, period)
        return initial_sum * (1 + self._interest_rate / 100 / 12) ** period - initial_sum


deposits_data_1 = dict(interest_rate=5, period_limit=(6, 18),
                       sum_limit=(1000, 100000))
deposits_data_2 = dict(interest_rate=5, period_limit=(6, 18),
                       sum_limit=(1000000, 5000000))

# Список имеющихся депозитов
deposits = (
    TimeDeposit("Сохраняй", interest_rate=5,
                period_limit=(6, 18),
                sum_limit=(1000, 100000)),
    BonusTimeDeposit("Бонусный 2", **deposits_data_1,
                     bonus=dict(percent=5, sum=2000)),
    CompoundTimeDeposit("С капитализацией", **deposits_data_1),
    TimeDeposit("Богач", interest_rate=5,
                period_limit=(6, 18),
                sum_limit=(1000000, 5000000)),
    BonusTimeDeposit("Бонусный с миллиона", **deposits_data_2,
                     bonus=dict(percent=2.5, sum=2000)),
    CompoundTimeDeposit("С капитализацией на миллион", **deposits_data_2)
)
