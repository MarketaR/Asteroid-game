import pyglet
from pyglet import gl
from math import sin, cos
import math
import random

ROTATION_SPEED = 200
ACCELERATION = 300
ASTEROID_SPEED = 200


def load_image(path):
    image = pyglet.image.load(path)
    image.anchor_x = image.width // 2
    image.anchor_y = image.height // 2
    return image

asteroid_imgs = [
    load_image(
        "/Users/Marketa/pyladies/asteroidy/PNG/Meteors/meteorGrey_big1.png"),
    load_image(
        "/Users/Marketa/pyladies/asteroidy/PNG/Meteors/meteorGrey_big2.png"),
    load_image(
        "/Users/Marketa/pyladies/asteroidy/PNG/Meteors/meteorGrey_big3.png"),
    load_image(
        "/Users/Marketa/pyladies/asteroidy/PNG/Meteors/meteorGrey_big4.png")]

spaceship_img = load_image(
    "/Users/Marketa/pyladies/asteroidy/playerShip2_blue.png")

window = pyglet.window.Window()

pressed_keys = set()

batch = pyglet.graphics.Batch()


def draw_circle(x, y, radius):
    iterations = 20
    s = math.sin(2 * math.pi / iterations)
    c = math.cos(2 * math.pi / iterations)

    dx, dy = radius, 0

    gl.glBegin(gl.GL_LINE_STRIP)
    for i in range(iterations + 1):
        gl.glVertex2f(x + dx, y + dy)
        dx, dy = (dx * c - dy * s), (dy * c + dx * s)
    gl.glEnd()


def distance(a, b, wrap_size):
    """Distance in one dirextion (x or y)"""
    result = abs(a - b)
    if result > wrap_size / 2:
        result = wrap_size - result
    return result


def overlaps(a, b):
    """Returns true iff two space objects overlap"""
    distance_squared = (distance(a.x, b.x, window.width) ** 2 +
                        distance(a.y, b.y, window.height) ** 2)
    max_distance_squared = (a.radius + b.radius) ** 2
    return distance_squared < max_distance_squared


class SpaceObject:

    def __init__(self, window):
        self.x = window.width / 2
        self.y = window.height / 2
        self.rotation = 0
        self.x_speed = 0
        self.y_speed = 0
        self.rotation_speed = 0
        self.window = window
        self.radius = 30

    def draw(self):
        self.sprite.x = self.x
        self.sprite.y = self.y
        self.sprite.rotation = 90 - self.rotation

        draw_circle(self.x, self.y, self.radius)

    def tick(self, dt):

        distance_x = self.x_speed * dt
        distance_y = self.y_speed * dt
        self.x = self.x + distance_x
        self.y = self.y + distance_y
        self.rotation = self.rotation + self.rotation_speed * dt

        while self.x > self.window.width:
            self.x = self.x - self.window.width

        while self.x < 0:
            self.x = self.x + self.window.width

        while self.y > self.window.height:
            self.y = self.y - self.window.height

    def hit_by_spaceship(self, spaceship):
        pass


class Spaceship(SpaceObject):

    def __init__(self, window):
        super().__init__(window)
        self.sprite = pyglet.sprite.Sprite(spaceship_img, batch=batch)
        self.radius = 20

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

        super().tick(dt)

        for obj in objects:
            if overlaps(self, obj):
                obj.hit_by_spaceship(self)


class Asteroid(SpaceObject):

    def __init__(self, window):
        super().__init__(window)
        img = random.choice(asteroid_imgs)
        self.sprite = pyglet.sprite.Sprite(img, batch=batch)
        self.radius = 30

        if random.randrange(2) == 1:
            self.x = 0
            self.y = random.uniform(0, self.window.height)
        else:
            self.x = random.uniform(0, self.window.width)
            self.y = 0

        self.rotation_speed = random.uniform(-ROTATION_SPEED, ROTATION_SPEED)

        self.x_speed = random.uniform(-ASTEROID_SPEED, ASTEROID_SPEED)
        self.y_speed = random.uniform(-ASTEROID_SPEED, ASTEROID_SPEED)

    def hit_by_spaceship(self, spaceship):
        raise Exception("Game Over")

objects = []
objects.append(Spaceship(window))
objects.append(Asteroid(window))
objects.append(Asteroid(window))


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
