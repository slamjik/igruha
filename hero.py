import random

import arcade
from arcade.gui import UIManager, UIAnchorLayout, UIBoxLayout, UILabel, UIDropdown
from pyglet.graphics import Batch

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
SCREEN_TITLE = "Choose Me"

PLAYER_SPEED = 5

TEXTURE_1 = ':resources:images/animated_characters/male_adventurer/maleAdventurer_idle.png'
TEXTURE_2 = ':resources:images/animated_characters/robot/robot_idle.png'
TEXTURE_3 = ':resources:images/animated_characters/zombie/zombie_idle.png'

MAP_NAME = ":resources:/tiled_maps/level_2.json"


class MenuView(arcade.View):
    def __init__(self):
        super().__init__()
        self.background_color = arcade.color.BLUE_GRAY

        self.batch = Batch()
        self.main_text = None
        self.space_text = None

        self.textures = [
            arcade.load_texture(TEXTURE_1),
            arcade.load_texture(TEXTURE_2),
            arcade.load_texture(TEXTURE_3)
        ]

        self.all_sprites = arcade.SpriteList()

        positions = [
            (SCREEN_WIDTH * 0.25, SCREEN_HEIGHT * 0.45),
            (SCREEN_WIDTH * 0.50, SCREEN_HEIGHT * 0.45),
            (SCREEN_WIDTH * 0.75, SCREEN_HEIGHT * 0.45),
        ]

        for i, pos in enumerate(positions):
            sprite = arcade.Sprite(scale=0.5)
            sprite.texture = self.textures[i]
            sprite.center_x, sprite.center_y = pos
            self.all_sprites.append(sprite)

        self.selected_texture = random.choice(self.textures)

        self.ui = UIManager()
        self.anchor = None
        self.option_list = ["Случайный", "Первый", "Второй", "Третий"]
        self.dropdown = None

    def on_show_view(self):
        self.main_text = arcade.Text(
            "Главное Меню",
            SCREEN_WIDTH / 2,
            SCREEN_HEIGHT - 60,
            arcade.color.WHITE,
            font_size=36,
            anchor_x="center",
            batch=self.batch
        )

        self.space_text = arcade.Text(
            "Выбери героя и нажми SPACE, чтобы начать!",
            SCREEN_WIDTH / 2,
            SCREEN_HEIGHT - 105,
            arcade.color.WHITE,
            font_size=18,
            anchor_x="center",
            batch=self.batch
        )

        self.ui.enable()

        self.anchor = UIAnchorLayout()
        v_box = UIBoxLayout(space_between=10)

        label = UILabel(
            text="Выбор героя:",
            font_size=18,
            text_color=arcade.color.WHITE
        )

        self.dropdown = UIDropdown(
            width=220,
            height=40,
            default="Случайный",
            options=self.option_list
        )
        self.dropdown.event = self.on_change

        v_box.add(label)
        v_box.add(self.dropdown)

        self.ui.add(
            self.anchor.add(
                child=v_box,
                anchor_x="center",
                anchor_y="bottom",
                align_y=40
            )
        )

    def on_hide_view(self):
        self.ui.disable()

    def on_change(self, event):
        value = event.new_value
        if value == "Первый":
            self.selected_texture = self.textures[0]
        elif value == "Второй":
            self.selected_texture = self.textures[1]
        elif value == "Третий":
            self.selected_texture = self.textures[2]
        else:
            self.selected_texture = random.choice(self.textures)

    def on_draw(self):
        self.clear()
        self.batch.draw()
        self.all_sprites.draw()
        self.ui.draw()

    def on_key_press(self, key, modifiers):
        if key == arcade.key.SPACE:
            game_view = GameView(self.selected_texture)
            self.window.show_view(game_view)


class GameView(arcade.View):
    def __init__(self, player_texture):
        super().__init__()
        arcade.set_background_color(arcade.color.BLUE_YONDER)

        tile_map = arcade.load_tilemap(MAP_NAME, scaling=0.5)
        self.scene = arcade.Scene.from_tilemap(tile_map)

        self.player = arcade.Sprite(scale=0.5)
        self.player.texture = player_texture
        self.player.center_x = 100
        self.player.center_y = 100

        if "Player" not in self.scene.name_mapping:
            self.scene.add_sprite("Player", self.player)
        else:
            self.scene["Player"].append(self.player)

        self.all_sprites = arcade.SpriteList()
        self.all_sprites.append(self.player)

        walls = arcade.SpriteList()
        if "Platforms" in self.scene.name_mapping:
            walls = self.scene["Platforms"]
        elif "Walls" in self.scene.name_mapping:
            walls = self.scene["Walls"]

        self.physics_engine = arcade.PhysicsEngineSimple(self.player, walls)

    def on_draw(self):
        self.clear()
        self.scene.draw()

    def on_update(self, delta_time):
        self.physics_engine.update()

    def on_key_press(self, key, modifiers):
        if key == arcade.key.LEFT:
            self.player.change_x = -PLAYER_SPEED
        elif key == arcade.key.RIGHT:
            self.player.change_x = PLAYER_SPEED
        elif key == arcade.key.UP:
            self.player.change_y = PLAYER_SPEED
        elif key == arcade.key.DOWN:
            self.player.change_y = -PLAYER_SPEED

    def on_key_release(self, key, modifiers):
        if key in (arcade.key.LEFT, arcade.key.RIGHT):
            self.player.change_x = 0
        elif key in (arcade.key.UP, arcade.key.DOWN):
            self.player.change_y = 0


def setup_game(width=800, height=600, title="Choose Me"):
    game = arcade.Window(width, height, title)
    return game


def main():
    window = setup_game(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)
    menu_view = MenuView()
    window.show_view(menu_view)
    arcade.run()


if __name__ == "__main__":
    main()