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

npc = Player()
npc.rect.move_ip((100,100))

running = True
while running:

    CLOCK.tick(60)
    EVENTS = pygame.event.get()

    INPUTS.update(EVENTS)

    for event in EVENTS:
        if event.type == pygame.QUIT:
            running = False

    # PLAYER

    player.update()

    premove = get_axis_l([
        INPUTS.lookup(key) for key in [pygame.K_d, pygame.K_q, pygame.K_s, pygame.K_z]
    ])

    if INPUTS.lookup(-1):
        frame = Frame(premove*2)
        cur = frame
        for _ in range(30):
            cur.hitbox.append(Hitbox((0,0),20))
            cur.hurtbox.append(Hitbox((0, 10), 10))
            cur.draw()
            cur.next = Frame(premove*2)
            cur = cur.next
        player.move(frame)

    player.move(Frame(premove * 10))

    # NPC

    npc.update()
    frame = Frame((0,0))
    frame.hitbox.append(Hitbox((25,25), 40))
    frame.draw()
    npc.move(frame)

    # COLLISION

    if player.action is not None and npc.action is not None:
        for urbox in player.action.hurtbox:
            for ibox in npc.action.hitbox:
                if urbox.collide(ibox):
                    print("hit")

    # DISPLAY

    CAMERA.clear_all()

    CAMERA.paint(player.image, player.rect.topleft)
    if player.action is not None:
        if player.action.texture is not None:
            CAMERA.paint(player.action.texture, player.rect.topleft-player.action.offset)

    CAMERA.paint(npc.image, npc.rect.topleft)
    if npc.action.texture is not None:
        CAMERA.paint(npc.action.texture, npc.rect.topleft - npc.action.offset)

    CAMERA.draw(SCREEN,(0,0))
    pygame.display.flip()
