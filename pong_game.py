import pygame
import random
import time

# Initialize Pygame
pygame.init()

# Constants
PADDLE_SPEED = 16
BALL_SIZE = 20
PADDLE_WIDTH, PADDLE_HEIGHT = 10, 150
WHITE = (255, 255, 255)
YELLOW = (255, 255, 0)
RED = (255, 0 , 0)
SKY_BLUE = (135, 206, 250)  # RGB color for sky blue

# Create the game window with fullscreen
screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
WIDTH, HEIGHT = screen.get_size()
pygame.display.set_caption("Pong")

# Initialize ball position and velocity
ball_x = WIDTH // 2
ball_y = HEIGHT // 2
ball_speed = random.randint(5, 15)
ball_dx = random.choice((1, -1)) * ball_speed
ball_dy = random.choice((1, -1)) * ball_speed

# Initialize paddle positions
left_paddle_y = (HEIGHT - PADDLE_HEIGHT) // 2
right_paddle_y = (HEIGHT - PADDLE_HEIGHT) // 2

# Initialize player names and scores
player1_name = ""
player2_name = ""
player1_score = 0
player2_score = 0

# Function to enter player names
def enter_names():
    global player1_name, player2_name
    font = pygame.font.Font(None, 36)
    input_box1 = pygame.Rect(WIDTH // 4, HEIGHT // 2 - 40, WIDTH // 2, 32)
    input_box2 = pygame.Rect(WIDTH // 4, HEIGHT // 2 + 10, WIDTH // 2, 32)
    color_inactive = pygame.Color('lightskyblue3')
    color_active = pygame.Color('dodgerblue2')
    color1 = color_inactive
    color2 = color_inactive
    active = False
    text1 = ''
    text2 = ''
    
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    player1_name = text1
                    player2_name = text2
                    return
                if active:
                    if event.key == pygame.K_BACKSPACE:
                        if active == 1:
                            text1 = text1[:-1]
                        else:
                            text2 = text2[:-1]
                    else:
                        if active == 1:
                            text1 += event.unicode
                        else:
                            text2 += event.unicode

            if event.type == pygame.MOUSEBUTTONDOWN:
                if input_box1.collidepoint(event.pos):
                    active = 1
                elif input_box2.collidepoint(event.pos):
                    active = 2
                else:
                    active = 0
                color1 = color_active if active == 1 else color_inactive
                color2 = color_active if active == 2 else color_inactive

        screen.fill((255, 255, 0))  # Set the background to white
        
        # Draw "Player 1" and "Player 2" labels
        player1_label = font.render("Player 1:", True, (0, 0, 0))
        player2_label = font.render("Player 2:", True, (0, 0, 0))
        screen.blit(player1_label, (input_box1.x - player1_label.get_width() - 10, input_box1.y))
        screen.blit(player2_label, (input_box2.x - player2_label.get_width() - 10, input_box2.y))
        
        txt_surface1 = font.render(text1, True, (0, 0, 0))
        width1 = max(200, txt_surface1.get_width()+10)
        input_box1.w = width1
        screen.blit(txt_surface1, (input_box1.x+5, input_box1.y+5))
        pygame.draw.rect(screen, color1, input_box1, 2)
        
        txt_surface2 = font.render(text2, True, (0, 0, 0))
        width2 = max(200, txt_surface2.get_width()+10)
        input_box2.w = width2
        screen.blit(txt_surface2, (input_box2.x+5, input_box2.y+5))
        pygame.draw.rect(screen, color2, input_box2, 2)
        
        pygame.display.flip()
        pygame.display.update()

# Call the enter_names() function to get player names
enter_names()

# Game loop
clock = pygame.time.Clock()
game_over = False
last_speed_change_time = pygame.time.get_ticks()
speed_change_interval = 1000  # Change speed every second (1000 milliseconds)

while not game_over:
    current_time = pygame.time.get_ticks()
    if current_time - last_speed_change_time >= speed_change_interval:
        # Change ball speed
        ball_speed = random.randint(5, 15)
        ball_dx = random.choice((1, -1)) * ball_speed
        ball_dy = random.choice((1, -1)) * ball_speed
        last_speed_change_time = current_time
        
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            game_over = True

    keys = pygame.key.get_pressed()
    if keys[pygame.K_w] and left_paddle_y > 0:
        left_paddle_y -= PADDLE_SPEED
    if keys[pygame.K_s] and left_paddle_y < HEIGHT - PADDLE_HEIGHT:
        left_paddle_y += PADDLE_SPEED
    if keys[pygame.K_UP] and right_paddle_y > 0:
        right_paddle_y -= PADDLE_SPEED
    if keys[pygame.K_DOWN] and right_paddle_y < HEIGHT - PADDLE_HEIGHT:
        right_paddle_y += PADDLE_SPEED

    # Update ball position
    ball_x += ball_dx
    ball_y += ball_dy

    # Ball collisions with top and bottom walls
    if ball_y <= 0 or ball_y >= HEIGHT - BALL_SIZE:
        ball_dy *= -1

    # Ball collisions with paddles
    if (
        ball_x <= PADDLE_WIDTH
        and left_paddle_y <= ball_y <= left_paddle_y + PADDLE_HEIGHT
    ) or (
        ball_x >= WIDTH - PADDLE_WIDTH - BALL_SIZE
        and right_paddle_y <= ball_y <= right_paddle_y + PADDLE_HEIGHT
    ):
        ball_dx *= -1

    # Ball out of bounds
    if ball_x < 0:
        # Player 2 scores
        player2_score += 1
        # Reset ball position
        ball_x = WIDTH // 2
        ball_y = HEIGHT // 2
        ball_dx = random.choice((1, -1)) * ball_speed
        ball_dy = random.choice((1, -1)) * ball_speed
    elif ball_x > WIDTH:
        # Player 1 scores
        player1_score += 1
        # Reset ball position
        ball_x = WIDTH // 2
        ball_y = HEIGHT // 2
        ball_dx = random.choice((1, -1)) * ball_speed
        ball_dy = random.choice((1, -1)) * ball_speed

    # Set the background color
    screen.fill(SKY_BLUE)

    # Draw paddles and ball
    pygame.draw.rect(screen, WHITE, (ball_x, ball_y, BALL_SIZE, BALL_SIZE))
    pygame.draw.rect(screen, WHITE, (0, left_paddle_y, PADDLE_WIDTH, PADDLE_HEIGHT))
    pygame.draw.rect(
        screen,
        WHITE,
        (WIDTH - PADDLE_WIDTH, right_paddle_y, PADDLE_WIDTH, PADDLE_HEIGHT),
    )

    # Draw individual scoreboards
    font = pygame.font.Font(None, 36)
    player1_score_text = font.render(f"{player1_name}: {player1_score}", True, WHITE)
    player2_score_text = font.render(f"{player2_name}: {player2_score}", True, WHITE)
    screen.blit(player1_score_text, (20, 20))
    screen.blit(player2_score_text, (WIDTH - player2_score_text.get_width() - 20, 20))

    # Draw ball speed
    ball_speed_text = font.render(f"Ball Speed: {ball_speed}", True, WHITE)
    screen.blit(ball_speed_text, (WIDTH // 2 - ball_speed_text.get_width() // 2, 20))

    # Check for game end condition
    if player1_score >= 10:
        winner_text = f"{player1_name} wins!"
        game_over = True
    elif player2_score >= 10:
        winner_text = f"{player2_name} wins!"
        game_over = True

    # Update the display
    pygame.display.flip()

    # Cap the frame rate
    clock.tick(30)

# Display the winner and wait for a moment before quitting
font = pygame.font.Font(None, 72)
winner_surface = font.render(winner_text, True, RED)
winner_rect = winner_surface.get_rect(center=(WIDTH // 2, HEIGHT // 2))
screen.blit(winner_surface, winner_rect)
pygame.display.flip()
time.sleep(3)  # Display the winner for 2 seconds
pygame.quit()
