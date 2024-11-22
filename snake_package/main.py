import pygame
import random
import time
from config import *

pygame.init()

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('Моя змейка')
clock = pygame.time.Clock()
font_style = pygame.font.SysFont("bahnschrift", 25)
SCORE = pygame.font.SysFont("comicsansms", 35)


def Your_score(score):
    """Выводит счёт игрока на экран"""
    value = SCORE.render("Ваш счёт: " + str(score), True, yellow)
    screen.blit(value, [0, 0])


def Our_snake(snake_block, snake_list):
    """Отрисовывает саму змейку"""
    for x in snake_list:
        pygame.draw.rect(screen, black, [x[0], x[1], snake_block, snake_block])


def message(msg, color):
    """Форматирует текст и выыодит на экран"""
    mesg = font_style.render(msg, True, color)
    screen.blit(mesg, [WIDTH / 6, HEIGHT / 3])


def gameLoop():
    """Тело самой игры"""
    global snake_speed
    game_over = False
    game_close = False
    x1 = ((WIDTH // steps) // 2) * steps
    y1 = ((HEIGHT // steps) // 2) * steps
    x1_change = 0
    y1_change = 0
    snake_List = []
    Length_of_snake = 1
    foodx = round(random.randrange(0, WIDTH - steps) // steps) * steps
    foody = round(random.randrange(0, HEIGHT - steps) // steps) * steps
    special_food = {'speed_up': [], 'speed_down': []}
    special_food_time = time.time()
    special_effect_time = time.time()

    # Цикл работает пока пользователь не закрыл игру
    while not game_over:
        # Цикл работает если пользователь проиграл, но всё ещё не закрыл игру
        while game_close:
            screen.fill(dark_green)
            Your_score(Length_of_snake - 1)
            Our_snake(steps, snake_List)
            message("Вы проиграли! Нажмите Q для выхода или C для повторной игры", red)
            snake_speed = base_snake_speed
            pygame.display.update()

            # Цикл смотри все события, пришедшие от пользователя
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
        # Проверка времени еды и эффекта от еды
        if now_time - special_food_time > 10:
            special_food = {'speed_up': [], 'speed_down': []}
        if now_time - special_effect_time > 10:
            snake_speed = base_snake_speed

        # Смотрим все события пришедшие от пользователя и, если необходимо, меняем направление змейки
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

        # Если врезается в границы, то игра заканчивается
        if x1 >= WIDTH or x1 < 0 or y1 >= HEIGHT or y1 < 0:
            game_close = True
        x1 += x1_change
        y1 += y1_change
        screen.fill(dark_green)

        # Рисуем еду
        pygame.draw.rect(screen, green, [foodx, foody, steps, steps])
        if special_food['speed_up']:
            pygame.draw.rect(screen, red, [special_food['speed_up'][0], special_food['speed_up'][1], steps, steps])
        elif special_food['speed_down']:
            pygame.draw.rect(screen, deep_blue,
                             [special_food['speed_down'][0], special_food['speed_down'][1], steps, steps])

        snake_Head = [x1, y1]
        snake_List.append(snake_Head)

        if len(snake_List) > Length_of_snake:
            del snake_List[0]

        # Если змейка врезалась в себя, то игра окончена
        for x in snake_List[:-1]:
            if x == snake_Head:
                game_close = True

        Our_snake(steps, snake_List)
        Your_score(Length_of_snake - 1)
        pygame.display.update()

        # Если съели еду, то меняем знаечение и добавляем эффект
        if x1 == foodx and y1 == foody:
            Length_of_snake += 1
            while [foodx, foody] in snake_List or [foodx, foody] in [
                special_food['speed_down'] + special_food['speed_up']]:
                foodx = round(random.randrange(0, WIDTH - steps) / steps) * steps
                foody = round(random.randrange(0, HEIGHT - steps) / steps) * steps
        if [x1, y1] in special_food.values():
            if [x1, y1] == special_food['speed_up']:
                Length_of_snake += 1
                snake_speed = snake_speed_up
                special_food = {'speed_up': [], 'speed_down': []}
            else:
                Length_of_snake += 1
                snake_speed = snake_speed_down
                special_food = {'speed_up': [], 'speed_down': []}
            special_effect_time = time.time()

        # Генерируем еду с эффектами
        if not special_food['speed_up'] and not special_food['speed_down']:
            randnum = random.randint(0, 100)
            if randnum == 0:
                randnum = random.randint(0, 2)
                if randnum == 0:
                    while special_food['speed_up'] == [] or special_food['speed_up'] in snake_List or special_food[
                        'speed_up'] == [foodx, foody]:
                        speed_up_foodx = round(random.randrange(0, WIDTH - steps) / steps) * steps
                        speed_up_foody = round(random.randrange(0, HEIGHT - steps) / steps) * steps
                        special_food['speed_up'] = [speed_up_foodx, speed_up_foody]
                else:
                    while special_food['speed_down'] == [] or special_food['speed_down'] in snake_List or special_food[
                        'speed_down'] == [foodx, foody]:
                        speed_down_foodx = round(random.randrange(0, WIDTH - steps) / steps) * steps
                        speed_down_foody = round(random.randrange(0, HEIGHT - steps) / steps) * steps
                        special_food['speed_down'] = [speed_down_foodx, speed_down_foody]
                special_food_time = time.time()

        # Устанавливаем фпс
        clock.tick(snake_speed)
    pygame.quit()
    quit()


gameLoop()
