import random

import arcade
from arcade.gui import UIAnchorLayout, UIBoxLayout, UIDropdown, UILabel, UIManager
from pyglet.graphics import Batch

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
SCREEN_TITLE = "Choose Me"

PLAYER_SPEED = 5

TEXTURE_1 = ":resources:images/animated_characters/male_adventurer/maleAdventurer_idle.png"
TEXTURE_2 = ":resources:images/animated_characters/robot/robot_idle.png"
TEXTURE_3 = ":resources:images/animated_characters/zombie/zombie_idle.png"

MAP_NAME = ":resources:/tiled_maps/level_2.json"


class MenuView(arcade.View):
    def __init__(self):
        super().__init__()
        self.background_color = arcade.color.BLUE_GRAY

        self.batch = Batch()
        self.main_text = arcade.Text(
            "\u0413\u043b\u0430\u0432\u043d\u043e\u0435 \u041c\u0435\u043d\u044e",
            SCREEN_WIDTH / 2,
            SCREEN_HEIGHT - 60,
            arcade.color.WHITE,
            font_size=36,
            anchor_x="center",
            batch=self.batch,
        )
        self.space_text = arcade.Text(
            "\u0412\u044b\u0431\u0435\u0440\u0438 \u0433\u0435\u0440\u043e\u044f \u0438 \u043d\u0430\u0436\u043c\u0438 SPACE, \u0447\u0442\u043e\u0431\u044b \u043d\u0430\u0447\u0430\u0442\u044c!",
            SCREEN_WIDTH / 2,
            SCREEN_HEIGHT - 105,
            arcade.color.WHITE,
            font_size=18,
            anchor_x="center",
            batch=self.batch,
        )

        self.textures = [
            arcade.load_texture(TEXTURE_1),
            arcade.load_texture(TEXTURE_2),
            arcade.load_texture(TEXTURE_3),
        ]

        self.all_sprites = arcade.SpriteList()
        self.labels = []

        positions = [
            (SCREEN_WIDTH * 0.25, SCREEN_HEIGHT * 0.45),
            (SCREEN_WIDTH * 0.50, SCREEN_HEIGHT * 0.45),
            (SCREEN_WIDTH * 0.75, SCREEN_HEIGHT * 0.45),
        ]
        captions = [
            "\u041f\u0435\u0440\u0432\u044b\u0439",
            "\u0412\u0442\u043e\u0440\u043e\u0439",
            "\u0422\u0440\u0435\u0442\u0438\u0439",
        ]

        for index, pos in enumerate(positions):
            sprite = arcade.Sprite(scale=0.5)
            sprite.texture = self.textures[index]
            sprite.center_x, sprite.center_y = pos
            self.all_sprites.append(sprite)
            self.labels.append(
                arcade.Text(
                    captions[index],
                    pos[0],
                    pos[1] - 80,
                    arcade.color.WHITE,
                    font_size=16,
                    anchor_x="center",
                    batch=self.batch,
                )
            )

        self.selected_texture = random.choice(self.textures)

        self.ui = UIManager()
        self.option_list = [
            "\u0421\u043b\u0443\u0447\u0430\u0439\u043d\u044b\u0439",
            "\u041f\u0435\u0440\u0432\u044b\u0439",
            "\u0412\u0442\u043e\u0440\u043e\u0439",
            "\u0422\u0440\u0435\u0442\u0438\u0439",
        ]
        self.dropdown = None

    def on_show_view(self):
        self.ui.enable()
        self.ui.clear()

        anchor = UIAnchorLayout()
        v_box = UIBoxLayout(space_between=10)

        label = UILabel(
            text="\u0412\u044b\u0431\u043e\u0440 \u0433\u0435\u0440\u043e\u044f:",
            font_size=18,
            text_color=arcade.color.WHITE,
        )
        self.dropdown = UIDropdown(
            width=220,
            height=40,
            default=self.option_list[0],
            options=self.option_list,
        )
        self.dropdown.event("on_change")(self.on_change)

        v_box.add(label)
        v_box.add(self.dropdown)

        anchor.add(child=v_box, anchor_x="center", anchor_y="bottom", align_y=40)
        self.ui.add(anchor)

    def on_hide_view(self):
        self.ui.disable()

    def on_change(self, event):
        value = event.new_value
        if value == self.option_list[1]:
            self.selected_texture = self.textures[0]
        elif value == self.option_list[2]:
            self.selected_texture = self.textures[1]
        elif value == self.option_list[3]:
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

        self.all_sprites = arcade.SpriteList()
        self.all_sprites.append(self.player)
        self.scene.add_sprite("Player", self.player)

        walls = arcade.SpriteList()
        for layer_name in ("Platforms", "Walls"):
            try:
                walls = self.scene.get_sprite_list(layer_name)
                break
            except KeyError:
                continue

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
