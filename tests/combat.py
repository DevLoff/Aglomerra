import pygame
from modules.camera import Camera
from modules.player import Player
from modules.input import InputHandler
from modules.hitbox import Frame, Hitbox

def get_axis_l(polars):
    axis = pygame.Vector2(polars[0] - polars[1], polars[2] - polars[3])
    if axis.length() > 0:
        axis = axis.normalize()
    return axis

pygame.init()
SCREEN = pygame.display.set_mode((800, 600))

CLOCK = pygame.time.Clock()
INPUTS = InputHandler()
CAMERA = Camera(1)

player = Player()

running = True
while running:

    CLOCK.tick(60)
    EVENTS = pygame.event.get()

    INPUTS.update(EVENTS)

    for event in EVENTS:
        if event.type == pygame.QUIT:
            running = False

    if INPUTS.lookup(-1):
        frame = Frame((0,0))
        cur = frame
        for _ in range(10):
            cur.hitbox.append(Hitbox((0,0),20))
            cur.next = Frame((0,0))
            cur = cur.next
        player.move(frame)

    premove = get_axis_l([
            INPUTS.lookup(key) for key in [pygame.K_d, pygame.K_q, pygame.K_s, pygame.K_z]
    ]) * 10
    if premove.length() > 0:
        player.move(Frame(premove))

    player.update()

    CAMERA.clear_all()

    CAMERA.paint(player.image, player.rect.topleft)
    if player.action is not None:
        debugTex = player.action.tex()
        if debugTex is not None:
            CAMERA.paint(debugTex[0], player.rect.topleft-debugTex[1])

    CAMERA.draw(SCREEN,(0,0))
    pygame.display.flip()
