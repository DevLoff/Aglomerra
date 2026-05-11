import pygame

def boot():
    pygame.init()
    pygame.display.set_mode((0,0), pygame.FULLSCREEN)
    loop()
    pygame.quit()

def loop():
    isInLoop = True
    while isInLoop:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                isInLoop = False