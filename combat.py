phase_p1 = "stand"
phase_p2 = "stand"

actions = ["stun","stand","parry","ready","strick","dodge"]

def wincond(p1,p2):
    if p1 == "strick":
        if p2 == "stun" or p2 == "stand" or p2 == "ready":
            return True
    return False

def turn(p1,p2):
    if p1 == "parry" :
        if p2 == "strick":
            return "ready"
        return "stun"
    if p1 == "strick" :
        if p2 == "parry":
            return "stun"
        if p2 == "dodge" or p2 == "strick":
            return "stand"
    if p1 == "dodge":
        if p2 == "strick":
            return "ready"
        return "stand"
    if p1 == "stun":
        return "stand"
    return p1

def move(p1,opt):
    if p1 == "stand":
        if opt == 1:
            return "parry"
        if opt == 2:
            return "ready"
    if p1 == "ready":
        if opt == 1:
            return "dodge"
        if opt == 2:
            return "strick"
        if opt == 3:
            return "stand"
    return p1

while not(wincond(phase_p1,phase_p2) or wincond(phase_p2,phase_p1)):
    print(phase_p1,phase_p2)
    phase_p1 = move(phase_p1, int(input()))
    phase_p2 = move(phase_p2, int(input()))
    tmp = turn(phase_p1,phase_p2)
    phase_p2 = turn(phase_p2,phase_p1)
    phase_p1 = tmp