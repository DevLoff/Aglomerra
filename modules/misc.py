import pygame

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