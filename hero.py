from pgzero.builtins import Actor
from pgzero.keyboard import keyboard

class Hero:
    def __init__(self, pos, maze):
        self.frames = [f"sprite{i}" for i in range(1, 4)] 
        self.frame_index = 0
        self.anim_timer = 0
        self.anim_speed = 5 

        self.actor: Actor = Actor(self.frames[self.frame_index], pos)
        self.maze = maze

        self.speed = 2
        self.score = 0
        self.lives = 3

        self.invincible = False
        self.invincible_timer = 0

    def update(self):
        self.handle_movement()
        self.update_animation()
        self.update_invincibility()

    def handle_movement(self):
        dx, dy = 0, 0
        if keyboard.left:
            dx -= self.speed
        if keyboard.right:
            dx += self.speed
        if keyboard.up:
            dy -= self.speed
        if keyboard.down:
            dy += self.speed

        next_pos = (self.actor.x + dx, self.actor.y + dy)

        if not self.maze.collides_with_wall(next_pos):
            self.actor.x += dx
            self.actor.y += dy

    def update_animation(self):
        self.anim_timer += 1
        if self.anim_timer >= self.anim_speed:
            self.anim_timer = 0
            self.frame_index = (self.frame_index + 1) % len(self.frames)
            self.actor.image = self.frames[self.frame_index]

    def update_invincibility(self):
        if self.invincible:
            self.invincible_timer -= 1
            if self.invincible_timer <= 0:
                self.invincible = False

    def draw(self):
        if not self.invincible or (self.invincible and (self.invincible_timer // 5) % 2 == 0):
            self.actor.draw()

    def take_damage(self):
        if not self.invincible:
            self.lives -= 1
            self.invincible = True
            self.invincible_timer = 60  # 60 кадров (~1 секунда при 60 FPS)
            if self.lives <= 0:
                print("Игра окончена!")

    def add_score(self):
        self.score += 1
