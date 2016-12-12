import pyglet
from pyglet import gl
from math import sin, cos
import math

ROTATION_SPEED = 200
ACCELERATION = 300


def load_image(path):
    image = pyglet.image.load(
        "/Users/Marketa/pyladies/asteroidy/playerShip2_blue.png")
    image.anchor_x = image.width // 2
    image.anchor_y = image.height // 2
    return image

Spaceship_img = load_image(
    "/Users/Marketa/pyladies/asteroidy/playerShip2_blue.png")

window = pyglet.window.Window()

pressed_keys = set()

batch = pyglet.graphics.Batch()


class Spaceship:

    def __init__(self, window):
        self.sprite = pyglet.sprite.Sprite(Spaceship_img, batch=batch)
        self.x = window.width / 2
        self.y = window.height / 2
        self.rotation = 0
        self.x_speed = 0
        self.y_speed = 0
        self.window = window

    def draw(self):
        self.sprite.x = self.x
        self.sprite.y = self.y
        self.sprite.rotation = 90 - self.rotation

    def tick(self, dt):
        if pyglet.window.key.LEFT in pressed_keys:
            self.rotation = self.rotation - ROTATION_SPEED * dt
        if pyglet.window.key.RIGHT in pressed_keys:
            self.rotation = self.rotation + ROTATION_SPEED * dt
        if pyglet.window.key.UP in pressed_keys:
            rot = math.radians(self.rotation)
            self.x_speed = self.x_speed + dt * ACCELERATION * cos(rot)
            self.y_speed = self.y_speed + dt * ACCELERATION * sin(rot)
        if pyglet.window.key.DOWN in pressed_keys:
            rot = math.radians(self.rotation)
            self.x_speed = self.x_speed - dt * ACCELERATION * cos(rot)
            self.y_speed = self.y_speed - dt * ACCELERATION * sin(rot)

        distance_x = self.x_speed * dt
        distance_y = self.y_speed * dt
        self.x = self.x + distance_x
        self.y = self.y + distance_y

        while self.x > self.window.width:
            self.x = self.x - self.window.width

        while self.x < 0:
            self.x = self.x + self.window.width

        while self.y > self.window.height:
            self.y = self.y - self.window.height

        while self.y < 0:
            self.y = self.y + self.window.height

objects = []
objects.append(Spaceship(window))


def draw():
    window.clear()
    for obj in objects:
        obj.draw()

    for x in -window.width, 0, window.width:
        for y in -window.height, 0, window.height:
            gl.glPushMatrix()
            gl.glTranslatef(x, y, 0)
            batch.draw()
            gl.glPopMatrix()


def key_pressed(key, mod):
    pressed_keys.add(key)


def key_released(key, mod):
    pressed_keys.discard(key)

window.push_handlers(on_draw=draw, on_key_press=key_pressed,
                     on_key_release=key_released)


def tick(dt):
    for obj in objects:
        obj.tick(dt)

pyglet.clock.schedule_interval(tick, 1 / 30)

pyglet.app.run()
