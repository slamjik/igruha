import arcade
import arcade.gui

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
SCREEN_TITLE = "Arcade Widgets Hero Selector"
MOVEMENT_SPEED = 4
ANIMATION_FRAME_DELAY = 10


class Hero:
    def __init__(self, idle_path: str, move_path: str, center_x: float, center_y: float, scale: float = 3.0):
        self.idle_texture = arcade.load_texture(idle_path)
        self.move_texture = arcade.load_texture(move_path)
        self.sprite = arcade.Sprite(center_x=center_x, center_y=center_y)
        self.sprite.textures = [self.idle_texture, self.move_texture]
        self.sprite.texture = self.idle_texture
        self.sprite.scale = scale


class MainWindow(arcade.Window):
    def __init__(self):
        super().__init__(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)
        arcade.set_background_color(arcade.color.GRAY)

        self.ui_manager = arcade.gui.UIManager()

        center_x = SCREEN_WIDTH / 2
        center_y = SCREEN_HEIGHT / 2 - 30

        self.heroes = {
            "Green Worm": Hero(
                ":resources:images/enemies/wormGreen.png",
                ":resources:images/enemies/wormGreen_move.png",
                center_x,
                center_y,
            ),
            "Slime Blue": Hero(
                ":resources:images/enemies/wormPink.png",
                ":resources:images/enemies/slimePurple.png",
                center_x,
                center_y,
            ),
            "Frog": Hero(
                ":resources:images/enemies/frog.png",
                ":resources:images/enemies/frog_move.png",
                center_x,
                center_y,
            ),
        }

        self.current_hero_name = "Green Worm"
        self.current_hero = self.heroes[self.current_hero_name]

        self.animation_frame_counter = 0
        self.animation_texture_index = 0

        self.left_pressed = False
        self.right_pressed = False
        self.up_pressed = False
        self.down_pressed = False

        self._setup_ui()

    def _setup_ui(self):
        self.ui_manager.enable()

        button_style = {
            "font_name": "Arial",
            "font_size": 14,
            "font_color": arcade.color.WHITE,
        }

        box = arcade.gui.UIBoxLayout(vertical=False, space_between=12)

        green_button = arcade.gui.UIFlatButton(text="Green Worm", width=150, **button_style)
        slime_button = arcade.gui.UIFlatButton(text="Slime Blue", width=150, **button_style)
        frog_button = arcade.gui.UIFlatButton(text="Frog", width=150, **button_style)

        @green_button.event("on_click")
        def _on_green_click(_event):
            self._switch_hero("Green Worm")

        @slime_button.event("on_click")
        def _on_slime_click(_event):
            self._switch_hero("Slime Blue")

        @frog_button.event("on_click")
        def _on_frog_click(_event):
            self._switch_hero("Frog")

        box.add(green_button)
        box.add(slime_button)
        box.add(frog_button)

        anchor = arcade.gui.UIAnchorWidget(anchor_x="center_x", anchor_y="top", child=box, align_y=-30)
        self.ui_manager.add(anchor)

    def _switch_hero(self, hero_name: str):
        old_x = self.current_hero.sprite.center_x
        old_y = self.current_hero.sprite.center_y
        self.current_hero_name = hero_name
        self.current_hero = self.heroes[hero_name]
        self.current_hero.sprite.center_x = old_x
        self.current_hero.sprite.center_y = old_y
        self.current_hero.sprite.texture = self.current_hero.sprite.textures[self.animation_texture_index]

    def on_draw(self):
        self.clear()
        self.ui_manager.draw()
        self.current_hero.sprite.draw()

    def on_update(self, delta_time: float):
        change_x = 0
        change_y = 0

        if self.left_pressed:
            change_x -= MOVEMENT_SPEED
        if self.right_pressed:
            change_x += MOVEMENT_SPEED
        if self.up_pressed:
            change_y += MOVEMENT_SPEED
        if self.down_pressed:
            change_y -= MOVEMENT_SPEED

        self.current_hero.sprite.center_x += change_x
        self.current_hero.sprite.center_y += change_y

        self.animation_frame_counter += 1
        if self.animation_frame_counter >= ANIMATION_FRAME_DELAY:
            self.animation_frame_counter = 0
            self.animation_texture_index = 1 - self.animation_texture_index
            self.current_hero.sprite.texture = self.current_hero.sprite.textures[self.animation_texture_index]

    def on_key_press(self, key: int, modifiers: int):
        if key == arcade.key.LEFT:
            self.left_pressed = True
        elif key == arcade.key.RIGHT:
            self.right_pressed = True
        elif key == arcade.key.UP:
            self.up_pressed = True
        elif key == arcade.key.DOWN:
            self.down_pressed = True

    def on_key_release(self, key: int, modifiers: int):
        if key == arcade.key.LEFT:
            self.left_pressed = False
        elif key == arcade.key.RIGHT:
            self.right_pressed = False
        elif key == arcade.key.UP:
            self.up_pressed = False
        elif key == arcade.key.DOWN:
            self.down_pressed = False


if __name__ == "__main__":
    window = MainWindow()
    arcade.run()
