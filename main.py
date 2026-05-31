import pygame
from matrix import Matrix2
import json

pygame.init()

SCREEN = pygame.display.set_mode((800, 600))
SCREEN_RECT = SCREEN.get_rect()
ML_run = True
CLOCK = pygame.time.Clock()
SPEED = 10
FONT = pygame.font.Font("ARIAL.TTF",20)

class InputHandler:
    def __init__(self):
        self.pressed = dict()
        self.clicked = dict()
        self.released = dict()
        self.comp = [self.pressed,self.clicked,self.released]

    def lookup(self,key,t=0):
        if key in self.comp[t]:
            return self.comp[t][key]
        return False

    def btn_down(self,key):
        self.clicked[key] = True
        self.pressed[key] = True

    def btn_up(self,key):
        self.released[key] = True
        self.pressed[key] = False

    def update(self,events):
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

INPUTBOARD = InputHandler()

def safe_subfill(canva,target):
    body = canva.get_rect()
    safe_target = target.clip(body)
    if body.contains(safe_target):
        return canva.subsurface(safe_target)
    return pygame.Surface((0,0))

def get_axis(x_po,x_ne,y_po,y_ne):
    axis = pygame.Vector2(x_po - x_ne, y_po - y_ne)
    if axis.length() > 0:
        axis = axis.normalize()
    return axis

def inside(collection,hitbox):
    cnt = 0
    for rect in collection:
        for point in [hitbox.topleft,hitbox.topright,hitbox.bottomleft,hitbox.bottomright]:
            if rect.collidepoint(point):
                cnt += 1
    if cnt == 4:
        return True
    return False

def string_sum(l):
    string = ""
    for line in l:
        string += line.strip()
    return string

def rect_goto(rect,pos):
    rect.move_ip(pos.x-rect.center[0],pos.y-rect.center[1])

TILESET = {
    "blue" : pygame.image.load("images/default_blue.png"),
    "sky" : pygame.image.load("images/default_sky.png"),
    "default" : pygame.image.load("images/default_tile.png")
}

BORDERS = []
SKEW = Matrix2(1/2,-1/2,1/4,1/4)

def load_level(filepath):
    BORDERS.clear()
    tiling = pygame.Surface((10000, 10000))
    lvl_read = open(filepath, 'r')
    raw_level = [item.split('|') for item in string_sum(lvl_read.readlines()).split(';')]
    lvl_read.close()
    for item in raw_level:
        x,y = item[1].split(',')
        BORDERS.append(pygame.Rect(int(x), int(y), 100, 100))
        item[1] = SKEW.mult(pygame.Vector2(int(x),int(y)))
    for item in sorted(raw_level,key=lambda x: x[1].y):
        tiling.blit(TILESET[item[0].strip()], item[1] + pygame.Vector2(5000,5000))
    return tiling

def decode_level(filepath):
    level_script = json.load(open(filepath))
    surface = pygame.Surface(level_script["size"])
    center = pygame.Vector2(surface.get_rect().center)
    for block in sorted(level_script["blocks"],key=lambda x: x["coord"][1]):
        surface.blit(TILESET[block["tag"]],pygame.Vector2(block["coord"]) + center)
    return surface



tiling = load_level("level.txt")

class Player:
    def __init__(self):
        self.image = pygame.Surface((50,50))
        self.image.fill((0,50,255))
        self.rect = pygame.Rect(0,0,50,50)
        self.speed = 10

    def move(self,inputs,borders):
        axis = get_axis(inputs.lookup(pygame.K_RIGHT),inputs.lookup(pygame.K_LEFT),inputs.lookup(pygame.K_DOWN),inputs.lookup(pygame.K_UP)).rotate(-45) * self.speed
        while not inside(borders,self.rect.move(axis)) and axis.length()>=1.0:
            axis *= 0.5
        if axis.length()>=1:
            self.rect.move_ip(axis)

player = Player()

class Camera:
    def __init__(self,n=1):
        size = pygame.display.get_surface().get_size()
        self.layers = [pygame.Surface(size)] + [pygame.Surface(size,pygame.SRCALPHA) for _ in range(n-1)]
        self.rect = pygame.Rect((0,0),size)

    def goto(self,x,y):
        self.rect.move_ip(x-self.rect.center[0],y-self.rect.center[1])

    def paint(self,surface,pos,layer=0):
        self.layers[layer].blit(surface, pygame.Vector2(pos) - pygame.Vector2(self.rect.topleft))

    def capture(self,surface,layer=0):
        to_be_blited = safe_subfill(surface,self.rect)
        print(to_be_blited.get_size())
        self.layers[layer].blit(to_be_blited, (0,0))

    def clear(self,layer=0):
        self.layers[layer].fill((0,0,0,0))

    def clear_all(self):
        for i in range(len(self.layers)):
            self.clear(i)

    def draw(self,surface,pos):
        for layer in self.layers:
            surface.blit(layer,pos)

CAMERA = Camera(2)

dialogs = []
txt_iter = 0
txt_display = pygame.Surface((0,0))
press_lag = False

def read_dialog(txt_reg,filepath):
    txt_reg.clear()
    txt_reader = open(filepath, 'r')
    for line in txt_reader.readlines():
        txt_reg.append(line.strip())
    txt_reader.close()

#read_dialog(dialogs,"dialog.txt")

npc_image = pygame.Surface((50,50))
npc_image.fill((255,0,0))
npc_range = pygame.Rect(100,-100,100,100)

while ML_run:
    CLOCK.tick(60)

    events = pygame.event.get()
    INPUTBOARD.update(events)

    for event in events:
        if event.type == pygame.QUIT:
            ML_run = False

    if txt_iter < len(dialogs):
        txt_display = FONT.render(dialogs[txt_iter], True, (255, 255, 255))
        if INPUTBOARD.lookup(pygame.K_a):
            if not press_lag:
                txt_iter += 1
            press_lag = True
        else:
            press_lag = False
    else :
        player.move(INPUTBOARD,BORDERS)

    if player.rect.colliderect(npc_range) and INPUTBOARD.lookup(pygame.K_f,1):
        print("interacted")
        rect_goto(player.rect,pygame.Vector2(150,150))
        tiling = load_level("level2.txt")

    p_skewed = SKEW.mult(pygame.Vector2(player.rect.center))
    CAMERA.goto(p_skewed.x,p_skewed.y)

    position = FONT.render(f"{player.rect.center[0]}:{player.rect.center[1]}", True, (255,0,255))

    CAMERA.paint(tiling,(-5000,-5000))
    CAMERA.paint(player.image,p_skewed + pygame.Vector2(25,-50),1)
    CAMERA.paint(npc_image,SKEW.mult(pygame.Vector2(npc_range.center)) + pygame.Vector2(25,-50),1)
    CAMERA.draw(SCREEN,(0,0))

    SCREEN.blit(position,(0,0))
    if txt_iter < len(dialogs):
        SCREEN.blit(txt_display,SCREEN_RECT.center)

    pygame.display.flip()

    CAMERA.clear_all()

pygame.quit()