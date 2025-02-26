import abc


class Arithmetic:
    """
    Абстрактный класс для арифметических действий.
    В данном классе есть следующие абстрактные методы: сложение, вычитание, умножение и деление.
    """

    @abc.abstractmethod
    def __add__(self, other):
        raise NotImplementedError("Нельзя вызывать абстрактный метод!")

    @abc.abstractmethod
    def __sub__(self, other):
        raise NotImplementedError("Нельзя вызывать абстрактный метод!")

    @abc.abstractmethod
    def __mul__(self, other):
        raise NotImplementedError("Нельзя вызывать абстрактный метод!")

    @abc.abstractmethod
    def __truediv__(self, other):
        raise NotImplementedError("Нельзя вызывать абстрактный метод!")


class Roman(Arithmetic):
    """
    Класс римских чисел.
    В классе реализованы методы перевода римских чисел в арабские и наоборот,
    сложения, вычитания, умножения и деления римских чисел.
    """

    @staticmethod
    def roman_to_int(roman: str):
        """
        Метод перевода римского числа в арабское.
        Принимает римское число в виде строки.
        Возвращает арабское число.
        """
        roman_numerals = {'I': 1, 'V': 5, 'X': 10, 'L': 50, 'C': 100, 'D': 500, 'M': 1000}
        arabic = 0
        prev_value = 0
        for char in reversed(roman):
            value = roman_numerals[char]
            if value < prev_value:
                arabic -= value
            else:
                arabic += value
            prev_value = value
        return arabic

    @staticmethod
    def int_to_roman(arabic: int):
        """
        Метод перевода арабского числа в римское.
        Принимает целое число.
        Возвращает римское число в виде строки.
        """
        val = [
            1000, 900, 500, 400,
            100, 90, 50, 40,
            10, 9, 5, 4,
            1
        ]
        syms = [
            "M", "CM", "D", "CD",
            "C", "XC", "L", "XL",
            "X", "IX", "V", "IV",
            "I"
        ]
        roman_num = ''
        i = 0
        while arabic > 0:
            for _ in range(arabic // val[i]):
                roman_num += syms[i]
                arabic -= val[i]
            i += 1
        return roman_num

    def __init__(self, value):
        """
        Конструктор класса.
        Принимает целочисленное или строковое значение.
        Если значение целочисленное, просто присваивает его полю класса Roman.
        Если число строковое, переводит его в целочисленное и присваивает полю класса Roman.
        """
        if isinstance(value, str):
            self.value = self.roman_to_int(value)
        elif isinstance(value, int):
            self.value = value
        else:
            raise ValueError("Значение должно быть строковым (римское число) или целым (арабское число).")

    def __add__(self, other):
        """
        Перегрузка методов класса: сложение.
        Принимает два объекта и складывает их.
        Возвращает результат сложения.
        """
        if isinstance(other, Roman):
            return Roman(self.value + other.value)
        else:
            return Roman(self.value + other)

    def __sub__(self, other):
        """
        Перегрузка методов класса: вычитание.
        Принимает два объекта и вычитает второе от первого.
        Возвращает результат вычитания.
        """
        if isinstance(other, Roman):
            return Roman(self.value - other.value)
        else:
            return Roman(self.value - other)

    def __mul__(self, other):
        """
        Перегрузка методов класса: умножение.
        Принимает два объекта и умножает их.
        Возвращает результат умножения.
        """
        if isinstance(other, Roman):
            return Roman(self.value * other.value)
        else:
            return Roman(self.value * other)

    def __truediv__(self, other):
        """
        Перегрузка методов класса: целочисленное деление.
        Принимает два объекта и делит первое на второе.
        Возвращает результат деления.
        """
        if isinstance(other, Roman):
            return Roman(self.value // other.value)
        else:
            return Roman(self.value // other)

    def __str__(self):
        """
        Перегрузка методов класса: вывод объекта через print().
        Возвращает римское число.
        """
        return self.int_to_roman(self.value)

    def __repr__(self):
        """
        Перегрузка методов класса: вывод объекта при запросе его в виде строки.
        Возвращает строку f"Roman('{self.int_to_roman(self.value)}')".
        """
        return f"Roman('{self.int_to_roman(self.value)}')"

    def __setattr__(self, attr, value):
        """
        Метод перегрузки установки новых атрибутов. Осуществляет инкапсуляцию.
        """
        if attr == 'value':
            self.__dict__[attr] = value
        else:
            raise AttributeError

    def __call__(self, value):
        """
        Метод перегрузки вызова класса. Переопределяет значение объекта.
        """
        if isinstance(value, str):
            self.value = self.roman_to_int(value)
        elif isinstance(value, int):
            self.value = value
        else:
            raise ValueError("Значение должно быть строковым (римское число) или целым (арабское число).")


# Проверка кода
a = Roman("X")
b = Roman("V")

print(a + b)  # XV
print(a - b)  # V
print(a * b)  # L
print(a / b)  # II

a(25)

print(a + b)  # XXX
print(a - b)  # XX
print(a * b)  # CXXV
print(a / b)  # V
