import pygame

from modules.matrix import Matrix2
from modules.player import Player
from modules.input import InputHandler
from modules.camera import Camera
from modules.level import Level

pygame.init()

SCREEN = pygame.display.set_mode((800, 600))
CLOCK = pygame.time.Clock()
FONT = pygame.font.Font("ARIAL.TTF",20)

ML_run = True

INPUTBOARD = InputHandler()
SKEW = Matrix2(1/2,-1/2,1/4,1/4)
LEVEL = Level("levels/level01",SKEW)
player = Player()
CAMERA = Camera(2)

pygame.mixer.music.load("musics/main01.wav")
pygame.mixer.music.play(-1)

while ML_run:
    CLOCK.tick(60)

    events = pygame.event.get()
    INPUTBOARD.update(events)

    for event in events:
        if event.type == pygame.QUIT:
            ML_run = False

    if INPUTBOARD.lookup(pygame.K_SPACE):
        player.dash(INPUTBOARD)
    player.move(INPUTBOARD)
    player.update(LEVEL.area)

    LEVEL = LEVEL.switch(player)

    p_skewed = SKEW.mult(pygame.Vector2(player.rect.center))
    CAMERA.goto(p_skewed.x,p_skewed.y)

    position = FONT.render(f"{player.rect.center[0]}:{player.rect.center[1]}", True, (255,0,255))

    CAMERA.paint(LEVEL.surface,-LEVEL.center)
    CAMERA.paint(player.image,p_skewed + pygame.Vector2(25,-50),1)
    CAMERA.draw(SCREEN,(0,0))

    SCREEN.blit(position,(0,0))

    pygame.display.flip()

    CAMERA.clear_all()

pygame.quit()