
from ursina import *
import math

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

def Gate_Wall(position):
    x, y, z = position
    R = Brick((x,y,z), (1,6,3), color.gray)
    L = Brick((x,y,z-6), (1,6,3), color.gray)
    M = Brick((x,y+2,z-3), (1,2,3), color.gray)

class Button(Entity):
    def __init__(self, position):
        x, y, z = position
        super().__init__()
        self.model = "cube"
        self.color = color.rgb(0, 250, 0)
        self.texture = "white_cube"
        self.position = (x,y+0.4,z)
        self.scale = (1,0.7,1)
        self.collider = "box"

class ROOM():
    def __init__(self,position,buttonPos,delete_wall=True,delete_door=False):
        self.open_gate = False
        self.x, self.y, self.z = position
        self.bx, self.by, self.bz = buttonPos

        self.delete_wall=delete_wall
        self.delete_door=delete_door

        # Floor
        self.Floor = Brick((self.x,self.y-2,self.z+1), (12,5,9), color.gray)

        # Delete Gate wall and button
        if self.delete_door == False:
            # Gate Wall
            self.gate_wall = Gate_Wall((self.x+6,self.y+3.5,self.z+4))

            # # Gate
            self.Gate = Brick((self.x+6,self.y+2.5,self.z+1), (0.5,4,3), color.red)

            # Back Wall
            self. back_wall = Brick((self.x,self.y+3.5,self.z+6), (11,6,1), color.gray)

        # Button !!
        self.button = Button((self.bx, self.by, self.bz))

        # Left Wall
        if self.delete_wall == False:
            Brick((self.x-6,self.y+3.5,self.z+1), (1,6,9), color.gray)

        

        

    def update(self):
        if self.delete_door == False:
            if self.open_gate and self.Gate.z < 3.5:
                self.Gate.z += time.dt
                self.button.color = color.rgb(90, 90, 90)
            elif self.Gate.z > 1:
                self.Gate.z -= time.dt

class Player():
    def __init__(self, position=(0,4,0)):
        self.scale=(1, 1, 1)
        self.position=position

        self.model = Entity(model='cube', color=color.orange, scale=(1, 1, 1), texture = "white_cube", position=(0,4,0))

        self.x,self.y,self.z = position
        
        self.direction = Vec3(0,0,0)
        self.speed = 6
        self.jump_speed = 6
        self.velocity = 0
        self.grounded = True
        self.room_ind = 0

        # Eyes
        self.camera_pivot = Entity(parent=self.model, y=-0.1)
        self.eye_pivot = Entity(parent=self.camera_pivot, y=0.1, z=0.25)
        self.eye_left = Entity(parent=self.eye_pivot, x=-0.3, z=0.2, scale=0.4, model="sphere", color=color.white)
        self.eye_right = Entity(parent=self.eye_pivot, x=0.3, z=0.2, scale=0.4, model="sphere", color=color.white)

    def update(self):
        if self.y < -10:
            self.position = (0,4,0)
            
        origin = self.model.world_position
        bottom_ray = raycast(origin , direction=Vec3(0,-1,0), ignore=[self,], distance=.75, debug=False)

        if not self.grounded: 
            self.velocity += GRAVITY * time.dt
            self.model.y += self.velocity * time.dt
            if bottom_ray.hit:
                item_name = (bottom_ray.entity.__init__.__qualname__).split(".")[0]
                if item_name != "Player":
                    self.model.y = self.model.position.y
                    self.velocity = 0
                    self.grounded = True
        else:
            if not bottom_ray.hit:
                self.grounded = False
            if held_keys['space']:
                self.velocity = self.jump_speed
                self.grounded = False

        self.direction = Vec3(self.model.forward * (held_keys['w'] - held_keys['s'])).normalized()
        middle_ray = raycast(origin , self.direction, ignore=[self,], distance=.5, debug=False)
        #bunun z sini 0.5 artır azalt

        # turning
        if not middle_ray.hit:
            self.model.position += self.direction * self.speed * time.dt 
            if held_keys['d']:
                self.model.rotation_y += 100 * time.dt
            if held_keys['a']:
                self.model.rotation_y -= 100 * time.dt

        self.camera_pivot.rotation_y = (self.model.rotation_y/100)* time.dt
        self.eye_pivot.rotation_x = self.model.rotation_x
        self.eye_pivot.rotation_z = -self.model.rotation_z
 
        if bottom_ray.hit:
            # Pressing Buttons
            if bottom_ray.entity == room0.button and room0.open_gate == False:
                room0.open_gate = True
            if bottom_ray.entity == room1.button and room1.open_gate == False:
                room1.open_gate = True
            if bottom_ray.entity == room2.button and room2.open_gate == False:
                room2.open_gate = True
            if bottom_ray.entity == room3.button and room3.open_gate == False:
                room3.open_gate = True
            if bottom_ray.entity == room4.button and room4.open_gate == False:
                pass

            # camera movement
            if bottom_ray.entity == room1.Floor and self.room_ind == 0:
                self.room_ind = 1
                self.camera_move()
                room0.open_gate = False
            if bottom_ray.entity == room2.Floor and self.room_ind == 1:
                self.room_ind = 2
                self.camera_move()
                room1.open_gate = False
            if bottom_ray.entity == room3.Floor and self.room_ind == 2:
                self.room_ind = 3
                self.camera_move()
                room2.open_gate = False
            if bottom_ray.entity == room4.Floor and self.room_ind == 3:
                self.room_ind = 4
                self.camera_move()
                room3.open_gate = False
    
    def check_position(self, limit):
        if self.model != None and self.model.x > limit:
            self.model = None
    # CAM
    def camera_move(self):
        camera.animate_position(
            Vec3(camera.position.x + 12, camera.position.y, camera.position.z),
            duration=1,
            curve=curve.in_out_sine
        )

app = Ursina()


player = Player()

x=12
room0 = ROOM((0,0,0), (3,0,3),  delete_wall=False)
room1 = ROOM((x,0,0), (3+x,0,3))
room2 = ROOM((x*2,0,0), (3+x*2,0,3))
room3 = ROOM((x*3,0,0), (3+x*3,0,3))
room4 = ROOM((x*4,0,0), (3+x*4,0,3))

print("room 0 button y :")
print(room0.button.y)
# ROOM 1
room1_wall = Brick((12,1,1), (0.5,2,9), rgb(47,79,79))

# ROOM 2
room2_wall = Brick((26,1,4), (3,2,3), rgb(47,79,79))
room2.button.position = (26,1.9,4)

# ROOM 3
room3_wall = Brick((38,1,-1), (3,2,3), rgb(47,79,79))
room3_wall2 = Brick((34,1,2), (3,5,3), rgb(47,79,79))
room3.button.position = (34,3.5,2)

def update():
    room0.update()
    room1.update()
    room2.update()
    room3.update()
    room4.update()

        
    player.update()

        

# Light and Shadow
# sunlight = DirectionalLight(y=10, color=color.white, shadows=True)
sunlight = DirectionalLight(y=10, color=color.white, shadows=True, shadow_resolution=1024)
ambient_light = AmbientLight(color=color.rgba(100, 100, 100, 0.5))

sunlight.parent = camera
ambient_light.parent = camera

# # Setup Camera
camera.position=(0,13,-18)
camera.rotation_x = 30



app.run()
