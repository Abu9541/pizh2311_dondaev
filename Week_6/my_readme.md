# **Тема**: Реализация принципов SOLID 
## Студента группы ПИЖ-б-о-23-1(1) Дондаева Абу Умар-Пашаевича <br><br>
**Репозиторий Git:** https://github.com/Abu9541/pizh2311_dondaev   
**Практическая работа:** 


*the_snake.py до реализации принципов инверсии зависимостей, открытости/закрытости и разделения интерфейсов SOLID:*
```python
import pygame
import random

# Константы для размеров поля и сетки:
SCREEN_WIDTH, SCREEN_HEIGHT = 640, 480
GRID_SIZE = 20
GRID_WIDTH = SCREEN_WIDTH // GRID_SIZE
GRID_HEIGHT = SCREEN_HEIGHT // GRID_SIZE

# Направления движения:
UP = (0, -1)
DOWN = (0, 1)
LEFT = (-1, 0)
RIGHT = (1, 0)

# Цвет фона - черный:
BOARD_BACKGROUND_COLOR = (0, 0, 0)

# Цвет границы ячейки
BORDER_COLOR = (93, 216, 228)

# Цвет яблока
APPLE_COLOR = (255, 0, 0)

# Цвет змейки
SNAKE_COLOR = (0, 255, 0)

# Скорость движения змейки:
SPEED = 20

# Настройка игрового окна:
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), 0, 32)

# Заголовок окна игрового поля:
pygame.display.set_caption("Змейка")

# Настройка времени:
clock = pygame.time.Clock()


# Тут опишите все классы игры.
class GameObject:
    """Класс GameObject базовый класс, от которого
    наследуются другие классы.
    """

    def __init__(self, position=None, body_color=BOARD_BACKGROUND_COLOR):
        """
        Функция инициализации.
        Должна быть реализована во всех классах.
        """
        if position is None:
            center_x = SCREEN_WIDTH // 2
            center_y = SCREEN_HEIGHT // 2
            position = ((center_x // GRID_SIZE * GRID_SIZE,
                        center_y // GRID_SIZE * GRID_SIZE,))
        self.position = position
        self.body_color = body_color

    def draw(self):
        """
        Абстрактный метод для отрисовки объекта.
        Должен быть реализован в дочерних классах.
        """
        pass


class Apple(GameObject):
    """
    Класс Apple унаследованный класс от GameObject.
    Он описывает яблоко и действия с ним.
    """

    def __init__(self, body_color=APPLE_COLOR, position=None):
        """
        Функция инициализации.
        Должна быть реализована во всех классах.
        """
        super().__init__(position)
        self.body_color = body_color
        if self.position is None:
            self.randomize_position()

    def randomize_position(self):
        """
        Функция определения позиции
        для спавна яблока.
        """
        self.position = (
            random.randint(0, GRID_WIDTH - 1) * GRID_SIZE,
            random.randint(0, GRID_HEIGHT - 1) * GRID_SIZE,
        )

    def draw(self):
        """
        Функция отрисовки яблока
        на игровом поле.
        """
        rect = pygame.Rect((self.position,
                           (GRID_SIZE, GRID_SIZE)))
        pygame.draw.rect(screen,
                         self.body_color, rect)
        pygame.draw.rect(screen, BORDER_COLOR, rect, 1)


class Snake(GameObject):
    """
    Класс Snake унаследованный класс от GameObject.
    Он описывает змейку и ее поведение.
    """

    length = 1

    def __init__(
        self,
        length=1,
        direction=RIGHT,
        next_direction=None,
        body_color=SNAKE_COLOR,
        position=None,
    ):
        """
        Функция инициализации.
        Должна быть реализована во всех классах.
        """
        super().__init__(position)
        self.body_color = body_color
        self.length = length
        self.direction = direction
        self.positions = [(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)]
        self.next_direction = (
            next_direction if next_direction is not None else direction
        )
        self.last = None

    def update_direction(self):
        """Функция обновления направления движения змеи."""
        if self.next_direction:
            self.direction = self.next_direction
            self.next_direction = None

    def move(self, apple):
        """
        Функция обновляет позицию змейки,
        добавляя новый сегмент головы и удаляя хвост.
        """
        if not self.positions:
            return

        head_x, head_y = self.positions[0]

        head_x += self.direction[0] * GRID_SIZE
        head_y += self.direction[1] * GRID_SIZE

        if head_x >= SCREEN_WIDTH:
            head_x = 0
        elif head_x < 0:
            head_x = SCREEN_WIDTH - GRID_SIZE

        if head_y >= SCREEN_HEIGHT:
            head_y = 0
        elif head_y < 0:
            head_y = SCREEN_HEIGHT - GRID_SIZE

        self.positions.insert(0, (head_x, head_y))

        # Проверка столкновения с телом змейки
        if (head_x, head_y) in self.positions[1:]:
            self.reset()

        if (head_x, head_y) != apple.position:
            self.positions.pop()
        else:
            self.length += 1
            apple.randomize_position()

    def draw(self):
        """
        Функция отрисовки змеи и ее поведения
        на игровом поле.
        """
        for position in self.positions[:-1]:
            rect = pygame.Rect(position, (GRID_SIZE, GRID_SIZE))
            pygame.draw.rect(screen, self.body_color, rect)
            pygame.draw.rect(screen, BORDER_COLOR, rect, 1)

        # Отрисовка головы змейки
        head_rect = pygame.Rect(self.positions[0], (GRID_SIZE, GRID_SIZE))
        pygame.draw.rect(screen, self.body_color, head_rect)
        pygame.draw.rect(screen, BORDER_COLOR, head_rect, 1)

        # Затирание последнего сегмента
        if self.last:
            last_rect = pygame.Rect(self.last, (GRID_SIZE, GRID_SIZE))
            pygame.draw.rect(screen, BOARD_BACKGROUND_COLOR, last_rect)

    def get_head_position(self):
        """Функция определения позиции головы змеи."""
        return self.position[0]

    def reset(self):
        """Функция сброса прогресса при столкновении с собой."""
        self.length = 1
        self.positions = [(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)]
        self.last = None
        self.direction = random.choice([UP, DOWN, LEFT, RIGHT])


def handle_keys(game_object):
    """
    Функция обработки
    нажатия клавиш.
    """
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            raise SystemExit
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP and game_object.direction != DOWN:
                game_object.next_direction = UP
            elif event.key == pygame.K_DOWN and game_object.direction != UP:
                game_object.next_direction = DOWN
            elif event.key == pygame.K_LEFT and game_object.direction != RIGHT:
                game_object.next_direction = LEFT
            elif event.key == pygame.K_RIGHT and game_object.direction != LEFT:
                game_object.next_direction = RIGHT
            elif event.key == pygame.K_ESCAPE:
                pygame.quit()
                raise SystemExit


def main():
    """Основная функция."""
    # Инициализация PyGame:
    pygame.init()
    # Тут нужно создать экземпляры классов.
    apple = Apple()
    snake = Snake(length=1)

    while True:
        handle_keys(snake)
        snake.update_direction()
        snake.move(apple)
        if snake.positions == []:
            snake.reset()
            apple.randomize_position()
        screen.fill(BOARD_BACKGROUND_COLOR)
        if snake.positions:
            snake.draw()
            apple.draw()

        pygame.display.update()

        clock.tick(SPEED)


if __name__ == "__main__":
    main()

```  

