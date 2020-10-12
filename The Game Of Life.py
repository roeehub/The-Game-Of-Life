
""" The main script of the game """

import game


game = game.Game()
game.running = True
while game.running:
    res = game.curr_menu.display_menu()
    if res == -1:
        game.quit()
        break
    elif game.playing:
        game.game_loop()
        game.reset_game()
