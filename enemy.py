import time
import random
from pgzero.builtins import Actor, sounds

class Enemy:
    def __init__(self):
        self.frames = [f"bomb{i}" for i in range(1, 9)]
        self.explosion_frames = self.frames[::-1]
        self.frame_index = 0
        self.actor = Actor(self.frames[self.frame_index])
        self.actor.pos = (random.randint(50, 750), -50)
        self.speed = random.randint(2, 5)
        self.last_anim_time = time.time()
        self.exploding = False
        self.explode_start_time = None
        self.damaged_player = False

    def update(self):
        now = time.time()

        if self.exploding:
            if now - self.last_anim_time > 0.05:
                self.frame_index += 1
                if self.frame_index < len(self.explosion_frames):
                    self.actor.image = self.explosion_frames[self.frame_index]
                    self.last_anim_time = now
                else:
                    return False
            return True

        self.actor.y += self.speed

        if self.actor.y > 550:
            self.explode()
            return True

        return True

    def explode(self):
        if not self.exploding:
            self.exploding = True
            self.frame_index = 0
            self.actor.image = self.explosion_frames[self.frame_index]
            self.last_anim_time = time.time()
            sounds.explosion.play()

    def draw(self):
        self.actor.draw()
