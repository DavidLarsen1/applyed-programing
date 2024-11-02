import pygame
import sys

# Initialize Pygame
pygame.init()

# Screen dimensions
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

# Paddles and Ball properties
PADDLE_WIDTH = 15
PADDLE_HEIGHT = 100
BALL_SIZE = 20
BALL_SPEED = 5

# Set up the display
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Pong Game")

# Paddle and ball positions
paddle_a_pos = [50, SCREEN_HEIGHT // 2 - PADDLE_HEIGHT // 2]
paddle_b_pos = [SCREEN_WIDTH - 50 - PADDLE_WIDTH, SCREEN_HEIGHT // 2 - PADDLE_HEIGHT // 2]
ball_pos = [SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2]
ball_velocity = [BALL_SPEED, BALL_SPEED]

# Clock for controlling FPS
clock = pygame.time.Clock()

def move_paddle(paddle, up_key, down_key):
    keys = pygame.key.get_pressed()
    if keys[up_key] and paddle[1] > 0:
        paddle[1] -= BALL_SPEED
    if keys[down_key] and paddle[1] < SCREEN_HEIGHT - PADDLE_HEIGHT:
        paddle[1] += BALL_SPEED

def move_ball():
    global ball_velocity
    ball_pos[0] += ball_velocity[0]
    ball_pos[1] += ball_velocity[1]

    # Bounce on top and bottom walls
    if ball_pos[1] <= 0 or ball_pos[1] >= SCREEN_HEIGHT - BALL_SIZE:
        ball_velocity[1] = -ball_velocity[1]

    # Bounce off paddles
    if (paddle_a_pos[0] < ball_pos[0] < paddle_a_pos[0] + PADDLE_WIDTH and
        paddle_a_pos[1] < ball_pos[1] < paddle_a_pos[1] + PADDLE_HEIGHT) or \
       (paddle_b_pos[0] < ball_pos[0] < paddle_b_pos[0] + PADDLE_WIDTH and
        paddle_b_pos[1] < ball_pos[1] < paddle_b_pos[1] + PADDLE_HEIGHT):
        ball_velocity[0] = -ball_velocity[0]

    # Reset if ball goes past paddles
    if ball_pos[0] <= 0 or ball_pos[0] >= SCREEN_WIDTH - BALL_SIZE:
        ball_pos[0], ball_pos[1] = SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2
        ball_velocity[0] = -ball_velocity[0]

def draw_objects():
    screen.fill(BLACK)
    pygame.draw.rect(screen, WHITE, (*paddle_a_pos, PADDLE_WIDTH, PADDLE_HEIGHT))
    pygame.draw.rect(screen, WHITE, (*paddle_b_pos, PADDLE_WIDTH, PADDLE_HEIGHT))
    pygame.draw.ellipse(screen, WHITE, (*ball_pos, BALL_SIZE, BALL_SIZE))
    pygame.draw.aaline(screen, WHITE, (SCREEN_WIDTH // 2, 0), (SCREEN_WIDTH // 2, SCREEN_HEIGHT))

def main():
    while True:
        # Event handling
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        # Player controls
        move_paddle(paddle_a_pos, pygame.K_w, pygame.K_s)
        move_paddle(paddle_b_pos, pygame.K_UP, pygame.K_DOWN)

        # Ball movement
        move_ball()

        # Draw everything
        draw_objects()

        # Update the display
        pygame.display.flip()
        clock.tick(60)

if __name__ == "__main__":
    main()
