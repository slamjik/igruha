import arcade
import random
import math
from pyglet.graphics import Batch

# Константы
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
SCREEN_TITLE = "Побежали!"
TILE_SIZE = 64
GRAVITY = 0.5
JUMP_SPEED = 15
MOVEMENT_SPEED = 5
CAMERA_LERP = 0.12


class GreenSparkParticle(arcade.SpriteCircle):
    """Частица зелёной искры"""

    def __init__(self, x, y):
        color = random.choice([
            (100, 255, 100, 255),
            (50, 255, 50, 255),
            (150, 255, 150, 255),
            (200, 255, 200, 255),
            (100, 200, 100, 255)
        ])
        size = random.randint(3, 6)
        super().__init__(size, color)

        self.center_x = x
        self.center_y = y

        angle = random.uniform(0, 2 * math.pi)
        speed = random.uniform(2, 7)
        self.change_x = math.cos(angle) * speed
        self.change_y = math.sin(angle) * speed

        self.alpha = 255
        self.lifetime = random.uniform(0.3, 0.8)
        self.time_alive = 0

    def update(self, delta_time):
        # Движение с учетом гравитации
        self.change_y -= 0.15
        self.center_x += self.change_x
        self.center_y += self.change_y

        # Уменьшение прозрачности и размера
        self.alpha = max(0, self.alpha - 8)
        self.scale_x *= 0.97
        self.scale_y *= 0.97

        # Увеличение времени жизни
        self.time_alive += delta_time

        # Удаление частицы по истечении времени жизни
        if self.time_alive >= self.lifetime or self.alpha <= 0:
            self.remove_from_sprite_lists()


class Player(arcade.Sprite):
    def __init__(self):
        self.walk_textures = [
            arcade.load_texture(":resources:images/alien/alienBlue_walk1.png"),
            arcade.load_texture(":resources:images/alien/alienBlue_walk2.png"),
        ]
        super().__init__(self.walk_textures[0], scale=1.6)

        self.texture = self.walk_textures[0]
        self.center_y = TILE_SIZE + self.height / 2
        self.change_x = 0
        self.change_y = 0
        self.animation_timer = 0
        self.current_texture = 0
        self.is_jumping = False

    def update(self, delta_time):
        # Гравитация
        self.change_y -= GRAVITY

        # Обновление позиции
        self.center_y += self.change_y

        # Анимация ходьбы
        self.animation_timer += delta_time
        if self.animation_timer >= 0.12:
            self.animation_timer = 0
            self.current_texture = (self.current_texture + 1) % len(self.walk_textures)
            self.texture = self.walk_textures[self.current_texture]

        # Проверка, чтобы персонаж не упал ниже земли
        ground_y = TILE_SIZE + self.height / 2
        if self.center_y <= ground_y:
            self.center_y = ground_y
            self.change_y = 0
            self.is_jumping = False

    def jump(self):
        if not self.is_jumping:
            self.change_y = JUMP_SPEED
            self.is_jumping = True


class GameWindow(arcade.Window):
    def __init__(self, width, height, title):
        super().__init__(width, height, title)
        self.background_color = arcade.color.SKY_BLUE

        # Спрайты
        self.player = None
        self.tile_list = None
        self.cactus_list = None
        self.spark_particles = None
        self.physics_engine = None
        self.player_list = None

        # Камера
        self.world_camera = None
        self.gui_camera = None

    def setup(self):
        # Инициализация игрока
        self.player = Player()
        self.player.center_x = self.width // 3

        # Создание списков спрайтов
        self.tile_list = arcade.SpriteList()
        self.cactus_list = arcade.SpriteList()
        self.player_list = arcade.SpriteList()
        self.spark_particles = arcade.SpriteList()

        self.player_list.append(self.player)

        self.world_camera = None
        self.gui_camera = None

        # Создание земли из тайлов
        for x in range(-TILE_SIZE, self.width + TILE_SIZE * 3, TILE_SIZE):
            tile = arcade.Sprite(
                ":resources:images/tiles/brickTextureWhite.png",
                center_x=x + TILE_SIZE / 2,
                center_y=TILE_SIZE / 2
            )
            self.tile_list.append(tile)

        # Размещение кактусов
        cactus_x = self.width + 250
        for _ in range(7):
            cactus = arcade.Sprite(":resources:images/tiles/cactus.png", scale=1.0)
            cactus.center_x = cactus_x
            cactus.center_y = TILE_SIZE + cactus.height / 2 - 4
            self.cactus_list.append(cactus)
            cactus_x += random.randint(220, 420)

        # Физический движок
        self.physics_engine = None

    def on_draw(self):
        self.clear()

        # Активация камеры
        # Камера тут не используется, потому что мир просто прокручивается влево

        # Отрисовка спрайтов
        self.tile_list.draw()
        self.cactus_list.draw()
        self.player_list.draw()
        self.spark_particles.draw()

    def create_green_sparks(self, x, y):
        """Создаёт эффект зелёных искр"""
        for _ in range(28):
            self.spark_particles.append(GreenSparkParticle(x, y))

    def _recycle_tiles(self):
        rightmost_x = max(tile.center_x for tile in self.tile_list)
        for tile in self.tile_list:
            if tile.right < 0:
                tile.center_x = rightmost_x + TILE_SIZE
                rightmost_x = tile.center_x

    def _recycle_cactus(self, cactus):
        rightmost_x = max(other.center_x for other in self.cactus_list)
        cactus.center_x = rightmost_x + random.randint(220, 420)
        cactus.center_y = TILE_SIZE + cactus.height / 2 - 4

    def on_update(self, delta_time):
        # Обновление игрока
        self.player.update(delta_time)

        # Обновление физики
        for tile in self.tile_list:
            tile.center_x -= MOVEMENT_SPEED

        for cactus in self.cactus_list:
            cactus.center_x -= MOVEMENT_SPEED

        self._recycle_tiles()

        for cactus in self.cactus_list:
            if cactus.right < 0:
                self._recycle_cactus(cactus)

        # Проверка столкновений с кактусами
        hit_list = arcade.check_for_collision_with_list(self.player, self.cactus_list)
        for cactus in hit_list:
            self.create_green_sparks(cactus.center_x, cactus.center_y + cactus.height / 4)
            self._recycle_cactus(cactus)

        # Обновление частиц
        for particle in list(self.spark_particles):
            particle.update(delta_time)

        # Настройка камеры
        # В этой версии не нужна

    def on_key_press(self, key, modifiers):
        if key == arcade.key.SPACE:
            self.player.jump()


def setup_game(width=1000, height=600, title="Побежали!"):
    game = GameWindow(width, height, title)
    game.setup()
    return game


def main():
    window = setup_game(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)
    arcade.run()


if __name__ == "__main__":
    main()