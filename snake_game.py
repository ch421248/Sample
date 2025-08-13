# Classic Snake Game using Pygame

import pygame
import sys
import random

# You may need to install pygame: pip install pygame

pygame.init()
WIDTH, HEIGHT = 400, 400
CELL = 20
screen = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()
font = pygame.font.SysFont(None, 32)

def draw_snake(snake):
    for pos in snake:
        pygame.draw.rect(screen, (0,255,0), (*pos, CELL, CELL))

def draw_food(food):
    pygame.draw.rect(screen, (255,0,0), (*food, CELL, CELL))

def show_score(score):
    img = font.render(f"Score: {score}", True, (255,255,255))
    screen.blit(img, (10, 10))

def main():
    snake = [(100,100), (80,100), (60,100)]
    direction = (CELL, 0)
    food = (random.randrange(0, WIDTH, CELL), random.randrange(0, HEIGHT, CELL))
    score = 0

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit(); sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP and direction != (0,CELL):
                    direction = (0, -CELL)
                elif event.key == pygame.K_DOWN and direction != (0,-CELL):
                    direction = (0, CELL)
                elif event.key == pygame.K_LEFT and direction != (CELL,0):
                    direction = (-CELL, 0)
                elif event.key == pygame.K_RIGHT and direction != (-CELL,0):
                    direction = (CELL, 0)

        head = ((snake[0][0] + direction[0]) % WIDTH,
                (snake[0][1] + direction[1]) % HEIGHT)
        if head in snake:
            break # Game Over
        snake = [head] + snake[:-1]
        if head == food:
            snake.append(snake[-1])
            score += 1
            while True:
                food = (random.randrange(0, WIDTH, CELL), random.randrange(0, HEIGHT, CELL))
                if food not in snake:
                    break

        screen.fill((0,0,0))
        draw_snake(snake)
        draw_food(food)
        show_score(score)
        pygame.display.flip()
        clock.tick(10)

    # Game Over screen
    screen.fill((0,0,0))
    img = font.render(f"Game Over! Score: {score}", True, (255,0,0))
    screen.blit(img, (WIDTH//2-100, HEIGHT//2-20))
    pygame.display.flip()
    pygame.time.wait(2000)

if __name__ == "__main__":
    main()