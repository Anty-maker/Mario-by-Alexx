import pygame
import random

# Initialize Pygame
pygame.init()

# Screen dimensions
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
CYAN = (0, 255, 255)
RED = (255, 0, 0)

# Player settings
player_size = 50
player_pos = [SCREEN_WIDTH // 2, SCREEN_HEIGHT - 2 * player_size]
player_speed = 10

# Enemy settings
enemy_size = 50
enemy_list = []
enemy_speed = 10
enemy_spawn_rate = 25  # Higher value means fewer enemies

# Load images
player_image = pygame.image.load("player.png")
player_image = pygame.transform.scale(player_image, (player_size, player_size))
enemy_image = pygame.image.load("enemy.png")
enemy_image = pygame.transform.scale(enemy_image, (enemy_size, enemy_size))

# Set up the display
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Mario by Alexx")

# Font settings
font = pygame.font.Font("Milker.otf", 35)
small_font = pygame.font.Font("Milker.otf", 25)

# Game loop
game_over = False
clock = pygame.time.Clock()
score = 0
level = 1
level_up_message = ""
home_screen = True
lose_screen = False

def detect_collision(player_pos, enemy_pos):
    p_x, p_y = player_pos
    e_x, e_y = enemy_pos

    if (e_x >= p_x and e_x < (p_x + player_size)) or (p_x >= e_x and p_x < (e_x + enemy_size)):
        if (e_y >= p_y and e_y < (p_y + player_size)) or (p_y >= e_y and p_y < (e_y + enemy_size)):
            return True
    return False

def drop_enemies(enemy_list):
    delay = random.random()
    if len(enemy_list) < 10 and delay < 1.0 / enemy_spawn_rate:
        x_pos = random.randint(0, SCREEN_WIDTH - enemy_size)
        y_pos = 0
        enemy_list.append([x_pos, y_pos])

def update_enemy_positions(enemy_list, score):
    for idx, enemy_pos in enumerate(enemy_list):
        if enemy_pos[1] >= 0 and enemy_pos[1] < SCREEN_HEIGHT:
            enemy_pos[1] += enemy_speed
        else:
            enemy_list.pop(idx)
            score += 1
    return score

def draw_enemies(enemy_list):
    for enemy_pos in enemy_list:
        screen.blit(enemy_image, (enemy_pos[0], enemy_pos[1]))

def increase_difficulty(level):
    global enemy_speed, enemy_spawn_rate
    enemy_speed = 10 + level * 2
    enemy_spawn_rate = 25 + level * 5

def show_home_screen():
    screen.fill(CYAN)
    title = font.render("Mario by Alexx", 1, BLACK)
    instructions = small_font.render("Press any key to start", 1, BLACK)
    screen.blit(title, (SCREEN_WIDTH // 2 - title.get_width() // 2, SCREEN_HEIGHT // 2 - title.get_height() // 2 - 50))
    screen.blit(instructions, (SCREEN_WIDTH // 2 - instructions.get_width() // 2, SCREEN_HEIGHT // 2 - instructions.get_height() // 2 + 50))
    pygame.display.update()

def show_lose_screen():
    screen.fill(CYAN)
    title = font.render("Game Over", 1, RED)
    instructions = small_font.render("Press any key to return to home", 1, BLACK)
    screen.blit(title, (SCREEN_WIDTH // 2 - title.get_width() // 2, SCREEN_HEIGHT // 2 - title.get_height() // 2 - 50))
    screen.blit(instructions, (SCREEN_WIDTH // 2 - instructions.get_width() // 2, SCREEN_HEIGHT // 2 - instructions.get_height() // 2 + 50))
    pygame.display.update()

while not game_over:
    if home_screen:
        show_home_screen()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game_over = True
            if event.type == pygame.KEYDOWN:
                home_screen = False
                lose_screen = False
                score = 0
                level = 1
                enemy_list = []
                player_pos = [SCREEN_WIDTH // 2, SCREEN_HEIGHT - 2 * player_size]
        continue

    if lose_screen:
        show_lose_screen()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game_over = True
            if event.type == pygame.KEYDOWN:
                home_screen = True
        continue

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            game_over = True

    keys = pygame.key.get_pressed()

    if keys[pygame.K_LEFT] and player_pos[0] > 0:
        player_pos[0] -= player_speed
    if keys[pygame.K_RIGHT] and player_pos[0] < SCREEN_WIDTH - player_size:
        player_pos[0] += player_speed
    if keys[pygame.K_UP] and player_pos[1] > 0:
        player_pos[1] -= player_speed
    if keys[pygame.K_DOWN] and player_pos[1] < SCREEN_HEIGHT - player_size:
        player_pos[1] += player_speed

    # Fill the background with a color
    screen.fill(CYAN)

    drop_enemies(enemy_list)
    score = update_enemy_positions(enemy_list, score)

    if any(detect_collision(player_pos, enemy_pos) for enemy_pos in enemy_list):
        lose_screen = True

    draw_enemies(enemy_list)
    screen.blit(player_image, (player_pos[0], player_pos[1]))

    # Display score and level
    score_label = small_font.render(f"Score: {score}", 1, BLACK)
    level_label = small_font.render(f"Level: {level}", 1, BLACK)
    screen.blit(score_label, (10, 10))
    screen.blit(level_label, (10, 40))

    # Display level up message
    if level_up_message:
        label = font.render(level_up_message, 1, RED)
        screen.blit(label, (SCREEN_WIDTH // 2 - label.get_width() // 2, SCREEN_HEIGHT // 2 - label.get_height() // 2))
        pygame.display.update()
        pygame.time.wait(2000)
        level_up_message = ""

    pygame.display.update()
    clock.tick(30)

    # Increase difficulty and level up
    if score % 20 == 0 and score != 0 and score // 20 == level:
        level += 1
        increase_difficulty(level)
        level_up_message = f"You reached level {level}!"

pygame.quit()
