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
class Theme:

    def __init__(self, themes):
        self.themes = themes

    def add_theme(self, theme):
        self.themes.append(theme)

    def shift_one(self):
        reserve = [self.themes[len(self.themes) - 1]]
        for i in range(len(self.themes)-1):
            reserve.append(self.themes[i])
        self.themes = reserve

    def reverse_order(self):
        self.themes.reverse()

    def get_themes(self):
        return self.themes

    def get_first(self):
        return self.themes[0]


theme_pack = ['weather', 'hobby', 'education', 'computers', 'food']
themes_1 = Theme(theme_pack)
print(themes_1.get_first())
print(themes_1.get_themes())
themes_1.add_theme('math')
print(themes_1.get_themes())
themes_1.shift_one()
print(themes_1.get_themes())
themes_1.reverse_order()
print(themes_1.get_themes())
```  
Вывод программы:  
weather  
['weather', 'hobby', 'education', 'computers', 'food']  
['weather', 'hobby', 'education', 'computers', 'food', 'math']  
['math', 'weather', 'hobby', 'education', 'computers', 'food']  
['food', 'computers', 'education', 'hobby', 'weather', 'math']  
