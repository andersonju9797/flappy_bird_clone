import pygame
import time
import random

# define constants

display_width = 290
display_height = 510

bird_w = 45
bird_h = 32

bird_speed = 7
bird_gravity = 0.4

GAP = 120
pipe_height = 430
pipe_width = 70

land_speed = 2
pipe_speed = 2

black = (0, 0, 0)
white = (255, 255, 255)
red = (255, 0, 0)
bright_red = (200, 0, 0)
green = (0, 200, 0)
bright_green = (0, 255, 0)

# block_color = (53, 115, 255)
background_color = (93, 186, 200)

background_img = pygame.image.load('background.png')
background_img = pygame.transform.scale(background_img, (300, 510))
land_img = pygame.image.load('land.png')
land_img = pygame.transform.scale(land_img, (336, 90))

bird_img = pygame.image.load('bird.png')
bird_up_img = pygame.image.load('bird_wing_up.png')
bird_down_img = pygame.image.load('bird_wing_down.png')
bird_img = pygame.transform.scale(bird_img, (45, 32))
bird_up_img = pygame.transform.scale(bird_up_img, (45, 32))
bird_down_img = pygame.transform.scale(bird_down_img, (45, 32))

pipe_top_img = pygame.image.load('pipe_top.png')
pipe_top_img = pygame.transform.scale(pipe_top_img, (70, 430))
pipe_bot_img = pygame.image.load('pipe_bot.png')
pipe_bot_img = pygame.transform.scale(pipe_bot_img, (70, 430))


# initiate pygame variables

pygame.init()
game_display = pygame.display.set_mode((display_width, display_height))
pygame.display.set_caption('Flappy Bird Clone')
clock = pygame.time.Clock()

large_text = pygame.font.SysFont(None, 54)
small_text = pygame.font.SysFont(None, 24)
tiny_text = pygame.font.SysFont(None, 12)


class PipePair:
    def __init__(self, top, bot):
        self.top = top
        self.bot = bot

    def move(self):
        self.top.move()
        self.bot.move(self.top)


class Pipe:
    def __init__(self, x, y):
        self.x = x
        self.y = y


class TopPipe(Pipe):
    def __init__(self, x, y):
        Pipe.__init__(self, x, y)
        self.img = pipe_top_img

    def reappear(self):
        self.x = display_width
        self.y = random.randrange(-410, -160)

    def move(self):
        self.x -= pipe_speed
        if self.x <= -pipe_width:
            self.reappear()


class BotPipe(Pipe):
    def __init__(self, x, y):
        Pipe.__init__(self, x, y)
        self.img = pipe_bot_img

    def move(self, top):
        self.x = top.x
        self.y = top.y + pipe_height + GAP


def display_message(text):
    text_surface, text_rectangle = text_objects(text, large_text)
    text_rectangle.center = (display_width/2, display_height/2)
    game_display.blit(text_surface, text_rectangle)
    pygame.display.update()

def text_objects(text, font):
    text_surface = font.render(text, True, black)
    return text_surface, text_surface.get_rect()

def button(msg, x, y, w, h, ic, ac, action=None):
    mouse = pygame.mouse.get_pos()
    click = pygame.mouse.get_pressed()

    if x+w > mouse[0] > x and y+h > mouse[1] > y:
        pygame.draw.rect(game_display, ac,(x,y,w,h))
        if click[0] == 1 and action != None:
            action()
    else:
        pygame.draw.rect(game_display, ic,(x,y,w,h))

    textSurf, textRect = text_objects(msg, small_text)
    textRect.center = ( (x+(w/2)), (y+(h/2)) )
    game_display.blit(textSurf, textRect)

def object(x, y, img):
    game_display.blit(img, (x, y))


def quit_game():
    pygame.quit()
    quit()

def crash():
    display_message('You Crashed!')
    time.sleep(1)

    pygame.display.update()

    game_over = True
    while game_over:
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_q:
                    quit_game()
                elif event.key == pygame.K_BACKSPACE:
                    intro_screen()
                else:
                    game_loop()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                game_loop()

def collision(x, y, pair1, pair2):
    pair1x = pair1.top.x
    top1y = pair1.top.y
    pair2x = pair2.top.x
    top2y = pair2.top.y

    if x + bird_w > pair1x and x < pair1x + pipe_width:
        if y < top1y + pipe_height or y + bird_h > top1y + pipe_height + GAP:
            return True
    elif x + bird_w > pair2x and x < pair2x + pipe_width:
        if y < top2y + pipe_height or y + bird_h > top2y + pipe_height + GAP:
            return True
    else:
        return False

