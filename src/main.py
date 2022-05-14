import sys
sys.path.append("./views")

import arcade
from views.Menu.MenuMain.main import MenuMain

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
SCREEN_TITLE = "Cave game"

def main():
    """ Main function """
    window = arcade.Window(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)
    viewMenuMain = MenuMain()

    window.show_view(viewMenuMain)
    arcade.run()

if __name__ == "__main__":
    main()
