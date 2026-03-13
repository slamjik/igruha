import random
from dataclasses import dataclass

import arcade
from arcade.particles import EmitMaintainCount, Emitter, FadeParticle
from pyglet.event import EVENT_HANDLE_STATE

# Окно и цвета
SCREEN_WIDTH, SCREEN_HEIGHT = 1200, 700
SCREEN_TITLE = "Falling Stars"
BACKGROUND_IMAGE = "earth_in_space.jpg"

# Сделаем набор текстур прямо в рантайме (быстро и дёшево)
SPARK_TEX = [
    arcade.make_circle_texture(4, arcade.color.WHITE),
    arcade.make_circle_texture(3, arcade.color.LIGHT_YELLOW),
    arcade.make_circle_texture(2, arcade.color.YELLOW),
]


def make_trail(attached_sprite, maintain=60):
    # «След за объектом»: поддерживаем постоянное число частиц
    emit = Emitter(
        center_xy=(attached_sprite.center_x, attached_sprite.center_y),
        emit_controller=EmitMaintainCount(maintain),
        particle_factory=lambda emitter: FadeParticle(
            filename_or_texture=random.choice(SPARK_TEX),
            change_xy=(random.uniform(-0.8, 0.8), random.uniform(-0.8, 0.8)),
            lifetime=random.uniform(0.4, 0.9),
            scale=random.uniform(0.2, 0.5),
            start_alpha=200,
            end_alpha=0,
        ),
    )
    # Хитрость: каждое обновление будем прижимать центр к спрайту
    emit.attached_sprite = attached_sprite
    return emit


@dataclass
class InputState:
    left: bool = False
    right: bool = False
    up: bool = False
    down: bool = False


class Star(arcade.Sprite):
    def __init__(self):
        super().__init__()
        self.texture = arcade.load_texture(":resources:images/items/star.png")
        self.scale = 0.3
        self.change_x = random.uniform(-2.5, 2.5)
        self.change_y = random.uniform(-6.5, -4.0)

    def update(self, delta_time: float = 1 / 60, *args, **kwargs) -> None:
        self.center_x += self.change_x
        self.center_y += self.change_y


class Playground(arcade.Window):
    def __init__(self, width, height, title):
        super().__init__(width, height, title)
        arcade.set_background_color(arcade.color.BLACK)

        self.background = self._load_background()
        self.background_sprite = arcade.Sprite()
        self.background_sprite.texture = self.background
        self.background_sprite.width = SCREEN_WIDTH
        self.background_sprite.height = SCREEN_HEIGHT
        self.background_sprite.center_x = SCREEN_WIDTH / 2
        self.background_sprite.center_y = SCREEN_HEIGHT / 2
        self.background_list = arcade.SpriteList()
        self.background_list.append(self.background_sprite)
        self.stars = arcade.SpriteList()
        self.emitters = []
        self.input_state = InputState()

    def _load_background(self):
        try:
            return arcade.load_texture(BACKGROUND_IMAGE)
        except FileNotFoundError:
            return arcade.load_texture(":resources:images/backgrounds/stars.png")

    def on_mouse_press(self, x: int, y: int, button: int, modifiers: int) -> EVENT_HANDLE_STATE:
        star = Star()
        star.center_x = x
        star.center_y = y
        self.stars.append(star)

        emitter = make_trail(star, maintain=60)
        self.emitters.append(emitter)
        return True

    # Логика
    def on_update(self, dt):
        # Движение «игрока»
        v = 280 * dt
        _ = v

        # Создаем копии списков для безопасной итерации
        for star in list(self.stars):
            star.update(dt)
            if star.right < 0 or star.top < 0 or star.left > SCREEN_WIDTH:
                star.remove_from_sprite_lists()

        # Удаляем помеченные спрайты
        # remove_from_sprite_lists уже убирает объект из self.stars

        # Обновляем эмиттеры и чистим «умершие»
        alive_emitters = []
        for emitter in self.emitters:
            attached = getattr(emitter, "attached_sprite", None)
            if attached is not None and attached in self.stars:
                emitter.center_x = attached.center_x
                emitter.center_y = attached.center_y
                emitter.update()
                alive_emitters.append(emitter)
            else:
                emitter.update()
                if len(emitter.particles) > 0:
                    alive_emitters.append(emitter)

        self.emitters = alive_emitters

    # Рендер
    def on_draw(self):
        self.clear()
        self.background_list.draw()
        self.stars.draw()
        for emitter in self.emitters:
            emitter.draw()


def setup_game(width=800, height=600, title="Falling Stars"):
    game = Playground(width, height, title)
    return game


def main():
    window = setup_game(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)
    arcade.run()


if __name__ == "__main__":
    main()
