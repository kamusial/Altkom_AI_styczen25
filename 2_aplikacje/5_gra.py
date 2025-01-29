import pygame
import random
import sys

# Inicjalizacja Pygame
pygame.init()

# Stałe
SCREEN_WIDTH, SCREEN_HEIGHT = 800, 600
FPS = 15
GRID_SIZE = 20

# Kolory
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)

# Ustawienia ekranu
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption('Królik i Wilk')

# Czcionka
font = pygame.font.SysFont('arial', 25)

# Funkcje pomocnicze
def draw_object(color, position):
    rect = pygame.Rect(position[0], position[1], GRID_SIZE, GRID_SIZE)
    pygame.draw.rect(screen, color, rect)

def display_score(score):
    text = font.render("Marchewki: " + str(score), True, WHITE)
    screen.blit(text, [0, 0])

def game_over(score):
    screen.fill(BLACK)
    text = font.render(f"Przegrałeś! Marchewki: {score}", True, RED)
    screen.blit(text, (SCREEN_WIDTH // 4, SCREEN_HEIGHT // 2))
    pygame.display.flip()
    pygame.time.wait(3000)
    sys.exit()

# Logika gry
def game_loop():
    clock = pygame.time.Clock()

    # Pozycje startowe
    rabbit_pos = [GRID_SIZE * 5, GRID_SIZE * 5]
    rabbit_body = [rabbit_pos[:]] * 5
    direction = 'RIGHT'
    carrot_pos = [random.randint(0, (SCREEN_WIDTH - GRID_SIZE) // GRID_SIZE) * GRID_SIZE,
                  random.randint(0, (SCREEN_HEIGHT - GRID_SIZE) // GRID_SIZE) * GRID_SIZE]
    wolf_pos = [SCREEN_WIDTH - GRID_SIZE, SCREEN_HEIGHT - GRID_SIZE]
    score = 0
    wolf_move_counter = 0  # Licznik ruchów wilka

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT and direction != 'RIGHT':
                    direction = 'LEFT'
                elif event.key == pygame.K_RIGHT and direction != 'LEFT':
                    direction = 'RIGHT'
                elif event.key == pygame.K_UP and direction != 'DOWN':
                    direction = 'UP'
                elif event.key == pygame.K_DOWN and direction != 'UP':
                    direction = 'DOWN'

        # Ruch królika
        if direction == 'LEFT':
            rabbit_pos[0] -= GRID_SIZE
        elif direction == 'RIGHT':
            rabbit_pos[0] += GRID_SIZE
        elif direction == 'UP':
            rabbit_pos[1] -= GRID_SIZE
        elif direction == 'DOWN':
            rabbit_pos[1] += GRID_SIZE

        # Koniec gry przy wyjściu poza planszę
        if rabbit_pos[0] < 0 or rabbit_pos[0] >= SCREEN_WIDTH or rabbit_pos[1] < 0 or rabbit_pos[1] >= SCREEN_HEIGHT:
            game_over(score)

        # Koniec gry przy zderzeniu z wilkiem
        if rabbit_pos == wolf_pos:
            game_over(score)

        # Ruch wilka (co drugi ruch królika)
        if wolf_move_counter % 2 == 0:  # Wilk rusza się dwa razy wolniej
            if wolf_pos[0] < rabbit_pos[0]:
                wolf_pos[0] += GRID_SIZE
            elif wolf_pos[0] > rabbit_pos[0]:
                wolf_pos[0] -= GRID_SIZE
            if wolf_pos[1] < rabbit_pos[1]:
                wolf_pos[1] += GRID_SIZE
            elif wolf_pos[1] > rabbit_pos[1]:
                wolf_pos[1] -= GRID_SIZE
        wolf_move_counter += 1

        # Zbieranie marchewek
        if rabbit_pos == carrot_pos:
            score += 1
            carrot_pos = [random.randint(0, (SCREEN_WIDTH - GRID_SIZE) // GRID_SIZE) * GRID_SIZE,
                          random.randint(0, (SCREEN_HEIGHT - GRID_SIZE) // GRID_SIZE) * GRID_SIZE]
            rabbit_body.insert(0, list(rabbit_pos))
        else:
            rabbit_body.insert(0, list(rabbit_pos))
            rabbit_body.pop()

        # Rysowanie
        screen.fill(BLACK)
        for pos in rabbit_body:
            draw_object(BLUE, pos)
        draw_object(RED, wolf_pos)
        draw_object(GREEN, carrot_pos)
        display_score(score)
        pygame.display.update()

        # Zegar
        clock.tick(FPS)

    pygame.quit()

# Uruchomienie gry
if __name__ == '__main__':
    game_loop()
