import pygame
import random
import time

pygame.init()
white = (255, 255, 255)
yellow = (255, 255, 102)
black = (0, 0, 0)
red = (213, 50, 80)
green = (0, 255, 0)
blue = (50, 153, 100)
deep_blue = (0, 0, 255)
WIDTH = 1000
HEIGHT = 760

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('Моя змейка')
clock = pygame.time.Clock()
steps = 20
snake_speed = 15
base_snake_speed = 15
FPS = 15
font_style = pygame.font.SysFont("bahnschrift", 25)
SCORE = pygame.font.SysFont("comicsansms", 35)


def Your_score(score):
    value = SCORE.render("Ваш счёт: " + str(score), True, yellow)
    screen.blit(value, [0, 0])


def our_snake(snake_block, snake_list):
    for x in snake_list:
        pygame.draw.rect(screen, black, [x[0], x[1], snake_block, snake_block])


def message(msg, color):
    mesg = font_style.render(msg, True, color)
    screen.blit(mesg, [WIDTH / 6, HEIGHT / 3])


def gameLoop():
    global snake_speed
    game_over = False
    game_close = False
    x1 = WIDTH // 2
    y1 = HEIGHT // 2
    x1_change = 0
    y1_change = 0
    snake_List = []
    Length_of_snake = 1
    foodx = round(random.randrange(0, WIDTH - steps) // steps) * steps
    foody = round(random.randrange(0, HEIGHT - steps) // steps) * steps
    special_food = {'speed_up': [], 'speed_down': []}
    special_food_time = time.time()
    special_effect_time = time.time()


    while not game_over:
        while game_close == True:
            screen.fill(blue)
            Your_score(Length_of_snake - 1)
            our_snake(steps, snake_List)
            message("Вы проиграли! Нажмите Q для выхода или C для повторной игры", red)
            snake_speed = 15
            pygame.display.update()

            for event in pygame.event.get():

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_q:
                        game_over = True
                        game_close = False
                    if event.key == pygame.K_c:
                        gameLoop()
                if event.type == pygame.QUIT:
                    game_over = True
                    game_close = False

        now_time = time.time()
        if now_time - special_food_time > 10:
            special_food = {'speed_up': [], 'speed_down': []}
        if now_time - special_effect_time > 10:
            snake_speed = base_snake_speed

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game_over = True
            if event.type == pygame.KEYDOWN:
                if event.key == (pygame.K_LEFT or event.key == pygame.K_a) and x1_change != steps:
                    x1_change = -steps
                    y1_change = 0
                elif event.key == (pygame.K_RIGHT or event.key == pygame.K_d) and x1_change != - steps:
                    x1_change = steps
                    y1_change = 0
                elif event.key == (pygame.K_UP or event.key == pygame.K_w) and y1_change != steps:
                    y1_change = -steps
                    x1_change = 0
                elif event.key == (pygame.K_DOWN or event.key == pygame.K_s) and y1_change != -steps:
                    y1_change = steps
                    x1_change = 0
        if x1 >= WIDTH or x1 < 0 or y1 >= HEIGHT or y1 < 0:
            game_close = True
        x1 += x1_change
        y1 += y1_change
        screen.fill(blue)
        pygame.draw.rect(screen, green, [foodx, foody, steps, steps])
        if special_food['speed_up']:
            pygame.draw.rect(screen, red, [special_food['speed_up'][0], special_food['speed_up'][1], steps, steps])
        elif special_food['speed_down']:
            pygame.draw.rect(screen, deep_blue, [special_food['speed_down'][0], special_food['speed_down'][1], steps, steps])

        snake_Head = [x1, y1]
        snake_List.append(snake_Head)
        print(snake_List)

        if len(snake_List) > Length_of_snake:
            del snake_List[0]

        for x in snake_List[:-1]:
            if x == snake_Head:
                game_close = True

        our_snake(steps, snake_List)
        Your_score(Length_of_snake - 1)
        pygame.display.update()

        if x1 == foodx and y1 == foody:
            Length_of_snake += 1
            while [foodx, foody] in snake_List or [foodx, foody] in [special_food['speed_down'] + special_food['speed_up']]:
                foodx = round(random.randrange(0, WIDTH - steps) / steps) * steps
                foody = round(random.randrange(0, HEIGHT - steps) / steps) * steps
        if [x1, y1] in special_food.values():
            if [x1, y1] == special_food['speed_up']:
                Length_of_snake += 1
                snake_speed = 10
                special_food = {'speed_up': [], 'speed_down': []}
            else:
                Length_of_snake += 1
                snake_speed = 20
                special_food = {'speed_up': [], 'speed_down': []}
            special_effect_time = time.time()

        if not special_food['speed_up'] and not special_food['speed_down']:
            randnum = random.randint(0, 100)
            if randnum == 0:
                randnum = random.randint(0, 2)
                if randnum == 0:
                    while special_food['speed_up'] == [] or special_food['speed_up'] in snake_List or special_food['speed_up'] == [foodx, foody]:
                        speed_up_foodx = round(random.randrange(0, WIDTH - steps) / steps) * steps
                        speed_up_foody = round(random.randrange(0, HEIGHT - steps) / steps) * steps
                        special_food['speed_up'] = [speed_up_foodx, speed_up_foody]
                else:
                    while special_food['speed_down'] == [] or special_food['speed_down'] in snake_List or special_food['speed_down'] == [foodx, foody]:
                        speed_down_foodx = round(random.randrange(0, WIDTH - steps) / steps) * steps
                        speed_down_foody = round(random.randrange(0, HEIGHT - steps) / steps) * steps
                        special_food['speed_down'] = [speed_down_foodx, speed_down_foody]
                special_food_time = time.time()

        clock.tick(snake_speed)
    pygame.quit()
    quit()


gameLoop()
