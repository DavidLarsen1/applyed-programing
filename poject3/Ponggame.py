import pygame
import sys
import json
import os

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
SAVE_FILE = "game_save.json"  # External file to save/load game state

# Set up the display
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Pong Game with Save/Load and Score System")

# Paddle and ball positions
paddle_a_pos = [50, SCREEN_HEIGHT // 2 - PADDLE_HEIGHT // 2]
paddle_b_pos = [SCREEN_WIDTH - 50 - PADDLE_WIDTH, SCREEN_HEIGHT // 2 - PADDLE_HEIGHT // 2]
ball_pos = [SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2]
ball_velocity = [BALL_SPEED, BALL_SPEED]

# Score variables
score_a = 0
score_b = 0

# Font for displaying score
font = pygame.font.Font(None, 36)

# Clock for controlling FPS
clock = pygame.time.Clock()

def move_paddle(paddle, up_key, down_key):
    keys = pygame.key.get_pressed()
    if keys[up_key] and paddle[1] > 0:
        paddle[1] -= BALL_SPEED
    if keys[down_key] and paddle[1] < SCREEN_HEIGHT - PADDLE_HEIGHT:
        paddle[1] += BALL_SPEED

def move_ball():
    global ball_velocity, score_a, score_b
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

    # Check for scoring
    if ball_pos[0] <= 0:
        score_b += 1
        reset_ball()
    elif ball_pos[0] >= SCREEN_WIDTH - BALL_SIZE:
        score_a += 1
        reset_ball()

def reset_ball():
    """Reset ball to the center with a new random direction."""
    global ball_pos, ball_velocity
    ball_pos = [SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2]
    ball_velocity[0] = -ball_velocity[0]

def draw_objects():
    screen.fill(BLACK)
    pygame.draw.rect(screen, WHITE, (*paddle_a_pos, PADDLE_WIDTH, PADDLE_HEIGHT))
    pygame.draw.rect(screen, WHITE, (*paddle_b_pos, PADDLE_WIDTH, PADDLE_HEIGHT))
    pygame.draw.ellipse(screen, WHITE, (*ball_pos, BALL_SIZE, BALL_SIZE))
    pygame.draw.aaline(screen, WHITE, (SCREEN_WIDTH // 2, 0), (SCREEN_WIDTH // 2, SCREEN_HEIGHT))

    # Render the scores
    score_text = font.render(f"{score_a} - {score_b}", True, WHITE)
    screen.blit(score_text, (SCREEN_WIDTH // 2 - score_text.get_width() // 2, 20))

def save_game():
    """Save the current game state to an external file."""
    game_state = {
        "paddle_a_pos": paddle_a_pos,
        "paddle_b_pos": paddle_b_pos,
        "ball_pos": ball_pos,
        "ball_velocity": ball_velocity,
        "score_a": score_a,
        "score_b": score_b
    }
    with open(SAVE_FILE, "w") as file:
        json.dump(game_state, file)
    print("Game saved successfully.")

def load_game():
    """Load the game state from an external file."""
    global paddle_a_pos, paddle_b_pos, ball_pos, ball_velocity, score_a, score_b
    if os.path.exists(SAVE_FILE):
        with open(SAVE_FILE, "r") as file:
            game_state = json.load(file)
            paddle_a_pos = game_state["paddle_a_pos"]
            paddle_b_pos = game_state["paddle_b_pos"]
            ball_pos = game_state["ball_pos"]
            ball_velocity = game_state["ball_velocity"]
            score_a = game_state["score_a"]
            score_b = game_state["score_b"]
        print("Game loaded successfully.")
    else:
        print("Save file not found.")

def main():
    while True:
        # Event handling
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            # Save game on pressing 's'
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_o:
                    save_game()
                # Load game on pressing 'l'
                elif event.key == pygame.K_l:
                    load_game()

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
