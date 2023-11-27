import pygame
import sys
import random
import math
import pygame.time
pygame.init()

# Constants
WIDTH, HEIGHT = 800, 600
PUCK_RADIUS = 18
PADDLE_RADIUS = 30
GOAL_WIDTH, GOAL_HEIGHT = 10, 120
cooldown = 250
FPS = 60
PUCK_SPEED = 6
PADDLE_SPEED = 6
# Colors
WHITE = (255, 255, 255)
BLUE = (77, 140, 255)
GREEN = (0, 255, 100)
RED = (255, 0, 80)
DARK_GREY = (10, 10, 10)
LIGHT_GREY = (150, 150, 150)
LIGHT_PURPLE = (220, 150, 230)
YELLOW = (240, 230, 0)
MIDNIGHT_BLUE = (10, 0, 100)
BURGUNDY = (150, 0, 20)
BLACK = (0, 0, 0)
PASTEL_RED = (255, 150, 150)
# Initialize the game window
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Air Hockey")
clock = pygame.time.Clock()


class Paddle:

  def __init__(self, x, y):
    self.rect = pygame.Rect(x, y, PADDLE_RADIUS * 2, PADDLE_RADIUS * 2)

  def move(self, y, x, isLeftPaddle):
    self.rect.y += y
    # Ensure the paddle stays within the screen boundaries
    self.rect.y = max(0, min(HEIGHT - (PADDLE_RADIUS * 2), self.rect.y))
    self.rect.x += x

    if isLeftPaddle:
      if self.rect.x < WIDTH // 2:
        self.rect.x = max(0, min(WIDTH // 2 - (PADDLE_RADIUS * 2),
                                 self.rect.x))
    else:
      self.rect.x = max((WIDTH // 2),
                        min(WIDTH - (PADDLE_RADIUS * 2), self.rect.x))

  def draw(self, colour):
    pygame.draw.circle(screen, WHITE, self.rect.center, PADDLE_RADIUS)
    pygame.draw.circle(screen, colour, self.rect.center, PADDLE_RADIUS - 3)


class Puck:

  def __init__(self, x, y):
    self.rect = pygame.Rect(x, y, PUCK_RADIUS * 2, PUCK_RADIUS * 2)
    self.speed = [random.choice([-PUCK_SPEED, PUCK_SPEED]), random.choice([-PUCK_SPEED, PUCK_SPEED])]
    self.last_collision = 0

  def move(self):
    self.rect.x += self.speed[0]
    self.rect.y += self.speed[1]

    # Bounce off the walls
    if self.rect.left < 0 or self.rect.right > WIDTH:
      self.speed[0] = -self.speed[0]
    if self.rect.top < 0 or self.rect.bottom > HEIGHT:
      self.speed[1] = -self.speed[1]

  def draw(self, colour):
    pygame.draw.circle(screen, WHITE, self.rect.center, PUCK_RADIUS)
    pygame.draw.circle(screen, colour, self.rect.center, PUCK_RADIUS - 3)


class Goal:

  def __init__(self, x, y):
    self.rect = pygame.Rect(x, y, GOAL_WIDTH, GOAL_HEIGHT)


def set_lines(dot_colour, line_colour, background_colour1, background_colour2):
  screen.fill(BLACK)
  for x in range(0, WIDTH, 30):
    for y in range(0, HEIGHT, 30):
      pygame.draw.rect(screen, dot_colour, (x, y, 1, 1))

  pygame.draw.circle(screen, background_colour1, (-1, HEIGHT / 2), 120, 4)
  pygame.draw.circle(screen, background_colour2, (1, HEIGHT / 2), 120, 4)
  pygame.draw.circle(screen, line_colour, (0, HEIGHT / 2), 120, 4)
  pygame.draw.circle(screen, background_colour1, (WIDTH - 1, HEIGHT / 2), 120, 4)
  pygame.draw.circle(screen, background_colour2, (WIDTH + 1, HEIGHT / 2), 120, 4)
  pygame.draw.circle(screen, line_colour, (WIDTH, HEIGHT / 2), 120, 4)
  pygame.draw.circle(screen, background_colour1, (WIDTH / 2 - 1, HEIGHT / 2), 120, 4)
  pygame.draw.circle(screen, background_colour2, (WIDTH / 2 + 1, HEIGHT / 2), 120, 4)
  pygame.draw.circle(screen, line_colour, (WIDTH / 2, HEIGHT / 2), 120, 4)
  pygame.draw.rect(screen, background_colour1, (-6, HEIGHT / 2 - 65, 20, 130), 4)
  pygame.draw.rect(screen, background_colour2, (-4, HEIGHT / 2 - 65, 20, 130), 4)
  pygame.draw.rect(screen, line_colour, (-5, HEIGHT / 2 - 65, 20, 130), 4)
  pygame.draw.rect(screen, background_colour1, (WIDTH - 16, HEIGHT / 2 - 65, 20, 130), 4)
  pygame.draw.rect(screen, background_colour2, (WIDTH - 14, HEIGHT / 2 - 65, 20, 130), 4)
  pygame.draw.rect(screen, line_colour, (WIDTH - 15, HEIGHT / 2 - 65, 20, 130), 4)
  line_width = 3  # You can adjust the width of the line
  line_start = (WIDTH // 4 - 1, 0)  # Starting point of the line
  line_end = (WIDTH // 4 - 1, HEIGHT)  # Ending point of the line
  pygame.draw.line(screen, background_colour1, line_start, line_end, line_width)
  line_start = (WIDTH // 4 + 1, 0)  # Starting point of the line
  line_end = (WIDTH // 4 + 1, HEIGHT)  # Ending point of the line
  pygame.draw.line(screen, background_colour2, line_start, line_end, line_width)
  line_start = (WIDTH // 4, 0)  # Starting point of the line
  line_end = (WIDTH // 4, HEIGHT)  # Ending point of the line
  pygame.draw.line(screen, line_colour, line_start, line_end, line_width)
  line_start = (3*WIDTH // 4 - 1, 0)  # Starting point of the line
  line_end = (3*WIDTH // 4 - 1, HEIGHT)  # Ending point of the line
  pygame.draw.line(screen, background_colour1, line_start, line_end, line_width)
  line_start = (3*WIDTH // 4 + 1, 0)  # Starting point of the line
  line_end = (3*WIDTH // 4 + 1, HEIGHT)  # Ending point of the line
  pygame.draw.line(screen, background_colour2, line_start, line_end, line_width)
  line_start = (3 * WIDTH // 4, 0)  # Starting point of the line
  line_end = (3 * WIDTH // 4, HEIGHT)  # Ending point of the line
  pygame.draw.line(screen, line_colour, line_start, line_end, line_width)


def collision(puck, paddle_left, paddle_right):
  # Get the current time to ensure we can't call this function multiple times in a row
  current_time = pygame.time.get_ticks()

  # If we called it too recently, then exit. Note it is 100 milliseconds
  if (current_time - puck.last_collision < cooldown):
#     print('too small')
    return
#   print('made it past')
  # Calculate the distance between the centers of the paddles with the puck
  distance_left = math.sqrt((paddle_left.rect.centerx - puck.rect.centerx)**2 +
                            (paddle_left.rect.centery - puck.rect.centery)**2)
  distance_right = math.sqrt(
      (paddle_right.rect.centerx - puck.rect.centerx)**2 +
      (paddle_right.rect.centery - puck.rect.centery)**2)

  # Sum of radii
  sum_of_radii = PADDLE_RADIUS + PUCK_RADIUS

  # Check collision with left paddle
  if distance_left < sum_of_radii:
    # normal vector = (x, y) of
    normal = [
        paddle_left.rect.centerx - puck.rect.centerx,
        paddle_left.rect.centery - puck.rect.centery
    ]
    # Normalize the normal vector
    length = math.sqrt(normal[0]**2 + normal[1]**2)
    if length != 0:
      normal[0] /= length
      normal[1] /= length
    # Reflect the speed vector
    dot_product = puck.speed[0] * normal[0] + puck.speed[1] * normal[1]
    puck.speed = [
        puck.speed[0] - 2 * dot_product * normal[0],
        puck.speed[1] - 2 * dot_product * normal[1]
    ]
    # Set the collision time:
    puck.last_collision = current_time

    # Check collision with right paddle
  elif distance_right < sum_of_radii:
    # Calculate the normal vector
    normal = [
        paddle_right.rect.centerx - puck.rect.centerx,
        paddle_right.rect.centery - puck.rect.centery
    ]
    # Normalize the normal vector
    length = math.sqrt(normal[0]**2 + normal[1]**2)
    if length != 0:
      normal[0] /= length
      normal[1] /= length
    # Reflect the speed vector
    dot_product = puck.speed[0] * normal[0] + puck.speed[1] * normal[1]
    puck.speed = [
        puck.speed[0] - 2 * dot_product * normal[0],
        puck.speed[1] - 2 * dot_product * normal[1]
    ]
    # Set the collision time:
    puck.last_collision = current_time


def game_loop():

  PLAYER1_COLOUR = BLUE
  PLAYER2_COLOUR = RED
  PUCK_COLOUR = LIGHT_PURPLE
  LINE_COLOUR = WHITE

  paddle_left = Paddle(50, HEIGHT // 2 - PADDLE_RADIUS * 2 // 2)
  paddle_right = Paddle(WIDTH - 50 - PADDLE_RADIUS * 2, HEIGHT // 2 - PADDLE_RADIUS * 2 // 2)
  puck = Puck(WIDTH // 2 - PUCK_RADIUS, HEIGHT // 2 - PUCK_RADIUS)
  # Initialize the goals
  goal_left = Goal(0, HEIGHT // 2 - GOAL_HEIGHT // 2)
  goal_right = Goal(WIDTH - 10, HEIGHT // 2 - GOAL_HEIGHT // 2)
  # Scores
  score_left = 0
  score_right = 0
  font = pygame.font.Font(None, 66)


  while True:
    for event in pygame.event.get():
      if event.type == pygame.QUIT:
        pygame.quit()
        sys.exit()

    keys = pygame.key.get_pressed()
    # Move the left paddle
    if keys[pygame.K_w]:
      paddle_left.move(-PADDLE_SPEED, 0, True)
    if keys[pygame.K_s]:
      paddle_left.move(PADDLE_SPEED, 0, True)
    if keys[pygame.K_a]:
      paddle_left.move(0, -PADDLE_SPEED, True)
    if keys[pygame.K_d]:
      paddle_left.move(0, PADDLE_SPEED, True)
      # Move the right paddle (for a two-player game)
    if keys[pygame.K_UP]:
      paddle_right.move(-PADDLE_SPEED, 0, False)
    if keys[pygame.K_DOWN]:
      paddle_right.move(PADDLE_SPEED, 0, False)
    if keys[pygame.K_LEFT]:
      paddle_right.move(0, -PADDLE_SPEED, False)
    if keys[pygame.K_RIGHT]:
      paddle_right.move(0, PADDLE_SPEED, False)

    # Move the puck
    puck.move()

    # Check collision and handle
    collision(puck, paddle_left, paddle_right)

    # Score logic
    # Make it so only goes in on goal for certain height and left of screen
    if puck.rect.left < 0 and (puck.rect.top < HEIGHT // 2 + 100 and puck.rect.top > HEIGHT // 2 - 100):
      score_right += 1
      #Reset location to the middle
      puck.rect.x = WIDTH // 2 - PUCK_RADIUS
    elif puck.rect.right > WIDTH and (puck.rect.top < HEIGHT // 2 + 100 and puck.rect.top > HEIGHT // 2 - 100):
      score_left += 1
      #Reset location to the middle
      puck.rect.x = WIDTH // 2 - PUCK_RADIUS

    # Colour everything
    set_lines(WHITE, LINE_COLOUR, PLAYER1_COLOUR, PLAYER2_COLOUR)
    paddle_left.draw(PLAYER1_COLOUR)
    paddle_right.draw(PLAYER2_COLOUR)
    puck.draw(PUCK_COLOUR)

    # Draw the score:
    score_display = font.render(f"{score_left} - {score_right}", True, RED)
    screen.blit(score_display, (WIDTH // 2 - 48, 22))
    score_display = font.render(f"{score_left} - {score_right}", True, BLUE)
    screen.blit(score_display, (WIDTH // 2 - 52, 18))
    score_display = font.render(f"{score_left} - {score_right}", True, WHITE)
    screen.blit(score_display, (WIDTH // 2 - 50, 20))

    pygame.display.flip()
    clock.tick(FPS)


if __name__ == "__main__":
  game_loop()
