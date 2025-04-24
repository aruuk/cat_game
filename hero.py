import time
from pgzero.builtins import Actor, keyboard, sounds

class Hero:
    def __init__(self, pos):
        self.frames = [
            "sprite1", "sprite2", "sprite3", "sprite4", "sprite5",
            "sprite6", "sprite7", "sprite8", "sprite9", "sprite10"
        ]
        self.frame_index = 0
        self.actor = Actor(self.frames[self.frame_index], pos)
        self.speed = 4
        self.last_anim_time = time.time()
        self.lives = 3
        self.wall_cooldown = 0
        self.dx = 0
        self.score = 0

    def update(self):
        if time.time() - self.last_anim_time > 0.1:
            self.frame_index = (self.frame_index + 1) % len(self.frames)
            self.actor.image = self.frames[self.frame_index]
            self.last_anim_time = time.time()

        self.dx = 0
        if keyboard.left:
            self.dx = -self.speed
        elif keyboard.right:
            self.dx = self.speed

        self.actor.x += self.dx
        self.actor.y = 600 - self.actor.height

        now = time.time()
        bounced = False
        bounce_force = 10

        if self.actor.left < 0:
            self.actor.left = 0
            self.actor.x += bounce_force
            bounced = True
        elif self.actor.right > 800:
            self.actor.right = 800
            self.actor.x -= bounce_force
            bounced = True

        if bounced and now - self.wall_cooldown > 1:
            self.take_damage()
            sounds.hit.play()
            self.wall_cooldown = now

    def take_damage(self):
        if self.lives > 0:
            self.lives -= 1

    def draw(self):
        self.actor.draw()