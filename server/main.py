import pygame
import sys
import random

pygame.init()

# Constants
WIDTH, HEIGHT = 800, 600
PUCK_RADIUS = 15
#PADDLE_WIDTH, PADDLE_HEIGHT = 15, 100
FPS = 60

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

# Initialize the game window
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Air Hockey")
clock = pygame.time.Clock()

class Puck:
    def __init__(self, x, y):
        self.rect = pygame.Rect(x, y, PUCK_RADIUS * 2, PUCK_RADIUS * 2)
        self.speed = [random.choice([-5, 5]), random.choice([-5, 5])]

    def move(self):
        self.rect.x += self.speed[0]
        self.rect.y += self.speed[1]

        # Bounce off the walls
        if self.rect.left < 0 or self.rect.right > WIDTH:
            self.speed[0] = -self.speed[0]
        if self.rect.top < 0 or self.rect.bottom > HEIGHT:
            self.speed[1] = -self.speed[1]

    def draw(self):
        pygame.draw.circle(screen, WHITE, self.rect.center, PUCK_RADIUS)


def game_loop():
    puck = Puck(WIDTH // 2 - PUCK_RADIUS, HEIGHT // 2 - PUCK_RADIUS)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        keys = pygame.key.get_pressed()

        # Move the ball
        puck.move()

        # Draw everything
        screen.fill(BLACK)
        puck.draw()

        pygame.display.flip()
        clock.tick(FPS)

if __name__ == "__main__":
    game_loop()
