import pygame
import random2 as random
import os

pygame.mixer.init()
pygame.init()

# Colors
white = (255, 255, 255)
red = (255, 0, 0)
black = (0, 0, 0)
blue = (0, 0, 255)
g2 = (200, 250, 4)

# Creating window
screen_width = 1000
screen_height = 700
gameWindow = pygame.display.set_mode((screen_width, screen_height))

# Background Image
bgimg = pygame.image.load('Snake game/name1.png')
bgimg = pygame.transform.scale(bgimg, (screen_width, screen_height)).convert_alpha()

# Game Title
pygame.display.set_caption('SNAKE GAME')
icon = pygame.image.load('Snake game/snake2.png')
icon = pygame.transform.scale(icon, (32, 32)).convert_alpha()
pygame.display.set_icon(icon)
pygame.display.update()
clock = pygame.time.Clock()


def text_screen(text, color, x, y, z):
    font = pygame.font.SysFont('celibri', z,italic=True)
    screen_text = font.render(text, True, color)
    gameWindow.blit(screen_text, [x, y])


def plot_snake(gameWindow, color, snk_list, snake_size, snake_x, snake_y):
    for x, y in snk_list:
        pygame.draw.circle(gameWindow, color, (x, y), snake_size / 2)

    bgimg0 = pygame.image.load('Snake game/snake2.png')
    bgimg0 = pygame.transform.scale(bgimg0, (40, 40)).convert_alpha()
    gameWindow.blit(bgimg0, (snake_x - 20, snake_y - 20))


def welcome():
    exit_game = False
    while not exit_game:
        gameWindow.fill((23, 210, 229))
        bgimg2 = pygame.image.load('Snake game/Play.png')
        bgimg2 = pygame.transform.scale(bgimg2, (screen_width, 700)).convert_alpha()
        gameWindow.blit(bgimg2, (0, 0))
        text_screen('Welcome to Snake Game', g2, 185, 70, 75)
        text_screen('~ by RISHI ', white, 375, 200, 55)
        text_screen('Click SAPCE to START', blue, 335, 300, 40)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                exit_game = True

            if event.type == pygame.KEYDOWN:

                if event.key == pygame.K_SPACE:
                    pygame.mixer.music.load('Snake game/back.mp3')
                    pygame.mixer.music.play()
                    gameloop()

        pygame.display.update()
        clock.tick(40)


# Game Loop
def gameloop():
    # Game specific variables
    exit_game = False
    game_over = False
    snake_x = 350
    snake_y = 350
    velocity_x = 0
    velocity_y = 0
    snk_list = []
    snk_length = 1

    # Check if hiscore file exists
    if (not os.path.exists('Snake game/hiscore.txt')):
        with open('hiscore.txt', 'w') as f:
            f.write('0')

    with open('Snake game/hiscore.txt', 'r') as f:
        hiscore = f.read()

    food_x = random.randint(50, screen_width / 2)
    food_y = random.randint(50, screen_height / 2)
    score = 0
    init_velocity = 2
    snake_size = 30
    fps = 90
    while not exit_game:
        if game_over:
            with open('Snake game/hiscore.txt', 'w') as f:
                f.write(str(hiscore))
            gameWindow.fill((10, 210, 150))
            bgimg1 = pygame.image.load('Snake game/game_over.png')
            bgimg1 = pygame.transform.scale(bgimg1, (screen_width, screen_height)).convert_alpha()
            gameWindow.blit(bgimg1, (0, 0))


            text_screen('Score: ' + str(score), g2, 10, 10, 50)
            text_screen('You Lose', g2, 10, 40, 50)
            text_screen('ENTER to replay', red, 310, 550, 60)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    exit_game = True

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN:
                        welcome()

        else:

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    exit_game = True

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RIGHT or event.key == pygame.K_KP6:
                        velocity_x = init_velocity
                        velocity_y = 0

                    if event.key == pygame.K_LEFT or event.key == pygame.K_KP4:
                        velocity_x = - init_velocity
                        velocity_y = 0

                    if event.key == pygame.K_UP or event.key == pygame.K_KP8:
                        velocity_y = - init_velocity
                        velocity_x = 0

                    if event.key == pygame.K_DOWN or event.key == pygame.K_KP2:
                        velocity_y = init_velocity
                        velocity_x = 0

            snake_x = snake_x + velocity_x
            snake_y = snake_y + velocity_y

            if (abs(snake_x - food_x) < 18 and abs(snake_y - food_y) < 18) or (
                    abs(food_x - snake_x + 30) < 20 and abs(food_y - snake_y + 30) < 20):
                score += 10
                pygame.mixer.music.load('Snake game/point.mp3')
                pygame.mixer.music.play()
                init_velocity += 0.2
                food_x = random.randint(50, screen_width - 50)
                food_y = random.randint(50, screen_height - 50)
                snk_length += 5
                if score > int(hiscore):
                    hiscore = score
                    pygame.mixer.music.load('Snake game/yeah.mp3')
                pygame.mixer.music.play()

            gameWindow.fill(white)

            gameWindow.blit(bgimg, (0, 0))

            text_screen('Score: ' + str(score) + '  Hiscore: ' + str(hiscore), white, 10, 15, 55)

            bgimgf = pygame.image.load('Snake game/rat.png')
            bgimgf = pygame.transform.scale(bgimgf, (50, 50)).convert_alpha()
            gameWindow.blit(bgimgf, (food_x, food_y))

            head = []
            head.append(snake_x)
            head.append(snake_y)
            snk_list.append(head)

            if len(snk_list) > snk_length:
                del snk_list[0]
            if head in snk_list[:-1]:
                head = snk_list
                game_over = True
                pygame.mixer.music.load('Snake game/gam.mp3')
                pygame.mixer.music.play()
            if snake_x < 0 or snake_x > screen_width or snake_y < 0 or snake_y > screen_height:
                game_over = True
                pygame.mixer.music.load('Snake game/gam.mp3')
                pygame.mixer.music.play()
            plot_snake(gameWindow, g2, snk_list, snake_size, snake_x, snake_y)
        pygame.display.update()
        clock.tick(fps)
    pygame.quit()
    quit()


welcome()
