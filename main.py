import pygame
import random

from snake import Snake, Cube

pygame.init()


# INIT VARIABLES
win_width = 500
win_height = 500
win = pygame.display.set_mode((win_width, win_height))
pygame.display.set_caption("Snake")
run_game = True
food_color = (255, 255, 0)


# GRID
lines_num = 20
offset_vertical = win_width / lines_num
start_pos_vertical = 0
offset_horizontal = win_height / lines_num
start_pos_horizontal = 0



# CHARACTER
x = 3*offset_horizontal
y = 3*offset_vertical
width = offset_horizontal
height = offset_vertical
vel = offset_horizontal
food_present = False


#FUNCTIONS
#MORE FOOD
def add_food(snake):
    food_x = random.randint(1, lines_num - 2) * offset_horizontal
    food_y = random.randint(1, lines_num - 2) * offset_vertical
    food_present = True
    snake.add_food(food_x, food_y, width, height, food_color)
#GAME OVER
def death(snake):
    font = pygame.font.Font(pygame.font.get_default_font(), 32)
    game_over = font.render('Game Over', True, (255, 0, 0), (0,0,0)) 
    game_over_rect = game_over.get_rect()  
    game_over_rect.center = (win_width // 2, win_height // 2) 
    restart = font.render('Press R to restart', True, (0, 0, 0), (255, 255, 255))
    restart_rect = restart.get_rect()
    restart_rect.center = (win_width // 2, win_height // 2 + 100)
    score = snake.body_lenght
    text_score = font.render('Your score: '+str(score), True, (255, 255, 255), (0,0,0))
    text_score_rect = text_score.get_rect()
    text_score_rect.center = (win_width // 2, win_height // 2 + 50) 
    win.blit(game_over, game_over_rect)
    win.blit(text_score, text_score_rect)
    win.blit(restart, restart_rect)

#RUN GAME
snake = Snake(x, y, width, height, vel, win_width, win_height)
while run_game:
    pygame.time.delay(70)
    # EVENTS
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run_game = False
        keys = pygame.key.get_pressed()
        head = snake.body[0]
        current_direction = head.current_dir
        current_head_x = head.x
        current_head_y = head.y
        #BREAK NECESSARY TO HANDLE MULTIPLE USER INPUTS AT THE SAME TIME
        for key in keys:
            if keys[pygame.K_LEFT] and current_direction != "Right":
                snake.set_dir(3)
                current_direction = "Left"
                break
            elif keys[pygame.K_RIGHT] and current_direction != "Left":
                snake.set_dir(4)
                current_direction = "Right"
                break
            elif keys[pygame.K_UP] and current_direction != "Down":
                snake.set_dir(1)
                current_direction = "Up"
                break
            elif keys[pygame.K_DOWN] and current_direction != "Up":
                snake.set_dir(2)
                current_direction = "Down"
                break
            elif keys[pygame.K_r] and snake.dead:
                snake.reinitialize(x, y, width, height, vel, win_width, win_height)

    # SPAWN FOOD
    if not snake.hungry:
        add_food(snake)
    #MOVEMENT AND REFRESH 
    snake.move()
    win.fill((0, 0, 0))
    #CHECK IF THE SNAKE IS DEAD OR HAS OVERCOME THE BOUNDARIES
    if not snake.dead:
        for snake_cube in snake.body:
            pygame.draw.rect(win, snake_cube.color,
                         (snake_cube.x, snake_cube.y, snake_cube.width, snake_cube.height))
        if snake.hungry:
            food = snake.food
            pygame.draw.rect(
                win, food.color, (food.x, food.y, food.width, food.height))
    else:
        death(snake)
    pygame.display.update()
pygame.quit()
