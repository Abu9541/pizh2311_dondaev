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
