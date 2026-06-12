from pygame import Surface, image, transform, display, draw, Color, SRCALPHA, event

type Num = int|float
type Point2D = tuple[Num, Num]
type GlNode = Node|Phy2D

class Node:
    def __init__(self):
        self.parent = None
        self.children = []

    def add_child(self, node:GlNode):
        node.parent = self
        self.children.append(node)

    def get_children(self) -> list[GlNode]:
        return self.children

    def clear(self) -> None:
        self.parent = None
        self.children = []

def add_2d(t1:Point2D,t2:Point2D) -> Point2D:
    return t1[0]+t2[0],t1[1]+t2[1]
def sub_2d(t1:Point2D,t2:Point2D) -> Point2D:
    return t1[0]-t2[0],t1[1]-t2[1]
def scale_2d(t:Point2D,q:Num) -> Point2D:
    return t[0]*q,t[1]*q
def norm_2d(t:Point2D, d:int = 2) -> float:
    if d == 0:
        return max(abs(t[0]),abs(t[1]))
    return (abs(t[0])**d + abs(t[1])**d)**(1/d)

def normalized(t:Point2D, d:int = 2) -> Point2D:
    norm = norm_2d(t, d)
    if norm > 0.1:
        return scale_2d(t, 1 / norm)
    return t

class Node2D(Node):
    def __init__(self, x:Num, y:Num) -> None:
        super().__init__()
        self.x,self.y = 0,0
        self.set_pos(x,y)

    def get_rel_pos(self) -> Point2D:
        return self.x, self.y
    def get_gl_pos(self) -> Point2D:
        if isinstance(self.parent,Phy2D):
            return add_2d(self.parent.get_gl_pos(),self.get_rel_pos())
        return self.get_rel_pos()

    def set_pos(self, x:Num|Point2D, y:Num=0) -> None:
        if type(x) is tuple:
            self.x,self.y = x
        else:
            self.x = x
            self.y = y
    def move_pos(self, x:Num|Point2D, y:Num=0) -> None:
        if type(x) is tuple:
            self.set_pos(add_2d((self.x,self.y),x))
        else:
            self.set_pos(x+self.x,y+self.y)

class Rect(Node2D):
    def __init__(self, x:Num, y:Num, w:Num, h:Num) -> None:
        super().__init__(x,y)
        self.span = Node2D(w,h)

    def get_size(self) -> Point2D:
        return self.span.get_rel_pos()

class Sprite(Rect):
    def __init__(self, x:Num, y:Num, w:Num, h:Num) -> None:
        super().__init__(x, y, w, h)
        self.tex = None
        self.render = Surface(self.get_size(),SRCALPHA)

    def gen_render(self) -> None:
        self.render = Surface(self.get_size(), SRCALPHA)
        if self.tex is not None:
            self.render.blit(transform.scale(self.tex,self.get_size()),(0,0))

    def get_tex_cntr(self) -> Point2D:
        return scale_2d(self.get_size(),0.5)
    def get_cntr_pos(self) -> Point2D:
        return sub_2d(self.get_gl_pos(),self.get_tex_cntr())

    def load_tex(self, filepath: str) -> None:
        self.tex = image.load(filepath)
        self.gen_render()
    def set_tex(self, surface: Surface) -> None:
        self.tex = surface.copy()
        self.gen_render()
    def resize(self, nsize : Point2D) -> None:
        self.span.set_pos(nsize)
        self.gen_render()

    def get_image(self) -> Surface:
        return self.render

def gen_circle_tex(radius:Num, hue:Color):
    cntr = (radius,radius)
    tex = Surface(scale_2d(cntr,2),SRCALPHA)
    draw.circle(tex,hue,cntr,radius)
    return tex

class Camera(Rect):
    def __init__(self, x:Num, y:Num, w:Num, h:Num) -> None:
        super().__init__(x,y,w,h)
        self.render = Surface(self.get_size())

    def blit_sprite(self, sprite:Sprite) -> None:
        self.render.blit(sprite.get_image(),sub_2d(sprite.get_cntr_pos(),self.get_gl_pos()))
    def display_render(self, keep_res:bool = False) -> None:
        window = display.get_surface()
        if keep_res:
            window.blit(self.render, (0, 0))
        else:
            screen_size, canva_size = window.get_size(), self.render.get_size()
            window.blit(transform.scale_by(self.render,min(screen_size[0]/canva_size[0],screen_size[1]/canva_size[1])),(0,0))
    def clear_render(self) -> None:
        self.render.fill((0,0,0))

type Collidable = Collider
class Collider(Node2D):
    def __init__(self, x:Num, y:Num, r:Num, d:Num = 2) -> None:
        super().__init__(x,y)
        self.radius = r
        self.norm_dim = d

    def copy(self) -> Collidable:
        return Collider(self.x,self.y,self.radius,self.norm_dim)

    def gen_visual(self, color:Color) -> None:
        mesh = Sprite(0,0,self.radius*2,self.radius*2)
        mesh.set_tex(gen_circle_tex(self.radius,color))
        self.add_child(mesh)

    def collide(self, node:Collidable) -> bool:
        return norm_2d(sub_2d(node.get_gl_pos(),self.get_gl_pos()),self.norm_dim) < self.radius+node.radius

CONNECTHIT = event.custom_type()

type Vulnerable = Char2D
class Char2D(Node2D):
    def __init__(self, x:Num, y:Num) -> None:
        super().__init__(x,y)
        self.hitbox = []
        self.hurtbox = []

    def add_collider(self, collider:Collider, ishit:bool, isvisible:bool = False) -> None:
        doble = collider.copy()
        doble.parent = self
        if ishit:
            if isvisible:
                doble.gen_visual(Color(255,0,0,150))
            self.hitbox.append(doble)
        else:
            if isvisible:
                doble.gen_visual(Color(255,255,255,150))
            self.hurtbox.append(doble)

    def add_colliders(self, transfer:list[Collider], ishit:bool, isvisible:bool = False) -> None:
        for collider in transfer:
            self.add_collider(collider, ishit, isvisible)
    def extract_colliders(self):
        for collider in self.hitbox+self.hurtbox:
            collider.clear()
        tmp = self.hitbox,self.hurtbox
        self.hitbox,self.hurtbox = [],[]
        return tmp

    def node_collide(self, node:Vulnerable) -> bool:
        for hurt in self.hurtbox:
            for hit in node.hitbox:
                if hit.collide(hurt):
                    event.post(event.Event(CONNECTHIT,{"by":self,"to":node,"with":hurt,"at":hit}))
                    return True
        return False

    def check_collision(self, group:list[Vulnerable]) -> None:
        for node in group:
            self.node_collide(node)

    def get_children(self) -> list[GlNode]:
        return self.children + self.hitbox + self.hurtbox

def seek_typed_node(root:GlNode,typed:type) -> list:
    nodes = []
    if type(root) is typed:
        nodes.append(root)
    for child in root.get_children():
        nodes += seek_typed_node(child,typed)
    return nodes


Phy2D = Node2D|Rect|Sprite|Camera|Collider|Char2D