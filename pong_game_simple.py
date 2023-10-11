import pygame
import time

# Initialize Pygame
pygame.init()

# Constants
BALL_SPEED = 3
PADDLE_SPEED = 5

# Get the screen's width and height
WIDTH, HEIGHT = pygame.display.Info().current_w, pygame.display.Info().current_h

# Create the game window in full screen
screen = pygame.display.set_mode((WIDTH, HEIGHT), pygame.FULLSCREEN)
pygame.display.set_caption("Pong Game")

# Create the ball and paddle objects
ball_color = (0, 255, 0)  # Initialize ball color as green
ball = pygame.Rect(WIDTH // 2 - 5, HEIGHT // 2 - 5, 10, 10)
paddle1 = pygame.Rect(10, HEIGHT // 2 - 50, 10, 100)
paddle2 = pygame.Rect(WIDTH - 20, HEIGHT // 2 - 50, 10, 100)

ball_speed_x = BALL_SPEED
ball_speed_y = BALL_SPEED

# Player scores
player1_score = 0
player2_score = 0

# Font for displaying scores and ball speed
font = pygame.font.Font(None, 36)

# Create a clock to control the frame rate
clock = pygame.time.Clock()

# Boolean variable to track the ball color state
green_ball = True

# Time tracking variables
last_speed_change_time = time.time()
speed_change_interval = 1  # Change speed every 1 second

# Create a function to display ball speed at the top center of the screen
def display_ball_speed():
    speed_text = font.render("Ball Speed: " + str(abs(ball_speed_x)), True, (255, 255, 255))
    text_rect = speed_text.get_rect()
    text_rect.midtop = (WIDTH // 2, 10)  # Position at the top center
    screen.blit(speed_text, text_rect)

# Start the game loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Check if it's time to change the ball speed
    current_time = time.time()
    if current_time - last_speed_change_time >= speed_change_interval:
        last_speed_change_time = current_time

        # Change the ball speed within the range of 3 to 9
        new_speed = (current_time % 9) + 1
        ball_speed_x = int(new_speed * (1 if ball_speed_x > 0 else -1))  # Preserve direction
        ball_speed_y = int(new_speed * (1 if ball_speed_y > 0 else -1))  # Preserve direction

    # Move the paddles
    keys = pygame.key.get_pressed()

    if keys[pygame.K_w]:
        paddle1.y -= PADDLE_SPEED
    if keys[pygame.K_s]:
        paddle1.y += PADDLE_SPEED

    if keys[pygame.K_UP]:
        paddle2.y -= PADDLE_SPEED
    if keys[pygame.K_DOWN]:
        paddle2.y += PADDLE_SPEED

    # Ensure paddles stay within the screen bounds
    paddle1.y = max(0, min(HEIGHT - paddle1.height, paddle1.y))
    paddle2.y = max(0, min(HEIGHT - paddle2.height, paddle2.y))

    # Collision detection and response for the paddles
    if ball.colliderect(paddle1) or ball.colliderect(paddle2):
        ball_speed_x *= -1
        if ball_speed_x > 0:
            ball_color = (0, 255, 0)  # Change ball color to green
        else:
            ball_color = (255, 0, 0)  # Change ball color to red

    # Move the ball using integer speed values
    ball.x += ball_speed_x
    ball.y += ball_speed_y

    # Check if the ball hits the top or bottom of the screen
    if ball.top <= 0 or ball.bottom >= HEIGHT:
        ball_speed_y *= -1

    # Check if the ball goes out of bounds
    if ball.left <= 0:
        # Player 2 scores a point
        player2_score += 1
        ball = pygame.Rect(WIDTH // 2 - 5, HEIGHT // 2 - 5, 10, 10)
        ball_speed_x = BALL_SPEED
        ball_speed_y = BALL_SPEED
        green_ball = True  # Reset ball color state to green

    if ball.right >= WIDTH:
        # Player 1 scores a point
        player1_score += 1
        ball = pygame.Rect(WIDTH // 2 - 5, HEIGHT // 2 - 5, 10, 10)
        ball_speed_x = -BALL_SPEED
        ball_speed_y = BALL_SPEED
        green_ball = not green_ball  # Toggle ball color state

    # Draw the screen
    screen.fill((0, 0, 0))
    pygame.draw.rect(screen, ball_color, ball)
    pygame.draw.rect(screen, (255, 255, 255), paddle1)
    pygame.draw.rect(screen, (255, 255, 255), paddle2)

    # Display scores
    player1_text = font.render("Player 1: " + str(player1_score), True, (255, 255, 255))
    player2_text = font.render("Player 2: " + str(player2_score), True, (255, 255, 255))
    screen.blit(player1_text, (50, 50))
    screen.blit(player2_text, (WIDTH - 200, 50))

    # Call the function to display ball speed
    display_ball_speed()

    # Update the display
    pygame.display.flip()

    # Control the frame rate
    clock.tick(60)

# Quit Pygame
pygame.quit()
