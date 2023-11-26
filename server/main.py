import pygame
import sys
import random
import math
import pygame.time
# start this pygame thing
pygame.init()

# Constants
WIDTH, HEIGHT = 800, 600
PUCK_RADIUS = 15
PADDLE_RADIUS = 30
#PADDLE_WIDTH, PADDLE_HEIGHT = 15, 100
GOAL_WIDTH, GOAL_HEIGHT = 10, 200
cooldown = 100
FPS = 60

# Colors
WHITE = (255, 255, 255)
BLUE = (77, 140, 255)
GREEN = (0, 255, 100)
RED = (255, 0, 80)
DARK_GREY = (10, 10, 10)
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
      if self.rect.x < WIDTH // 3:
        self.rect.x = max(0, min(WIDTH // 3 - (PADDLE_RADIUS * 2),
                                 self.rect.x))
    else:
      self.rect.x = max(2 * (WIDTH // 3),
                        min(WIDTH - (PADDLE_RADIUS * 2), self.rect.x))

  def draw(self, colour):
    #pygame.draw.rect(screen, WHITE, self.rect)
    pygame.draw.circle(screen, colour, self.rect.center, PADDLE_RADIUS)

#    pygame.draw.circle(screen, WHITE, self.rect.center, PADDLE_RADIUS)

class Puck:

  def __init__(self, x, y):
    self.rect = pygame.Rect(x, y, PUCK_RADIUS * 2, PUCK_RADIUS * 2)
    self.speed = [random.choice([-5, 5]), random.choice([-5, 5])]
    #for ensuring multiple calls do not occur in a row
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
    pygame.draw.circle(screen, colour, self.rect.center, PUCK_RADIUS)


class Goal:

  def __init__(self, x, y):
    self.rect = pygame.Rect(x, y, GOAL_WIDTH, GOAL_HEIGHT)

  def draw(self):
    pygame.draw.rect(screen, PASTEL_RED, self.rect)


# def collision(puck, paddle_left, paddle_right):
#     in_x_range_pl = paddle_left.rect.right > puck.rect.left > paddle_left.rect.left
#     in_y_range_pl = paddle_left.rect.bottom > puck.rect.top > paddle_left.rect.top
#     in_x_range_pr = paddle_right.rect.left < puck.rect.right < paddle_right.rect.right
#     in_y_range_pr = paddle_right.rect.bottom > puck.rect.top > paddle_right.rect.top

#     # If a collision occurs, reverse the direction of the puck
#     if (in_x_range_pl and in_y_range_pl) or (in_x_range_pr and in_y_range_pr):
#         puck.speed[1] = -puck.speed[1]
#         puck.speed[0] = -puck.speed[0]



def collision(puck, paddle_left, paddle_right):
    # Get the current time to ensure we can't call this function multiple times in a row
    current_time = pygame.time.get_ticks() 

    # If we called it too recently, then exit. Note it is 100 milliseconds
    if(current_time - puck.last_collision < cooldown):
        print('too small')
        return
    print('made it past')
    # Calculate the distance between the centers of the paddles with the puck
    distance_left = math.sqrt((paddle_left.rect.centerx - puck.rect.centerx)**2 + (paddle_left.rect.centery - puck.rect.centery)**2)
    distance_right = math.sqrt((paddle_right.rect.centerx - puck.rect.centerx)**2 + (paddle_right.rect.centery - puck.rect.centery)**2)

    # Sum of radii
    sum_of_radii = PADDLE_RADIUS + PUCK_RADIUS

    # Check collision with left paddle
    if distance_left < sum_of_radii:
        # normal vector = (x, y) of 
        normal = [paddle_left.rect.centerx - puck.rect.centerx, paddle_left.rect.centery - puck.rect.centery]
        # Normalize the normal vector
        length = math.sqrt(normal[0]**2 + normal[1]**2)
        if length != 0:
            normal[0] /= length
            normal[1] /= length
        # Reflect the speed vector
        dot_product = puck.speed[0] * normal[0] + puck.speed[1] * normal[1]
        puck.speed = [puck.speed[0] - 2 * dot_product * normal[0],
                      puck.speed[1] - 2 * dot_product * normal[1]]
        # Set the collision time:
        puck.last_collision = current_time

    # Check collision with right paddle
    elif distance_right < sum_of_radii:
        # Calculate the normal vector
        normal = [paddle_right.rect.centerx - puck.rect.centerx, paddle_right.rect.centery - puck.rect.centery]
        # Normalize the normal vector
        length = math.sqrt(normal[0]**2 + normal[1]**2)
        if length != 0:
            normal[0] /= length
            normal[1] /= length
        # Reflect the speed vector
        dot_product = puck.speed[0] * normal[0] + puck.speed[1] * normal[1]
        puck.speed = [puck.speed[0] - 2 * dot_product * normal[0],
                      puck.speed[1] - 2 * dot_product * normal[1]]
        # Set the collision time:
        puck.last_collision = current_time
        
    









def game_loop():
  paddle_left = Paddle(50, HEIGHT // 2 - PADDLE_RADIUS * 2 // 2)
  paddle_right = Paddle(WIDTH - 50 - PADDLE_RADIUS * 2,
                        HEIGHT // 2 - PADDLE_RADIUS * 2 // 2)
  puck = Puck(WIDTH // 2 - PUCK_RADIUS, HEIGHT // 2 - PUCK_RADIUS)

  # Initialize the goals
  goal_left = Goal(0, HEIGHT // 2 - GOAL_HEIGHT // 2)
  goal_right = Goal(WIDTH - 10, HEIGHT // 2 - GOAL_HEIGHT // 2)

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
      paddle_left.move(-5, 0, True)
    if keys[pygame.K_s]:
      paddle_left.move(5, 0, True)

    if keys[pygame.K_a]:
      paddle_left.move(0, -5, True)
    if keys[pygame.K_d]:
      paddle_left.move(0, 5, True)

      # Move the right paddle (for a two-player game)
    if keys[pygame.K_UP]:
      paddle_right.move(-5, 0, False)
    if keys[pygame.K_DOWN]:
      paddle_right.move(5, 0, False)

    if keys[pygame.K_LEFT]:
      paddle_right.move(0, -5, False)
    if keys[pygame.K_RIGHT]:
      paddle_right.move(0, 5, False)

    # Move the puck
    puck.move()

    # Check collision and handle
    collision(puck, paddle_left, paddle_right)

    # Score logic
    # Make it so only goes in on goal for certain height and left of screen
    if puck.rect.left < 0 and (puck.rect.top < HEIGHT // 2 + 100
                               and puck.rect.top > HEIGHT // 2 - 100):
      score_right += 1
      #Reset location to the middle
      puck.rect.x = WIDTH // 2 - PUCK_RADIUS
    elif puck.rect.right > WIDTH and (puck.rect.top < HEIGHT // 2 + 100
                                      and puck.rect.top > HEIGHT // 2 - 100):
      score_left += 1
      #Reset location to the middle
      puck.rect.x = WIDTH // 2 - PUCK_RADIUS

    # Draw everything
    screen.fill(BLACK)
    paddle_left.draw(BLUE)
    paddle_right.draw(RED)
    puck.draw(GREEN)
    goal_left.draw()
    goal_right.draw()

    # Draw the score:
    score_display = font.render(f"{score_left} - {score_right}", True, WHITE)
    screen.blit(score_display, (WIDTH // 2 - 50, 20))

    pygame.display.flip()
    clock.tick(FPS)


if __name__ == "__main__":
  game_loop()
