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


"""Класс реализации тем для разговора"""


class Themes:

    """Конструктор класса, передает список тем объекту"""
    def __init__(self, themes: list):
        self.themes = themes

    """Абстрактный метод реализации добавления темы в конец списка тем."""
    @abc.abstractmethod  
    def add_theme(self, theme: str): 
        raise NotImplementedError("Нельзя вызывать абстрактный метод!")  # возбуждение ошибки

    """Метод, смещающий темы вправо на одну. Ничего не принимает.
    В результате изменяет список тем так, что темы смещены на одну вправо, последняя становится первой."""
    def shift_one(self):  
        reserve = [self.themes[len(self.themes) - 1]]
        for i in range(len(self.themes) - 1):
            reserve.append(self.themes[i])
        self.themes = reserve

    """Метод, разворачивающий список тем. Ничего не принимает.
    В результате изменяет список тем так, что темы расположены в обратном порядке."""
    def reverse_order(self):
        self.themes.reverse()

    """Метод, возвращающий список тем. Ничего не принимает.
    Возвращает список тем."""
    def get_themes(self):
        return self.themes

    """Метод установки нового списка тем. Принимает новый список тем.
    Изменяет список старых тем на новый."""
    def set_new_themes(self, themes: list):
        self.themes = themes

    """Метод, возвращающий первую тему списка. Ничего не принимает.
    Возвращает первую тему списка."""
    def get_first(self):
        return self.themes[0]

    """Метод перегрузки установки новых атрибутов. Осуществляет инкапсуляцию."""
    def __setattr__(self, attr, value):
        if attr == 'themes':
            self.__dict__[attr] = value
        else:
            raise AttributeError

    """Метод перегрузки вызова класса. Переопределяет список тем."""
    def __call__(self, themes: list):
        self.themes = themes

    """Метод перегрузки вызова объекта строкой. Возвращает список тем."""
    def __repr__(self):
        return f'{self.themes}'


"""Класс, наследующий класс тем для разговора.
Создан для реализации наследования, полиморфизма и абстракции."""


class Theme(Themes):

    """Определение абстрактного метода родительского класса. Метод принимает название темы.
    Тема добавляется в конец списка тем."""
    def add_theme(self, theme: str):
        self.themes.append(theme)

    """Переопределение метода вывода списка тем.
    Изменен формат вывода."""
    def get_themes(self):
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

