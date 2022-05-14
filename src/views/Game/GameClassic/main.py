import arcade

class MenuMain(arcade.View):
    def __init__(self):
        super().__init__()

    def draw(self):
        self.clear()
        arcade.set_background_color(arcade.color.BLACK)
