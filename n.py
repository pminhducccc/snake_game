import sys
import pygame
from pygame.locals import QUIT
import random
import json
from time import sleep

# Set up a file
best_score = json.load(open("score.json", "r+"))

# Setup pygame
pygame.init()

# Define color code (RGB)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)

# Init working screen
g_display_width = 800
g_display_height = 600

# Init snake property
g_snake_block = 10
g_snake_speed = 30

g_clock = pygame.time.Clock()

# Init working display
g_display = pygame.display.set_mode((g_display_width, g_display_height))
pygame.display.set_caption("Snake game!")

# Method game
# Show message display
def ShowMessage(msg, color, coord_x, coord_y):
    font_style = pygame.font.SysFont(None, 30)
    msg_convert = font_style.render(msg, True, color)
    g_display.blit(msg_convert, [coord_x, coord_y])


# draw snake
def DrawSnake(snake):
    for block in snake:
        pygame.draw.rect(g_display, BLACK, [block[0], block[1], g_snake_block, g_snake_block])

# main display
def GameLoop():
    # ========================== Init default value =============================
    # Mode game
    game_run = True
    game_close = False
    # init coords snake| default screen center
    snake_coord_x = g_display_width / 2
    snake_coord_y = g_display_height / 2

    # init x,y change snake
    snake_x_change = 0
    snake_y_change = 0

    # init x,y food default
    food_x = (round(random.randrange(0, g_display_width - g_snake_block))//10)*10
    food_y = (round(random.randrange(0, g_display_height - g_snake_block))//10)*10
    
    # score:
    score = 0

    # snake:
    snake = []
    length = 1
    # game run:
    m = 0
    # ==========================================================================

    # main loop
    while game_run:
        # Play Again
        PlayAgain(game_close)

        # Screen player
        # Handle event player
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    snake_x_change = -g_snake_block
                    snake_y_change = 0
                elif event.key == pygame.K_RIGHT:
                    snake_x_change = g_snake_block
                    snake_y_change = 0
                elif event.key == pygame.K_UP:
                    snake_x_change = 0
                    snake_y_change = -g_snake_block
                elif event.key == pygame.K_DOWN:
                    snake_x_change = 0
                    snake_y_change = g_snake_block

        # --------------- Snake crash in to the wall ---------------------------
        if (snake_coord_x >= g_display_width \
            or snake_coord_x < 0 \
            or snake_coord_y >= g_display_height \
            or snake_coord_y < 0) or m == 1:
            game_close = True
            if score > best_score["score"]:
                best_score["score"] = score
                with open("score.json", "w") as k:
                    json.dump(best_score, k)
                    g_display.fill(WHITE)
            mess = "Your score is: " + str(score) + " . Best score: " + str(best_score["score"])
            ShowMessage(mess, 
                        RED, 
                        g_display_width/4, 
                        g_display_height/2)
            pygame.display.update()
            sleep(3)

        # update x,y change to snake x,y
        snake_coord_x += snake_x_change
        snake_coord_y += snake_y_change

        # Init the snake
        snake_head = [snake_coord_x, snake_coord_y]
        snake.append(snake_head)
        if len(snake) > length:
            snake.pop(0)

        for i in range(0, len(snake) - 2):
            if snake_head == snake[i]:
                m = 1
        # eating food
        if snake_coord_x == food_x and snake_coord_y == food_y:
            food_x = (round(random.randrange(0, g_display_width - g_snake_block))//10)*10
            food_y = (round(random.randrange(0, g_display_height - g_snake_block))//10)*10
            score += 10
            length += 1

        # Draw object
        g_display.fill(WHITE)
        # draw food
        pygame.draw.rect(g_display, BLUE, [
                         food_x, food_y, g_snake_block, g_snake_block])

        # draw snake
        DrawSnake(snake)
        ShowMessage(str(score), BLACK, 0, 0)
        # update screen
        pygame.display.update()

        # setup speed snake
        g_clock.tick(g_snake_speed)

def PlayAgain(game_close):
    while game_close == True:
        # Show message game lost and player instruction
        g_display.fill(WHITE)
        ShowMessage(
            "You Lost! SPACE to Play Again !!!",
            RED,
            g_display_width / 3,
            g_display_height / 2)
        pygame.display.update()

        # Handle event keyboard user
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    GameLoop()
            elif event.type == pygame.QUIT:

                pygame.quit()

if __name__ == "__main__":
    GameLoop()
    sys.exit()
