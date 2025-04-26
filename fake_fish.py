import random
from pgzero.builtins import Actor, sounds

class FakeFish:
    def __init__(self, maze, occupied_cells):
        self.frames = ['fish2']
        self.frame_index = 0
        self.actor = Actor(self.frames[self.frame_index])
        self.reset(maze, occupied_cells)
        self.anim_timer = 0

    def reset(self, maze, occupied_cells):
        # Ищем свободные клетки
        free_cells = [
            (col, row)
            for row in range(maze.rows)
            for col in range(maze.cols)
            if not maze.is_wall((col, row)) and (col, row) not in occupied_cells
        ]

        if not free_cells:
            raise Exception("Нет свободных клеток для фальшивой рыбы!")

        self.cell = random.choice(free_cells)
        occupied_cells.add(self.cell)

        self.actor.pos = maze.cell_to_pixel(self.cell)
        self.collected = False

    def update(self, player):
        self.anim_timer = (self.anim_timer + 1) % 6
        if self.anim_timer == 0:
            self.frame_index = (self.frame_index + 1) % len(self.frames)
            self.actor.image = self.frames[self.frame_index]

        if not self.collected and self.actor.colliderect(player.actor):
            self.collected = True
            player.score -= 1
            sounds.ffish.play()

    def draw(self):
        if not self.collected:
            self.actor.draw()
