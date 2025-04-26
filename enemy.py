import random
import time
from pgzero.builtins import Actor, sounds

class Enemy:
    def __init__(self, maze, occupied_cells):
        self.frames = [f"bomb{i}" for i in range(1, 9)]
        self.explosion_frames = self.frames[::-1]
        self.frame_index = 0
        self.actor = Actor(self.frames[self.frame_index])

        # Выбираем свободную клетку
        free_cells = [
            (col, row)
            for row in range(maze.rows)
            for col in range(maze.cols)
            if not maze.is_wall((col, row)) and (col, row) not in occupied_cells
        ]

        if not free_cells:
            raise Exception("Нет свободных клеток для врагов!")

        self.cell = random.choice(free_cells)
        occupied_cells.add(self.cell)

        self.actor.pos = maze.cell_to_pixel(self.cell)

        self.last_anim_time = time.time()
        self.spawn_time = time.time()
        self.exploding = False
        self.damaged_player = False

    def update(self):
        now = time.time()

        # Бомба исчезает через 5 секунд
        if now - self.spawn_time > 5 and not self.exploding:
            self.explode()

        if self.exploding:
            if now - self.last_anim_time > 0.05:
                self.frame_index += 1
                if self.frame_index < len(self.explosion_frames):
                    self.actor.image = self.explosion_frames[self.frame_index]
                    self.last_anim_time = now
                else:
                    return False
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
