class Person:

    def __init__(self, name: str, surname: str, qualification: int = 1):
        self.name = name
        self.surname = surname
        self.qualification = qualification

    def info(self):
        print(f'Имя и фамилия: {self.name} {self.surname}. Квалификация: {self.qualification}')

    def __del__(self):
        print(f'До свидания, мистер {self.name} {self.surname}.')


Toby = Person('Toby', 'Maguire', 3)
Andrew = Person('Andrew', 'Garfield', 2)
Tom = Person('Tom', 'Holland')
Toby.info()
Andrew.info()
Tom.info()
del Tom
close = input()
