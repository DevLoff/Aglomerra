import pygame

class InputHandler:
    def __init__(self) -> None:
        self.pressed = dict()
        self.clicked = dict()
        self.released = dict()
        self.comp = [self.pressed,self.clicked,self.released]

    def lookup(self,key:int,t:int=0) -> bool:
        if key in self.comp[t]:
            return self.comp[t][key]
        return False

    def btn_down(self,key:int) -> None:
        self.clicked[key] = True
        self.pressed[key] = True

    def btn_up(self,key:int) -> None:
        self.released[key] = True
        self.pressed[key] = False

    def update(self,events:list[pygame.event.Event]) -> None:
        for item in self.clicked:
            self.clicked[item] = False
        for item in self.pressed:
            self.released[item] = False
        for event in events:
            if event.type == pygame.KEYDOWN:
                self.btn_down(event.key)
            if event.type == pygame.KEYUP:
                self.btn_up(event.key)
            if event.type == pygame.MOUSEBUTTONDOWN:
                self.btn_down(-1 * event.button)
            if event.type == pygame.MOUSEBUTTONUP:
                self.btn_up(-1 * event.button)