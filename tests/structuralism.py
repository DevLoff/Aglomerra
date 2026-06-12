import pygame
import modules.structure as struct

pygame.init()
pygame.display.set_mode((800,600))

CLOCK = pygame.time.Clock()

root = struct.Node2D(0,0)

camera = struct.Camera(10,10,800,600)
root.add_child(camera)

player = struct.Char2D(0,0)
player_mesh = struct.Sprite(0,0,50,50)
player_mesh.set_tex(struct.gen_circle_tex(25,pygame.Color(0,0,255)))
player.add_child(player_mesh)
root.add_child(player)

hurtbox_offsets = [(0,0,20),(20,20,10)]
preset_hurtbox = [struct.Collider(x,y,r) for x,y,r in hurtbox_offsets]

npc = struct.Char2D(100,100)
root.add_child(npc)
npc.add_collider(struct.Collider(0,0,20),True,True)

running = True
while running:

    CLOCK.tick(60)
    events = pygame.event.get()
    for event in events:
        if event.type == pygame.QUIT:
            running = False

    collisions = [event for event in events if event.type == struct.CONNECTHIT]
    for collision in collisions:
        pos_diff = struct.sub_2d(collision.to.get_gl_pos(),collision.by.get_gl_pos())
        collision.to.move_pos(struct.normalized(pos_diff))

    player.extract_colliders()
    if pygame.mouse.get_pressed()[0]:
        player.add_colliders(preset_hurtbox,False,True)

    stick = (
            pygame.key.get_pressed()[pygame.K_d]-pygame.key.get_pressed()[pygame.K_q],
            pygame.key.get_pressed()[pygame.K_s]-pygame.key.get_pressed()[pygame.K_z]
    )
    stick = struct.normalized(stick)

    characters = struct.seek_typed_node(root, struct.Char2D)
    for char in characters:
        char.check_collision(characters)

    player.move_pos(struct.scale_2d(stick,10))

    for sprite in struct.seek_typed_node(root,struct.Sprite):
        camera.blit_sprite(sprite)
    camera.display_render(True)
    pygame.display.flip()
    camera.clear_render()