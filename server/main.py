import pygame
import sys
import random

pygame.init()

# Constants
WIDTH, HEIGHT = 800, 600
PUCK_RADIUS = 15
PADDLE_WIDTH, PADDLE_HEIGHT = 15, 100

FPS = 60

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

# Initialize the game window
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Air Hockey")
clock = pygame.time.Clock()


class Paddle:
    def __init__(self, x, y):
        self.rect = pygame.Rect(x, y, PADDLE_WIDTH, PADDLE_HEIGHT)

    def move(self, y):
        self.rect.y += y
        # Ensure the paddle stays within the screen boundaries
        self.rect.y = max(0, min(HEIGHT - PADDLE_HEIGHT, self.rect.y))

    def draw(self):
        pygame.draw.rect(screen, WHITE, self.rect)


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

class Goal:
    def __init__(self, x, y):
        self.rect = pygame.Rect(x, y, PUCK_RADIUS * 2, PUCK_RADIUS * 2)
        self.speed = [random.choice([-5, 5]), random.choice([-5, 5])]
    
    def draw(self):
        pygame.draw.circle(screen, WHITE, self.rect.center, PUCK_RADIUS)


def game_loop():
    paddle_left = Paddle(50, HEIGHT // 2 - PADDLE_HEIGHT // 2)
    paddle_right = Paddle(WIDTH - 50 - PADDLE_WIDTH, HEIGHT // 2 - PADDLE_HEIGHT // 2)
    puck = Puck(WIDTH // 2 - PUCK_RADIUS, HEIGHT // 2 - PUCK_RADIUS)

    # Scores
    score_left = 0
    score_right = 0
    font = pygame.font.Font(None, 36)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        keys = pygame.key.get_pressed()
        # Move the left paddle
        if keys[pygame.K_w]:
            paddle_left.move(-5)
        if keys[pygame.K_s]:
            paddle_left.move(5)

        # Move the right paddle (for a two-player game)
        if keys[pygame.K_UP]:
            paddle_right.move(-5)
        if keys[pygame.K_DOWN]:
            paddle_right.move(5)

        # Move the puck
        puck.move()

        # Score logic
        # Make it so only goes in on goal for certain height and left of screen
        if puck.rect.left < 0 and (puck.rect.top< HEIGHT//2 +100 and puck.rect.top> HEIGHT//2 -100):
            score_right += 1
            #Reset location to the middle
            puck.rect.x = WIDTH // 2 - PUCK_RADIUS
        elif puck.rect.right > WIDTH and (puck.rect.top< HEIGHT//2 +100 and puck.rect.top> HEIGHT//2 -100):
            score_left += 1
            #Reset location to the middle
            puck.rect.x = WIDTH // 2 - PUCK_RADIUS

        # Draw everything
        screen.fill(BLACK)
        paddle_left.draw()
        paddle_right.draw()
        puck.draw()

        # Draw the score:
        score_display = font.render(f"{score_left} - {score_right}", True, WHITE)
        screen.blit(score_display, (WIDTH // 2 - 50, 20))

        pygame.display.flip()
        clock.tick(FPS)

if __name__ == "__main__":
    game_loop()
