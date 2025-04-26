from pygame import Rect

class Maze:
    def __init__(self, map_data, screen_width, screen_height):
        self.map_data = map_data
        self.rows = len(map_data)
        self.cols = len(map_data[0])
        self.cell_size = min(screen_width // self.cols, screen_height // self.rows)
        
        # Вычисляем отступы для центрирования лабиринта
        maze_width = self.cols * self.cell_size
        maze_height = self.rows * self.cell_size
        self.offset_x = (screen_width - maze_width) // 2
        self.offset_y = (screen_height - maze_height) // 2

    def draw(self, screen):
        for row in range(self.rows):
            for col in range(self.cols):
                if self.map_data[row][col] == 0:
                    screen.draw.filled_rect(
                        Rect(
                            (self.offset_x + col * self.cell_size,
                             self.offset_y + row * self.cell_size),
                            (self.cell_size, self.cell_size)
                        ),
                        "darkgray"
                    )

    def cell_to_pixel(self, cell):
        col, row = cell
        x = self.offset_x + col * self.cell_size
        y = self.offset_y + row * self.cell_size
        return (x, y)

    def cell_to_pixel_center(self, cell):
        col, row = cell
        x = self.offset_x + col * self.cell_size + self.cell_size // 2
        y = self.offset_y + row * self.cell_size + self.cell_size // 2
        return (x, y)

    def pixel_to_cell(self, pos):
        x, y = pos
        col = int((x - self.offset_x) // self.cell_size)
        row = int((y - self.offset_y) // self.cell_size)
        return (col, row)

    def is_wall(self, cell):
        col, row = cell
        if 0 <= row < self.rows and 0 <= col < self.cols:
            return self.map_data[row][col] == 0
        return True  # Считаем всё вне лабиринта стенами

    def collides_with_wall(self, pos):
        col, row = self.pixel_to_cell(pos)
        return self.is_wall((col, row))

    def get_neighbors(self, cell):
        x, y = cell
        neighbors = [
            (x + 1, y),  # Right
            (x - 1, y),  # Left
            (x, y + 1),  # Down
            (x, y - 1),  # Up
        ]
        return [n for n in neighbors if not self.is_wall(n)]
