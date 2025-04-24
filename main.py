import pgzrun
from hero import Hero
from enemy import Enemy
from fish import Fish
import random
import time

WIDTH = 800
HEIGHT = 600

player = Hero((WIDTH // 2, HEIGHT - 50))
enemies = [Enemy() for _ in range(3)]
fishes = []
last_fish_time = time.time()
fish_spawn_interval = 5
game_over = False
button_rect = Rect((WIDTH // 2 - 60, HEIGHT // 2 + 50), (120, 40))
score = 0
in_main_menu = True
music_on = True


def update():
    global game_over, fishes, last_fish_time

    if game_over:
        return

    player.update()

    for enemy in enemies[:]:
        if player.actor.colliderect(enemy.actor) and not enemy.exploding:
            enemy.explode()
            if not enemy.damaged_player:
                player.take_damage()
                enemy.damaged_player = True
        if not enemy.update():
            enemies.remove(enemy)
            enemies.append(Enemy())

    for fish in fishes:
        fish.update(player)

    if time.time() - last_fish_time > fish_spawn_interval:
        available_fish = next((f for f in fishes if f.collected), None)
        if available_fish:
            available_fish.reset()
        elif len(fishes) < 3:
            fishes.append(Fish())
        last_fish_time = time.time()

    if player.lives <= 0:
        game_over = True

def draw():
    screen.clear()
    screen.blit("background", (0, 0))

    if in_main_menu:
        draw_main_menu()
    elif game_over:
        draw_game_over()
    else:
        player.draw()
        for enemy in enemies:
            enemy.draw()
        for fish in fishes:
            fish.draw()
        draw_hearts()
        draw_score()

def draw_main_menu():
    screen.draw.text("CAT GAME", center=(WIDTH//2, 100), fontsize=60, color="white")

    start_btn = Rect((WIDTH//2 - 100, 200), (200, 50))
    toggle_sound_btn = Rect((WIDTH//2 - 100, 280), (200, 50))
    quit_btn = Rect((WIDTH//2 - 100, 360), (200, 50))

    screen.draw.filled_rect(start_btn, "darkblue")
    screen.draw.text("Start game", center=start_btn.center, fontsize=30, color="white")

    screen.draw.filled_rect(toggle_sound_btn, "darkgreen")
    sound_label = "Turn off music" if music_on else "Turn on music"
    screen.draw.text(sound_label, center=toggle_sound_btn.center, fontsize=30, color="white")

    screen.draw.filled_rect(quit_btn, "darkred")
    screen.draw.text("Exit", center=quit_btn.center, fontsize=30, color="white")

def draw_hearts():
    for i in range(3):
        heart_image = "heart_full" if i < player.lives else "heart_empty"
        screen.blit(heart_image, (10 + i * 40, 10))

def draw_score():
    screen.draw.text(f"Score: {player.score}", topright=(WIDTH - 10, 10), fontsize=40, color="white", owidth=1, ocolor="black")

def draw_game_over():
    screen.fill("lightblue")
    screen.draw.text("GAME OVER", center=(WIDTH // 2, HEIGHT // 2 - 60), fontsize=60, color="black", owidth=2.0, ocolor="white")
    screen.draw.text(f"Your Score: {player.score}", center=(WIDTH // 2, HEIGHT // 2 - 20), fontsize=40, color="white", owidth=1.0, ocolor="black")

    button_rect = Rect((WIDTH // 2 - 60, HEIGHT // 2 + 20), (120, 40))
    screen.draw.filled_rect(button_rect, "black")
    screen.draw.text("RETRY", center=button_rect.center, fontsize=30, color="white")

def on_mouse_down(pos):
    global in_main_menu, music_on, game_over, player, enemies, fishes, score, last_fish_time

    if in_main_menu:
        if Rect((WIDTH//2 - 100, 200), (200, 50)).collidepoint(pos):
            in_main_menu = False
            if music_on and not music.is_playing("background"):
                music.play("background")
                music.set_volume(0.5)
        elif Rect((WIDTH//2 - 100, 280), (200, 50)).collidepoint(pos):
            music_on = not music_on
            if music_on:
                music.play("background")
                music.set_volume(0.5)
            else:
                music.stop()
        elif Rect((WIDTH//2 - 100, 360), (200, 50)).collidepoint(pos):
            exit()
        return

    if game_over:
        button_rect = Rect((WIDTH // 2 - 60, HEIGHT // 2 + 20), (120, 40))
        if button_rect.collidepoint(pos):
            player = Hero((WIDTH // 2, HEIGHT - 50))
            enemies = [Enemy() for _ in range(5)]
            fishes = []
            last_fish_time = time.time()
            score = 0
            game_over = False


pgzrun.go()
