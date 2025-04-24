import random
from pgzero.builtins import Actor, sounds

class Fish:
    def __init__(self):
        self.actor = Actor("fish")
        self.reset_position()
        self.collected = False

    def reset_position(self):
        self.actor.x = random.randint(50, 750)
        self.actor.y = 550

    def reset(self):
        self.collected = False
        self.reset_position()

    def update(self, player):
        if not self.collected and self.actor.colliderect(player.actor):
            self.collected = True
            player.score += 1
            sounds.collect.play()

    def draw(self):
        if not self.collected:
            self.actor.draw()
