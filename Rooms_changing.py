
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
    def __init__(self,position,buttonPos,delete_wall=False):
        self.open_gate = False
        self.x, self.y, self.z = position
        self.bx, self.by, self.bz = buttonPos

        # Floor
        self.Floor = Brick((self.x,self.y-2,self.z+1), (12,5,9), color.gray)

        # Gate Wall
        Gate_Wall((self.x+6,self.y+3.5,self.z+4))

        # # Gate
        self.Gate = Brick((self.x+6,self.y+2.5,self.z+1), (0.5,4,3), color.red)

        # Left Wall
        if delete_wall == False:
            Brick((self.x-6,self.y+3.5,self.z+1), (1,6,9), color.gray)

        # Back Wall
        Brick((self.x+0,self.y+3.5,self.z+6), (11,6,1), color.gray)

        # Button !!
        self.button = Button((self.bx, self.by, self.bz))

    def update(self):
        if self.open_gate and self.Gate.z < 3.5:
            self.Gate.z += time.dt
            self.button.color = color.rgb(0, 160, 0)


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
        self.room_ind = 0



    def update(self):
        if self.position.y < -10:
            self.position = (0,4,0)
        # taking distance (see)
        # hit_info_center = raycast(self.position, self.forward, distance=5, ignore=[self])
        # hit_info_right = raycast(self.position, self.right+self.forward, distance=5, ignore=[self])
        # hit_info_left = raycast(self.position, self.left+self.forward, distance=5, ignore=[self])

        # upper
        # hit_info_center = raycast(self.position, self.forward, distance=5, ignore=[self])
        # hit_info_right = raycast(self.position, self.right+self.forward, distance=5, ignore=[self])
        # hit_info_left = raycast(self.position, self.left+self.forward, distance=5, ignore=[self])

        # if hit_info_center.hit:
        #     distance_center = math.ceil(hit_info_center.distance)
        #     print(f"Center Distance: {distance_center}")
        # if hit_info_right.hit:
        #     distance_right = math.ceil(hit_info_right.distance)
        #     print(f"Right Distance: {distance_right}")
        # if hit_info_left.hit:
        #     distance_left = math.ceil(hit_info_left.distance)
        #     print(f"Left Distance: {distance_left}")
        
   
        # collision and movement
        origin = self.world_position
        bottom_ray = raycast(origin , direction=Vec3(0,-1,0), ignore=[self,], distance=.75, debug=False)

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

        # turning
        if not middle_ray.hit:
            self.position += self.direction * self.speed * time.dt 
            if held_keys['d']:
                self.rotation_y += 90 * time.dt
            if held_keys['a']:
                self.rotation_y -= 90 * time.dt

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

            # camera movement
            if bottom_ray.entity == room1.Floor and self.room_ind == 0:
                self.room_ind = 1
                self.camera_move()
            if bottom_ray.entity == room2.Floor and self.room_ind == 1:
                self.room_ind = 2
                self.camera_move()
            if bottom_ray.entity == room3.Floor and self.room_ind == 2:
                self.room_ind = 3
                self.camera_move()
            if bottom_ray.entity == room4.Floor and self.room_ind == 3:
                self.room_ind = 4
                self.camera_move()
        
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
room0 = ROOM((0,0,0), (3,0,3))
room1 = ROOM((x,0,0), (3+x,0,3), delete_wall=True)
room2 = ROOM((x*2,0,0), (3+x*2,0,3), delete_wall=True)
room3 = ROOM((x*3,0,0), (3+x*3,0,3), delete_wall=True)
room4 = ROOM((x*3,0,0), (3+x*3,0,3), delete_wall=True)# winning room

def update():
    room0.update()
    room1.update()
    room2.update()
    room3.update()





# Light and Shadow
# sunlight = DirectionalLight(y=10, color=color.white, shadows=True)
sunlight = DirectionalLight(y=10, color=color.white, shadows=True, shadow_resolution=1024)
ambient_light = AmbientLight(color=color.rgba(100, 100, 100, 0.5))

sunlight.parent = camera
ambient_light.parent = camera

# Setup Camera
camera.position=(0,13,-18)
camera.rotation_x = 30

app.run()
