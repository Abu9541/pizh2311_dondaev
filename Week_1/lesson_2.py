from random import randint


class Warrior:

    health = 100

    def __init__(self, number: int):
        self.number = number

    def attack(self, unit):
        n = unit.number
        if self.health > 0:
            if unit.health > 0:
                unit.health -= 20
                print("Юнит", self.number, "ударил юнита", n, ".\nY юнита", n, "осталось", unit.health, "здоровья.")
                if unit.health <= 0:
                    print("Юнит", self.number, "победил!")
            else:
                print("Юнит", n, "уже мертв.")
        else:
            print("Юниту", self.number, "не хватает здоровья, чтобы ударить. Он умер.")


def start_fight(unit1, unit2):
    number_list = [unit1.number, unit2.number]
    while unit1.health > 0 and unit2.health > 0:
        n = randint(0, 1)
        if number_list[n] == unit1.number:
            unit1.attack(unit2)
        else:
            unit2.attack(unit1)


unit_1 = Warrior(1)
unit_2 = Warrior(2)
start_fight(unit_1, unit_2)