*the_snake.py после реализации принципов инверсии зависимостей, открытости/закрытости и разделения интерфейсов SOLID:*  
```python
import pygame
import random
from abc import ABC, abstractmethod

# Константы
SCREEN_WIDTH, SCREEN_HEIGHT = 640, 480
GRID_SIZE = 20
GRID_WIDTH = SCREEN_WIDTH // GRID_SIZE
GRID_HEIGHT = SCREEN_HEIGHT // GRID_SIZE

UP = (0, -1)
DOWN = (0, 1)
LEFT = (-1, 0)
RIGHT = (1, 0)

BOARD_BACKGROUND_COLOR = (0, 0, 0)
BORDER_COLOR = (93, 216, 228)
APPLE_COLOR = (255, 0, 0)
SNAKE_COLOR = (0, 255, 0)
SPEED = 20

# Инициализация PyGame
pygame.init()
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), 0, 32)
pygame.display.set_caption("Змейка")
clock = pygame.time.Clock()


# Интерфейс для игрового объекта
class IGameObject(ABC):
    @abstractmethod
    def draw(self):
        pass

    @property
    @abstractmethod
    def position(self):
        pass

    @position.setter
    @abstractmethod
    def position(self, value):
        pass


# Интерфейс для еды
class IFood(IGameObject):
    @abstractmethod
    def randomize_position(self):
        pass


# Интерфейс контролируемого объекта
class IControllable(IGameObject):
    @property
    @abstractmethod
    def direction(self):
        pass

    @direction.setter
    @abstractmethod
    def direction(self, value):
        pass

    @property
    @abstractmethod
    def next_direction(self):
        pass

    @next_direction.setter
    @abstractmethod
    def next_direction(self, value):
        pass


# Реализация игрового объекта
class GameObject(IGameObject):
    def __init__(self, position=None, body_color=BOARD_BACKGROUND_COLOR):
        if position is None:
            center_x = SCREEN_WIDTH // 2
            center_y = SCREEN_HEIGHT // 2
            self._position = (center_x // GRID_SIZE * GRID_SIZE,
                            center_y // GRID_SIZE * GRID_SIZE)
        else:
            self._position = position
        self.body_color = body_color

    @property
    def position(self):
        return self._position

    @position.setter
    def position(self, value):
        self._position = value

    def draw(self):
        pass


# Реализация еды
class Apple(IFood, GameObject):
    def __init__(self, body_color=APPLE_COLOR, position=None):
        super().__init__(position, body_color)
        if position is None:
            self.randomize_position()

    def randomize_position(self):
        self.position = (
            random.randint(0, GRID_WIDTH - 1) * GRID_SIZE,
            random.randint(0, GRID_HEIGHT - 1) * GRID_SIZE,
        )

    def draw(self):
        rect = pygame.Rect((self.position, (GRID_SIZE, GRID_SIZE)))
        pygame.draw.rect(screen, self.body_color, rect)
        pygame.draw.rect(screen, BORDER_COLOR, rect, 1)


# Реализация контролируемого объекта
class Snake(IControllable, GameObject):
    def __init__(
        self,
        length=1,
        direction=RIGHT,
        next_direction=None,
        body_color=SNAKE_COLOR,
        position=None,
    ):
        super().__init__(position, body_color)
        self.length = length
        self._direction = direction
        self._next_direction = next_direction if next_direction is not None else direction
        self.positions = [self.position]
        self.last = None

    @property
    def direction(self):
        return self._direction

    @direction.setter
    def direction(self, value):
        self._direction = value

    @property
    def next_direction(self):
        return self._next_direction

    @next_direction.setter
    def next_direction(self, value):
        self._next_direction = value

    def update_direction(self):
        if self.next_direction:
            self.direction = self.next_direction
            self.next_direction = None

    def move(self, food: IFood):
        if not self.positions:
            return

        head_x, head_y = self.positions[0]
        head_x += self.direction[0] * GRID_SIZE
        head_y += self.direction[1] * GRID_SIZE

        # Проверка границ
        head_x = head_x % SCREEN_WIDTH
        head_y = head_y % SCREEN_HEIGHT

        self.positions.insert(0, (head_x, head_y))

        # Проверка столкновения с собой
        if (head_x, head_y) in self.positions[1:]:
            self.reset()

        # Проверка съедания еды
        if (head_x, head_y) != food.position:
            self.positions.pop()
        else:
            self.length += 1
            food.randomize_position()

    def draw(self):
        for position in self.positions[:-1]:
            rect = pygame.Rect((position, (GRID_SIZE, GRID_SIZE)))
            pygame.draw.rect(screen, self.body_color, rect)
            pygame.draw.rect(screen, BORDER_COLOR, rect, 1)

        head_rect = pygame.Rect((self.positions[0], (GRID_SIZE, GRID_SIZE)))
        pygame.draw.rect(screen, self.body_color, head_rect)
        pygame.draw.rect(screen, BORDER_COLOR, head_rect, 1)

        if self.last:
            last_rect = pygame.Rect((self.last, (GRID_SIZE, GRID_SIZE)))
            pygame.draw.rect(screen, BOARD_BACKGROUND_COLOR, last_rect)

    def reset(self):
        self.length = 1
        self.positions = [self.position]
        self.last = None
        self.direction = random.choice([UP, DOWN, LEFT, RIGHT])


# Функция обработки клавиш
def handle_keys(controllable: IControllable):
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            raise SystemExit
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP and controllable.direction != DOWN:
                controllable.next_direction = UP
            elif event.key == pygame.K_DOWN and controllable.direction != UP:
                controllable.next_direction = DOWN
            elif event.key == pygame.K_LEFT and controllable.direction != RIGHT:
                controllable.next_direction = LEFT
            elif event.key == pygame.K_RIGHT and controllable.direction != LEFT:
                controllable.next_direction = RIGHT
            elif event.key == pygame.K_ESCAPE:
                pygame.quit()
                raise SystemExit


# Точка входа
def main():
    apple = Apple()
    snake = Snake(length=1)

    while True:
        handle_keys(snake)
        snake.update_direction()
        snake.move(apple)
        if not snake.positions:
            snake.reset()
            apple.randomize_position()
        screen.fill(BOARD_BACKGROUND_COLOR)
        if snake.positions:
            snake.draw()
            apple.draw()
        pygame.display.update()
        clock.tick(SPEED)


if __name__ == "__main__":
    main()
```  
Для реализации принципа инверсии зависимостей, заключающегося в обеспечении независимости верхних модулей от нижних, были введены интерфейсы IGameObject, IFood и IControllsble, связывающих классы между собой. Теперь класс Snake не зависит напрямую от класса GameObject, он реализует интерфейс IControllable, а класс Apple - интерфейс IFood. Это делает классы зависимыми не от конкретных классов, а от абстрактных.  
Принцип открытости/закрытости гласит, что  модуль должен быть расширяем без изменения кода данного модуля. В измененной программе the_snake_DIP_OCP_ISP.py это обеспечивается опять-таки за счет внедрения интерфейсов и использования их вместо конкретных экземпляров классов Snake и Apple. Функция handle_keys() принимает в качестве параметра не экземпляр класса Snake, а реализацию интерфейса IControllable. Это позволит в будущем добавить новый управляемый объект и внедрить его в код без надобности изменения модуля реализации обработки клавиш.  
Принцип раздедения интерфейсов заключается в создании нескольких маленьких узкоспециализированных интерфейсов заместо создания одного большого. Это позволяет реализовать в классах только необходимый функционал. В данной программе этот принцип соблюдается засчет раздедения возможного одного интерфейса на IGameObject, IFood и IControllable. Каждый из этих интефейсов требует реализации только необохдимых методов.  