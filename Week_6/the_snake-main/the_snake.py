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
