import arcade
import random

# Константы
SCREEN_WIDTH = 1000
SCREEN_HEIGHT = 600
SCREEN_TITLE = "From the sound of hooves"
GRAVITY = 0.5
JUMP_SPEED = 10
MOVEMENT_SPEED = 5
SCALE = 1.0


class DustParticle(arcade.SpriteCircle):
    """Частица пыли для эффекта приземления"""
    def __init__(self, x, y):
        color = random.choice([
            (200, 200, 200, 200),
            (180, 180, 180, 200),
            (220, 220, 220, 200),
            (190, 170, 150, 200)
        ])
        size = random.randint(3, 8)
        super().__init__(size, color)
        self.center_x = x
        self.center_y = y
        self.change_x = random.uniform(-1.5, 1.5)
        self.change_y = random.uniform(0, 2)
        self.scale = 1.0
        self.alpha = 200
        self.lifetime = random.uniform(0.5, 1.2)
        self.time_alive = 0

    def update(self, delta_time):
        # Движение частицы
        self.center_x += self.change_x
        self.center_y += self.change_y

        # Замедление
        self.change_x *= 0.95
        self.change_y *= 0.95

        # Изменение масштаба
        self.scale_x *= 1.02
        self.scale_y *= 1.005

        # Уменьшение прозрачности
        self.alpha -= 2

        # Увеличение времени жизни
        self.time_alive += delta_time

        # Проверка на окончание времени жизни
        if self.time_alive >= self.lifetime or self.alpha <= 0:
            self.remove_from_sprite_lists()


class MyGame(arcade.Window):
    def __init__(self, width, height, title):
        super().__init__(width, height, title)

        # Спрайт-листы
        self.player_list = None
        self.tile_list = None
        self.dust_particles = None

        # Игрок
        self.player_sprite = None
        self.physics_engine = None

        # Состояние игры
        self.is_jumping = False
        self.was_jumping = False

        arcade.set_background_color(arcade.color.SKY_BLUE)

        self.idle_texture = arcade.load_texture(':resources:images/enemies/frog.png')
        self.jump_texture = arcade.load_texture(':resources:images/enemies/frog_move.png')

    def setup(self):
        """Настройка игры"""
        # Создаём спрайт-листы
        self.player_list = arcade.SpriteList()
        self.tile_list = arcade.SpriteList(use_spatial_hash=True)
        self.dust_particles = arcade.SpriteList()

        # Создаём игрока (лягушку)
        self.player_sprite = arcade.Sprite(scale=SCALE)
        self.player_sprite.texture = self.idle_texture
        self.player_sprite.center_x = 80
        self.player_sprite.center_y = 160
        self.player_list.append(self.player_sprite)

        # Создаём землю из тайлов травы
        tile_texture = arcade.load_texture(':resources:images/tiles/grassMid.png')
        tile_width = tile_texture.width

        for x in range(0, SCREEN_WIDTH + tile_width, tile_width):
            tile = arcade.Sprite(':resources:images/tiles/grassMid.png', SCALE)
            tile.left = x
            tile.bottom = 64
            self.tile_list.append(tile)

        # Создаём физический движок
        self.physics_engine = arcade.PhysicsEnginePlatformer(
            self.player_sprite,
            self.tile_list,
            gravity_constant=GRAVITY
        )

        # Состояние прыжка
        self.is_jumping = False
        self.was_jumping = False

    def on_draw(self):
        """Отрисовка"""
        self.clear()

        # Рисуем все спрайты
        self.tile_list.draw()
        self.player_list.draw()
        self.dust_particles.draw()

    def on_update(self, delta_time):
        """Логика игры"""
        self.physics_engine.update()
        self.dust_particles.update(delta_time)

        self.is_jumping = not self.physics_engine.can_jump()

        if self.is_jumping:
            self.player_sprite.texture = self.jump_texture
        else:
            self.player_sprite.texture = self.idle_texture

        if self.was_jumping and not self.is_jumping:
            self.create_dust_effect()

        self.was_jumping = self.is_jumping

    def create_dust_effect(self):
        """Создаёт эффект пыли при приземлении"""
        # Создаём 15-20 частиц пыли
        for _ in range(random.randint(15, 20)):
            particle = DustParticle(
                self.player_sprite.center_x,
                self.player_sprite.bottom
            )
            self.dust_particles.append(particle)

    def on_key_press(self, key, modifiers):
        """Обработка нажатия клавиш"""
        if key == arcade.key.LEFT:
            self.player_sprite.change_x = -MOVEMENT_SPEED
        elif key == arcade.key.RIGHT:
            self.player_sprite.change_x = MOVEMENT_SPEED
        elif key == arcade.key.SPACE and self.physics_engine.can_jump():
            self.player_sprite.change_y = JUMP_SPEED

    def on_key_release(self, key, modifiers):
        """Обработка отпускания клавиш"""
        if key in (arcade.key.LEFT, arcade.key.RIGHT):
            self.player_sprite.change_x = 0


def setup_game(width=1000, height=600, title="From the sound of hooves"):
    game = MyGame(width, height, title)
    return game


def main():
    """Главная функция"""
    window = setup_game(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)
    window.setup()
    arcade.run()


if __name__ == "__main__":
    main()