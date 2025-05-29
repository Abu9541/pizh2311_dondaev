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