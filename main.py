import pygame
import random

# Initialize pygame
pygame.init()

# Set up the screen
screen_width = 800
screen_height = 600
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Ping Pong")

# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)

# Game variables
ball_radius = 10
ball_speed_x = 5 * random.choice((1, -1))
ball_speed_y = 5 * random.choice((1, -1))
ball_x = screen_width // 2
ball_y = screen_height // 2

paddle_width = 10
paddle_height = 100
paddle_speed = 20  # Adjust this value for smoother movement
player_paddle_x = 20
ai_paddle_x = screen_width - 20 - paddle_width
player_paddle_y = screen_height // 2 - paddle_height // 2
ai_paddle_y = screen_height // 2 - paddle_height // 2

player_score = 0
ai_score = 0
font = pygame.font.Font(None, 36)

clock = pygame.time.Clock()

def draw_paddles():
    pygame.draw.rect(screen, WHITE, (player_paddle_x, player_paddle_y, paddle_width, paddle_height))
    pygame.draw.rect(screen, WHITE, (ai_paddle_x, ai_paddle_y, paddle_width, paddle_height))

def draw_ball():
    pygame.draw.circle(screen, WHITE, (ball_x, ball_y), ball_radius)

def move_ball():
    global ball_x, ball_y, ball_speed_x, ball_speed_y, player_score, ai_score

    ball_x += ball_speed_x
    ball_y += ball_speed_y

    # Collision with top and bottom walls
    if ball_y <= 0 or ball_y >= screen_height:
        ball_speed_y = -ball_speed_y

    # Collision with paddles
    if ball_x <= player_paddle_x + paddle_width and player_paddle_y <= ball_y <= player_paddle_y + paddle_height:
        ball_speed_x = -ball_speed_x

    if ball_x >= ai_paddle_x - ball_radius and ai_paddle_y <= ball_y <= ai_paddle_y + paddle_height:
        ball_speed_x = -ball_speed_x

    # Ball out of bounds
    if ball_x < 0:
        ai_score += 1
        reset_ball()

    if ball_x > screen_width:
        player_score += 1
        reset_ball()

def reset_ball():
    global ball_x, ball_y, ball_speed_x, ball_speed_y
    ball_x = screen_width // 2
    ball_y = screen_height // 2
    ball_speed_x = 5 * random.choice((1, -1))
    ball_speed_y = 5 * random.choice((1, -1))

def move_ai_paddle():
    global ai_paddle_y

    # Calculate the desired position of the AI paddle (the y-coordinate of the ball)
    desired_position = ball_y - paddle_height // 2

    # Interpolate towards the desired position
    if ai_paddle_y < desired_position:
        ai_paddle_y += min(paddle_speed, desired_position - ai_paddle_y)
    elif ai_paddle_y > desired_position:
        ai_paddle_y -= min(paddle_speed, ai_paddle_y - desired_position)

def display_scores():
    player_text = font.render(f"Player: {player_score}", True, WHITE)
    ai_text = font.render(f"AI: {ai_score}", True, WHITE)
    screen.blit(player_text, (50, 50))
    screen.blit(ai_text, (screen_width - 150, 50))

# Main game loop
running = True
while running:
    screen.fill(BLACK)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Handle continuous movement of the player's paddle
    keys = pygame.key.get_pressed()
    if keys[pygame.K_UP] and player_paddle_y > 0:
        player_paddle_y -= paddle_speed
    if keys[pygame.K_DOWN] and player_paddle_y < screen_height - paddle_height:
        player_paddle_y += paddle_speed

    move_ai_paddle()
    move_ball()

    draw_paddles()
    draw_ball()
    display_scores()

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
