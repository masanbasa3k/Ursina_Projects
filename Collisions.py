from ursina import *

def update():
    global ball_speed
    ball.x += time.dt * ball_speed

    hit_info = ball.intersects()
    if hit_info.hit:
        ball_speed = -ball_speed

app = Ursina()

ball = Entity(model="sphere", color=color.orange, collider="box")
ball_speed = 2

box = Entity(model="cube", color=color.blue, texture="white_cube", scale=(1,2,1), position=(4,0,0), collider="box")
box = Entity(model="cube", color=color.blue, texture="white_cube", scale=(1,2,1), position=(-4,0,0), collider="box")

# Setup Camera
camera.position=(0,20,-20)
camera.rotation_x = 45

app.run()