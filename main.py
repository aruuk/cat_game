import pgzrun
from hero import Hero
from enemy import Enemy
from fish import Fish
from fake_fish import FakeFish
from dog import Dog
from maze import Maze
from pgzero.builtins import Actor, sounds, music

WIDTH = 1200
HEIGHT = 700

maze_map = [
    [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
    [0,1,1,1,1,1,1,1,1,1,1,1,1,1,0,1,1,1,1,0],
    [0,1,1,1,1,1,1,1,1,1,1,1,1,1,0,1,1,1,1,0],
    [0,1,1,1,1,1,1,1,1,1,1,1,1,1,0,1,1,0,0,0],
    [0,1,1,1,0,1,1,0,0,0,0,1,1,1,1,1,1,1,1,0],
    [0,1,1,1,0,1,1,1,1,1,0,1,1,1,1,1,1,1,1,0],
    [0,1,1,1,0,1,1,1,1,1,0,1,1,1,1,1,1,1,1,0],
    [0,1,1,1,0,1,1,1,1,1,0,1,1,1,1,1,1,1,1,0],
    [0,1,1,1,1,1,1,1,1,1,0,1,1,1,1,1,1,1,1,0],
    [0,1,1,1,1,1,1,1,1,1,0,0,0,0,0,0,1,1,1,0],
    [0,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,0],
    [0,0,0,0,0,0,0,1,1,1,1,1,1,1,1,1,1,0,0,0],
    [0,1,1,1,1,1,1,1,1,1,1,1,0,1,1,1,1,1,1,0],
    [0,1,1,1,1,1,1,1,1,1,1,1,0,1,1,1,1,1,1,0],
    [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
]

maze = Maze(maze_map, WIDTH, HEIGHT)

occupied_cells = set()

player = Hero((WIDTH // 2, HEIGHT - 50), maze)
dog = Dog((WIDTH // 2, HEIGHT // 2), maze)

enemies = [Enemy(maze, occupied_cells) for _ in range(3)]
fishes = []
fake_fishes = []

fish_spawn_timer = 0
fish_spawn_interval = 5
game_over = False
in_main_menu = True
music_on = True

def update(dt):
    global fish_spawn_timer, game_over

    if in_main_menu or game_over:
        return

    player.update()
    dog.update(player) 

    for enemy in enemies[:]:
        if player.actor.colliderect(enemy.actor) and not enemy.exploding:
            enemy.explode()
            if not enemy.damaged_player:
                player.take_damage()
                enemy.damaged_player = True
        if not enemy.update():
            enemies.remove(enemy)
            enemies.append(Enemy(maze, occupied_cells))

    for fish in fishes:
        fish.update(player)

    for fake_fish in fake_fishes:
        fake_fish.update(player)

    fish_spawn_timer += dt
    if fish_spawn_timer >= fish_spawn_interval:
        spawn_fishes()
        fish_spawn_timer = 0

    if player.lives <= 0:
        game_over = True

def spawn_fishes():
    available_fish = next((f for f in fishes if f.collected), None)
    available_fake = next((f for f in fake_fishes if f.collected), None)

    if available_fish:
        available_fish.reset(maze, occupied_cells)
    elif len(fishes) < 3:
        fishes.append(Fish(maze, occupied_cells))

    if available_fake:
        available_fake.reset(maze, occupied_cells)
    elif len(fake_fishes) < 2:
        fake_fishes.append(FakeFish(maze, occupied_cells))

def draw():
    screen.clear()

    if in_main_menu:
        draw_main_menu()
    elif game_over:
        draw_game_over()
    else:
        maze.draw(screen)
        player.draw()
        dog.draw()
        for enemy in enemies:
            enemy.draw()
        for fish in fishes:
            fish.draw()
        for fake_fish in fake_fishes:
            fake_fish.draw()
        draw_ui()

def draw_main_menu():
    screen.draw.text("CAT GAME", center=(WIDTH // 2, 100), fontsize=60, color="white")

    start_btn = Rect((WIDTH // 2 - 100, 200), (200, 50))
    toggle_sound_btn = Rect((WIDTH // 2 - 100, 280), (200, 50))
    quit_btn = Rect((WIDTH // 2 - 100, 360), (200, 50))

    screen.draw.filled_rect(start_btn, "darkblue")
    screen.draw.text("Start Game", center=start_btn.center, fontsize=30, color="white")

    screen.draw.filled_rect(toggle_sound_btn, "darkgreen")
    sound_label = "Turn off music" if music_on else "Turn on music"
    screen.draw.text(sound_label, center=toggle_sound_btn.center, fontsize=30, color="white")

    screen.draw.filled_rect(quit_btn, "darkred")
    screen.draw.text("Exit", center=quit_btn.center, fontsize=30, color="white")

def draw_game_over():
    screen.fill("lightblue")
    screen.draw.text("GAME OVER", center=(WIDTH // 2, HEIGHT // 2 - 60), fontsize=60, color="black", owidth=2, ocolor="white")
    screen.draw.text(f"Your Score: {player.score}", center=(WIDTH // 2, HEIGHT // 2 - 20), fontsize=40, color="white", owidth=1, ocolor="black")

    retry_button = Rect((WIDTH // 2 - 60, HEIGHT // 2 + 20), (120, 40))
    screen.draw.filled_rect(retry_button, "black")
    screen.draw.text("RETRY", center=retry_button.center, fontsize=30, color="white")

def draw_ui():
    for i in range(3):
        heart_image = "heart_full" if i < player.lives else "heart_empty"
        screen.blit(heart_image, (10 + i * 40, 10))

    screen.draw.text(
        f"Score: {player.score}",
        topright=(WIDTH - 10, 10),
        fontsize=40,
        color="white",
        owidth=1,
        ocolor="black"
    )

def on_mouse_down(pos):
    global in_main_menu, music_on, game_over

    if in_main_menu:
        if Rect((WIDTH // 2 - 100, 200), (200, 50)).collidepoint(pos):
            start_game()
        elif Rect((WIDTH // 2 - 100, 280), (200, 50)).collidepoint(pos):
            toggle_music()
        elif Rect((WIDTH // 2 - 100, 360), (200, 50)).collidepoint(pos):
            exit()

    elif game_over:
        retry_button = Rect((WIDTH // 2 - 60, HEIGHT // 2 + 20), (120, 40))
        if retry_button.collidepoint(pos):
            start_game()

def start_game():
    global player, dog, enemies, fishes, fake_fishes, fish_spawn_timer, game_over, in_main_menu, occupied_cells

    occupied_cells.clear()

    cat_cell = (1, 1)
    dog_cell = (18, 1)

    cat_pos = maze.cell_to_pixel(cat_cell)
    dog_pos = maze.cell_to_pixel(dog_cell)

    player = Hero(cat_pos, maze)
    dog = Dog(dog_pos, maze)

    enemies.clear()
    enemies.extend([Enemy(maze, occupied_cells) for _ in range(3)])
    fishes.clear()
    fake_fishes.clear()
    fish_spawn_timer = 0
    game_over = False
    in_main_menu = False

    if music_on and not music.is_playing("background"):
        music.play("background")
        music.set_volume(0.5)

def toggle_music():
    global music_on
    music_on = not music_on
    if music_on:
        music.play("background")
        music.set_volume(0.5)
    else:
        music.stop()

pgzrun.go()
