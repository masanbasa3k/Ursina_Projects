
from ursina import *

GRAVITY = -9.81

class Brick(Entity):
    def __init__(self, position, scale, c):
        super().__init__()
        self.model = "cube"
        self.color = c
        self.texture = "white_cube"
        self.position = position
        self.scale = scale
        self.collider = "box"

class Button(Entity):
    def __init__(self, position):
        super().__init__()
        self.model = "cube"
        self.color = color.green
        self.texture = "white_cube"
        self.position = position
        self.scale = (1,0.5,1)
        self.collider = "box"


class Player(Entity):
    def __init__(self, position=(0,4,0)):
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
        self.grounded = True

    def update(self):
        if self.intersects(button).hit and wallR.y < 5:
            wallR.y += time.dt * 1

        origin = self.world_position
        bottom_ray = raycast(origin , direction=Vec3(0,-1,0), ignore=[self,], distance=1, debug=False)

        if not self.grounded:
            self.velocity += GRAVITY * time.dt
            self.y += self.velocity * time.dt
            if bottom_ray.hit:
                self.y = self.position.y
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


# Light
# DirectionalLight(y=5, color=color.white, shadows=True)

# Setup Camera
camera.position=(0,23,-20)
camera.rotation_x = 45

flr = Brick((0,0,0), (11,1,6), color.gray)
wallB = Brick((0,2,3.5), (11,5,1), color.gray)
wallL = Brick((-6,2,0), (1,5,6), color.gray)
wallR = Brick((6,2,0), (1,5,6), color.gray)

button = Button((2,1,2))

player = Player()


app.run()
