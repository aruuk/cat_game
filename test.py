import pgzrun

WIDTH = 800
HEIGHT = 600

def draw():
    screen.clear()
    screen.draw.text("Привет, мир!", center=(WIDTH // 2, HEIGHT // 2), fontsize=60, color="white")

pgzrun.go()
