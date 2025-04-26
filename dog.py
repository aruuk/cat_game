import random
from pgzero.builtins import Actor, sounds
from collections import deque

class Dog:
    def __init__(self, pos, maze):
        self.frames = [f"dog{i}" for i in range(1, 5)]
        self.frame_index = 0
        self.actor = Actor(self.frames[self.frame_index], pos)
        self.speed = 1 
        self.anim_timer = 0
        self.start_pos = pos
        self.maze = maze
        self.path = []

    def update(self, player):
        self.anim_timer = (self.anim_timer + 1) % 10
        if self.anim_timer == 0:
            self.frame_index = (self.frame_index + 1) % len(self.frames)
            self.actor.image = self.frames[self.frame_index]

        if self.anim_timer == 0:
            self.find_path_to_player(player)

        if self.path:
            next_cell = self.path[0]
            next_pixel = self.maze.cell_to_pixel_center(next_cell)

            dx = next_pixel[0] - self.actor.x
            dy = next_pixel[1] - self.actor.y

            if abs(dx) < self.speed and abs(dy) < self.speed:
                self.actor.pos = next_pixel
                self.path.pop(0)
            else:
                move_x = self.speed if dx > 0 else -self.speed
                move_y = self.speed if dy > 0 else -self.speed

                if abs(dx) > abs(dy):
                    self.actor.x += move_x
                else:
                    self.actor.y += move_y

        if self.actor.colliderect(player.actor):
            player.take_damage()
            self.reset_position()
            sounds.bark.play()

    def find_path_to_player(self, player):
        start_cell = self.maze.pixel_to_cell(self.actor.pos)
        target_cell = self.maze.pixel_to_cell(player.actor.pos)

        queue = deque()
        queue.append((start_cell, []))
        visited = set()
        visited.add(start_cell)

        while queue:
            current, path = queue.popleft()

            if current == target_cell:
                self.path = path
                return

            for neighbor in self.get_neighbors(current):
                if neighbor not in visited:
                    visited.add(neighbor)
                    queue.append((neighbor, path + [neighbor]))

        self.path = []

    def get_neighbors(self, cell):
        x, y = cell
        neighbors = [
            (x + 1, y),
            (x - 1, y),
            (x, y + 1),
            (x, y - 1),
        ]
        return [n for n in neighbors if not self.maze.is_wall(n)]

    def reset_position(self):
        self.actor.pos = self.start_pos
        self.path = []

    def draw(self):
        self.actor.draw()
