import pygame
import os
from network import Network
from settings.global_constants import window_heigth, window_width

# set global window settings
pygame.init()
width = window_width
height = window_heigth
win = pygame.display.set_mode((width, height))
pygame.display.set_caption("Client")
# print(pygame.display.list_modes())

# defines lists of images for the walking animation
SKIN_PATH = 'objects/statics/player/skin'  # get parent folder
walk_right = [pygame.image.load(os.path.join(SKIN_PATH, img)) for img in
                   ['R{}.png'.format(x) for x in range(1, 5)]]
walk_left = [pygame.image.load(os.path.join(SKIN_PATH, img)) for img in
                  ['L{}.png'.format(x) for x in range(1, 5)]]
char = pygame.image.load(os.path.join(SKIN_PATH, 'standing.png'))


def draw_player(plr, window):
    # if we move in the left direction display the image by index of walk_count // same for right
    if plr.position_map[0]:
        window.blit(walk_left[plr.walk_count], (plr.x, plr.y))

    elif plr.position_map[1]:
        window.blit(walk_right[plr.walk_count], (plr.x, plr.y))

    elif plr.position_map[2] or plr.position_map[3]:
        window.blit(char, (plr.x, plr.y))

    else:
        window.blit(char, (plr.x, plr.y))

    pygame.draw.rect(window, (255, 0, 0), plr.hitbox, 2)


def define_rect(rect_tuple):
    # (y, y, width, height)
    x = rect_tuple[0]
    y = rect_tuple[1]
    x2 = rect_tuple[0] + rect_tuple[2]
    y2 = rect_tuple[1] + rect_tuple[3]
    return x, y, x2, y2


def spell_hit(player, spell, player2):

    # rectangle of player it self
    x1, y1, x2, y2 = define_rect(player.hitbox)

    # rectangle of enemy player
    ex1, ey1, ex2, ey2 = define_rect(player2.hitbox)

    # this function checks if the player it self was hit by an enemy spell
    if (spell.x > x1) and (spell.x < x2) and (spell.y > y1) and (spell.y < y2):
        if spell.owner != player.id:
            player.hit(spell.damage)
            return True

    # this function checks if one of the own spells hits the enemy
    if (spell.x > ex1) and (spell.x < ex2) and (spell.y > ey1) and (spell.y < ey2):
        if spell.owner == player.id:
            player.spells.pop(player.spells.index(spell))


# draw the Window which we want to display
def draw_window(window, player, player2):
    win.fill((255, 255, 255))

    draw_player(player, window)
    draw_player(player2, window)

    # draw all the spells player one has casted
    for sp in player.spells + player2.spells:
        sp.update(spell_hit(player, sp, player2))
        sp.draw(window)

    pygame.display.update()


# Defines the main loop which runs until the program gets stopped
def run_game():
    run = True
    n = Network()
    player1 = n.getP()
    clock = pygame.time.Clock()

    while run:
        clock.tick(60)
        player2 = n.send(player1)

        # update the game window for each event // pygame specific
        for event in pygame.event.get():

            if event.type == pygame.MOUSEBUTTONUP:
                player1.target = pygame.mouse.get_pos()

            # if the event is equal to stop, then set run to false an quit the game
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()

        player1.move2()
        draw_window(win, player1, player2)


run_game()