def intro_screen():
    intro = True
    land_start_x = 0
    while intro:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                quit_game()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_q:
                    quit_game()
                if event.key == pygame.K_RETURN:
                    game_loop()

        game_display.blit(background_img, (0,0))
        game_display.blit(land_img, (land_start_x, display_height-90))
        land_start_x -= land_speed
        if land_start_x <= -24:
            land_start_x = 0

        text_surface, text_rectangle = text_objects('Flappy Clone', large_text)
        text_rectangle.center = (display_width / 2, display_height / 2)
        game_display.blit(text_surface, text_rectangle)

        instructions_text = tiny_text.render('Use left and right arrow keys to move', True, black)
        pause_text = tiny_text.render('Press \'p\' to pause', True, black)
        quit_text = tiny_text.render('Press \'q\' to quit', True, black)
        game_display.blit(instructions_text, (0, 0))
        game_display.blit(pause_text, (0, 20))
        game_display.blit(quit_text, (0, 40))

        button('start!', display_width / 2 - 100, display_height / 2 + 150, 200, 100, green, bright_green, game_loop)

        pygame.display.update()
        clock.tick(60)

def game_loop():
    x = display_width * 0.25
    y = display_height * 0.5 - 6
    v = 0
    angle = 0
    anglev = 0

    pipe_top_x = display_width + 100
    pipe_top_y = random.randrange(-410, -160)
    pipe_bot_x = pipe_top_x
    pipe_bot_y = pipe_top_y + pipe_height + GAP

    top1 = TopPipe(pipe_top_x, pipe_top_y)
    bot1 = BotPipe(pipe_bot_x, pipe_bot_y)
    pair1 = PipePair(top1, bot1)

    pipe_top_2_x = display_width + (display_width + pipe_width) / 2 + 100
    pipe_top_2_y = random.randrange(-410, -160)
    pipe_bot_2_x = pipe_top_2_x
    pipe_bot_2_y = pipe_top_2_y + pipe_height + GAP

    top2 = TopPipe(pipe_top_2_x, pipe_top_2_y)
    bot2 = BotPipe(pipe_bot_2_x, pipe_bot_2_y)
    pair2 = PipePair(top2, bot2)



    land_start_x = 0

    game_exit = False

    while not game_exit:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                quit_game()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_q:
                    quit_game()
                if event.key == pygame.K_w:
                    v = -bird_speed
                    anglev += 5

        if v < 8:
            v += bird_gravity

        y += v

        land_start_x -= land_speed
        if land_start_x <= -24:
            land_start_x = 0

        if v > 0:
            img = bird_up_img
        elif v < 0 and v > -3:
            img = bird_img
        else:
            img = bird_down_img
            anglev += 30

        if v > 2:
            anglev -= 0.2
        angle += anglev

        if angle <= -90:
            angle = -90
            anglev = 0
        elif angle >= 10:
            angle = 10
            anglev = 0
        img = pygame.transform.rotate(img, angle)

        if y + bird_h >= display_height - 90:
            game_display.blit(background_img, (0, 0))

            object(pair1.top.x, pair1.top.y, pair1.top.img)
            object(pair1.bot.x, pair1.bot.y, pair1.bot.img)
            object(pair2.top.x, pair2.top.y, pair2.top.img)
            object(pair2.bot.x, pair2.bot.y, pair2.bot.img)

            game_display.blit(land_img, (land_start_x, display_height - 90))
            object(x, display_height - 90 - bird_h, img) # bird
            pygame.display.update()
            crash()

        pair1.move()
        pair2.move()

        game_display.blit(background_img, (0, 0))
        object(pair1.top.x, pair1.top.y, pair1.top.img)
        object(pair1.bot.x, pair1.bot.y, pair1.bot.img)
        object(pair2.top.x, pair2.top.y, pair2.top.img)
        object(pair2.bot.x, pair2.bot.y, pair2.bot.img)

        game_display.blit(land_img, (land_start_x, display_height - 90))
        object(x, y, img) # bird
        pygame.display.update()

        # if collision(x, y, pair1, pair2):
        #     crash()

        clock.tick(60)

intro_screen()