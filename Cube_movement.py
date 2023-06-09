
from ursina import *

GRAVITY = -9.81

class Brick(Entity):
    def __init__(self, position, scale):
        super().__init__()
        self.model = "cube"
        self.color = color.gray
        self.texture = "white_cube"
        self.position = position
        self.scale = scale
        self.collider = "box"

class Player(Entity):
    def __init__(self, position=(0,0,0)):
        super().__init__()
        self.model='cube'
        self.color=color.orange
        self.texture = "white_cube"
        self.scale=(1, 1, 1)
        self.position=position
        self.collider = "box"
        self.direction = Vec3(0,0,0)
        self.speed = 3
        self.jump_speed = 6
        self.velocity = 0
        self.grounded = False
        

    def update(self):
        origin = self.world_position

        bottom_ray = raycast(origin , direction=Vec3(0,-1,0), ignore=[self,], distance=1, debug=False)

        if not self.grounded:
            self.velocity += GRAVITY * time.dt
            self.y += self.velocity * time.dt
            if bottom_ray.hit:
                self.y = self.position.y
                self.velocity = 0
                self.grounded = True
            elif self.y <= 0:
                self.y = 0
                self.velocity = 0
                self.grounded = True
        else:
            if not bottom_ray.hit:
                self.grounded = False
            if held_keys['space']:
                self.velocity = self.jump_speed
                self.grounded = False

        self.direction = Vec3(self.forward * (held_keys['w'] - held_keys['s'])).normalized()
        middle_ray = raycast(origin , self.direction, ignore=[self,], distance=.5, debug=False)

        if not middle_ray.hit:
            self.position += self.direction * self.speed * time.dt 
            if held_keys['d']:
                self.rotation_y += 90 * time.dt
            if held_keys['a']:
                self.rotation_y -= 90 * time.dt


app = Ursina()

# Setup Camera
camera.position=(0,20,-20)
camera.rotation_x = 45

cube = Brick((-3,0,0), (3,1,3))
cube1 = Brick((-2,2,4), (3,1,3))

player = Player()

app.run()
