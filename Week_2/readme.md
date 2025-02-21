# Лабораторная работа на неделю 2
## **Тема**: Объектно-ориентированное программирование на Python 
### Студента группы ПИЖ-б-о-23-1(1) Дондаева Абу Умар-Пашаевича <br><br>
**Репозиторий Git:** https://github.com/Abu9541/pizh2311_dondaev  
**Вариант: 8**  
**Практическая работа:**  
*Задание:*  
Экземпляру класса при инициализации передается аргумент - список тем для разговора.  
Класс реализует методы:
- add_theme(value) - добавить тему в конец;
- shift_one() - сдвинуть темы на одну вправо (последняя становится первой, остальные сдвигаются);
- reverse_order() - поменять порядок тем на обратный;
- get_themes() - возвращает список тем;
- get_first() - возвращает первую тему.  

*Ответ:*  
```python
"""Модуль для разметки абстрактных методов"""
import abc


class Themes:
    """
    Класс реализации тем для разговора
    """

    def __init__(self, themes: list):
        """
        Конструктор класса, передает список тем объекту
        """
        self.themes = themes

    @abc.abstractmethod
    def add_theme(self, theme: str):
        """
        Абстрактный метод реализации добавления темы в конец списка тем.
        """
        raise NotImplementedError("Нельзя вызывать абстрактный метод!")  # возбуждение ошибки

    def shift_one(self):
        """
        Метод, смещающий темы вправо на одну. Ничего не принимает.
        В результате изменяет список тем так, что темы смещены на одну вправо, последняя становится первой.
        """
        reserve = [self.themes[len(self.themes) - 1]]
        for i in range(len(self.themes) - 1):
            reserve.append(self.themes[i])
        self.themes = reserve

    def reverse_order(self):
        """
        Метод, разворачивающий список тем. Ничего не принимает.
        В результате изменяет список тем так, что темы расположены в обратном порядке.
        """
        self.themes.reverse()

    def get_themes(self):
        """
        Метод, возвращающий список тем. Ничего не принимает.
        Возвращает список тем.
        """
        return self.themes

    def set_new_themes(self, themes: list):
        """
        Метод установки нового списка тем. Принимает новый список тем.
        Изменяет список старых тем на новый.
        """
        self.themes = themes

    def get_first(self):
        """
        Метод, возвращающий первую тему списка. Ничего не принимает.
        Возвращает первую тему списка.
        """
        return self.themes[0]

    def __setattr__(self, attr, value):
        """
        Метод перегрузки установки новых атрибутов. Осуществляет инкапсуляцию.
        """
        if attr == 'themes':
            self.__dict__[attr] = value
        else:
            raise AttributeError

    def __call__(self, themes: list):
        """
        Метод перегрузки вызова класса. Переопределяет список тем.
        """
        self.themes = themes
 
    def __repr__(self):
        """
        Метод перегрузки вызова объекта строкой. Возвращает список тем.
        """
        return f'{self.themes}'


class Theme(Themes):
    """
    Класс, наследующий класс тем для разговора.
    Создан для реализации наследования, полиморфизма и абстракции.
    """

    def add_theme(self, theme: str):
        """
        Определение абстрактного метода родительского класса. Метод принимает название темы.
        Тема добавляется в конец списка тем.
        """
        self.themes.append(theme)

    def get_themes(self):
        """
        Переопределение метода вывода списка тем.
        Изменен формат вывода.
        """
        line = ''
        for theme in self.themes:
            line += f'{theme}    '
        return f'Themes: {line}'


"""Проверка работы методов."""
theme_pack_1 = ['weather', 'hobby', 'education', 'computers', 'food']
theme_pack_2 = ['school', 'football', 'astronomy', 'travelling']
themes_1 = Theme(theme_pack_1)
print(themes_1.get_first())
print(themes_1.get_themes())
themes_1.add_theme('math')
print(themes_1.get_themes())
themes_1.shift_one()
print(themes_1.get_themes())
themes_1.reverse_order()
print(themes_1.get_themes())
themes_1(theme_pack_2)
print(themes_1)
themes_1.add_theme('diving')
print(themes_1.get_themes())
```  
Вывод программы:  
weather  
Themes: weather    hobby    education    computers    food      
Themes: weather    hobby    education    computers    food    math    
Themes: math    weather    hobby    education    computers    food    
Themes: food    computers    education    hobby    weather    math    
['school', 'football', 'astronomy', 'travelling']  
Themes: school    football    astronomy    travelling    diving    

