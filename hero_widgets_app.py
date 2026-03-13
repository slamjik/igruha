import arcade
import arcade.gui

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
SCREEN_TITLE = "Arcade Widgets Hero Selector"

MOVEMENT_SPEED = 4
ANIMATION_FRAME_DELAY = 10
HERO_SCALE = 2.5


class Hero:
    def __init__(
        self,
        idle_path: str,
        move_path: str,
        center_x: float,
        center_y: float,
        scale: float = HERO_SCALE,
    ):
        self.idle_texture = arcade.load_texture(idle_path)
        self.move_texture = arcade.load_texture(move_path)

        self.sprite = arcade.Sprite(
            self.idle_texture,
            center_x=center_x,
            center_y=center_y,
            scale=scale,
        )
        self.sprite.textures = [self.idle_texture, self.move_texture]
        self.sprite.texture = self.idle_texture


class MainWindow(arcade.Window):
    def __init__(self):
        super().__init__(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)
        arcade.set_background_color(arcade.color.GRAY)

        self.ui_manager = arcade.gui.UIManager()
        self.ui_manager.enable()

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

        self.hero_list = arcade.SpriteList()
        self.hero_list.append(self.current_hero.sprite)

        self.animation_frame_counter = 0
        self.animation_texture_index = 0

        self.left_pressed = False
        self.right_pressed = False
        self.up_pressed = False
        self.down_pressed = False

        self._setup_ui()

    def _setup_ui(self):
        button_box = arcade.gui.UIBoxLayout(vertical=False, space_between=12)

        green_button = arcade.gui.UIFlatButton(text="Green Worm", width=150)
        slime_button = arcade.gui.UIFlatButton(text="Slime Blue", width=150)
        frog_button = arcade.gui.UIFlatButton(text="Frog", width=150)

        @green_button.event("on_click")
        def on_green_click(event):
            self._switch_hero("Green Worm")

        @slime_button.event("on_click")
        def on_slime_click(event):
            self._switch_hero("Slime Blue")

        @frog_button.event("on_click")
        def on_frog_click(event):
            self._switch_hero("Frog")

        button_box.add(green_button)
        button_box.add(slime_button)
        button_box.add(frog_button)

        anchor_layout = arcade.gui.UIAnchorLayout()
        anchor_layout.add(
            child=button_box,
            anchor_x="center_x",
            anchor_y="top",
            align_y=-30,
        )

        self.ui_manager.add(anchor_layout)

    def _switch_hero(self, hero_name: str):
        old_x = self.current_hero.sprite.center_x
        old_y = self.current_hero.sprite.center_y

        self.current_hero_name = hero_name
        self.current_hero = self.heroes[hero_name]

        self.current_hero.sprite.center_x = old_x
        self.current_hero.sprite.center_y = old_y
        self.current_hero.sprite.texture = self.current_hero.sprite.textures[
            self.animation_texture_index
        ]

        self.hero_list = arcade.SpriteList()
        self.hero_list.append(self.current_hero.sprite)

    def on_draw(self):
        self.clear()
        self.ui_manager.draw()
        self.hero_list.draw()

    def on_update(self, delta_time: float):
        if self.left_pressed:
            self.current_hero.sprite.center_x -= MOVEMENT_SPEED
        if self.right_pressed:
            self.current_hero.sprite.center_x += MOVEMENT_SPEED
        if self.up_pressed:
            self.current_hero.sprite.center_y += MOVEMENT_SPEED
        if self.down_pressed:
            self.current_hero.sprite.center_y -= MOVEMENT_SPEED

        self._keep_hero_inside_window()

        self.animation_frame_counter += 1
        if self.animation_frame_counter >= ANIMATION_FRAME_DELAY:
            self.animation_frame_counter = 0
            self.animation_texture_index = 1 - self.animation_texture_index
            self.current_hero.sprite.texture = self.current_hero.sprite.textures[
                self.animation_texture_index
            ]

    def _keep_hero_inside_window(self):
        half_width = self.current_hero.sprite.width / 2
        half_height = self.current_hero.sprite.height / 2

        if self.current_hero.sprite.center_x < half_width:
            self.current_hero.sprite.center_x = half_width
        if self.current_hero.sprite.center_x > SCREEN_WIDTH - half_width:
            self.current_hero.sprite.center_x = SCREEN_WIDTH - half_width

        if self.current_hero.sprite.center_y < half_height:
            self.current_hero.sprite.center_y = half_height
        if self.current_hero.sprite.center_y > SCREEN_HEIGHT - half_height:
            self.current_hero.sprite.center_y = SCREEN_HEIGHT - half_height

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