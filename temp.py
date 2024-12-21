import pygame
import time
import random

# Pygame'i başlatıyoruz
pygame.init()

# Oyun ekranı boyutları
width = 800
height = 600

# Renkler
white = (255, 255, 255)
yellow = (255, 255, 102)
black = (0, 0, 0)
red = (213, 50, 80)
green = (34, 177, 76)  # Yılan için yeşil renk
blue = (50, 153, 213)
orange = (255, 165, 0)
light_blue = (0, 191, 255)  # Daha modern bir mavi
dark_blue = (25, 25, 112)  # Koyu mavi, arka plan için
light_gray = (211, 211, 211)
dark_gray = (169, 169, 169)

# Ekran ayarları
dis = pygame.display.set_mode((width, height))
pygame.display.set_caption('Modern Yılan Oyunu')

# Yılan ayarları
snake_block = 20

# Fontlar (Modern ve estetik fontlar)
font_style = pygame.font.SysFont("comicsansms", 50, bold=True)
score_font = pygame.font.SysFont("comicsansms", 35, bold=True)
menu_font = pygame.font.SysFont("comicsansms", 30)

# Sesler
pygame.mixer.init()
hit_sound = pygame.mixer.Sound('hit_sound.wav')
eat_sound = pygame.mixer.Sound('eat_sound.wav')

# Skor yazdırma fonksiyonu
def your_score(score):
    value = score_font.render("Skor: " + str(score), True, black)
    dis.blit(value, [width / 2 - 100, 10])

# Yılanı oval şekilde çizme fonksiyonu
def our_snake(snake_block, snake_list, snake_color):
    for i, x in enumerate(snake_list):
        pygame.draw.ellipse(dis, snake_color, [x[0], x[1], snake_block, snake_block])

# Mesaj yazdırma fonksiyonu
def message(msg, color, y_offset=0, font=font_style):
    mesg = font.render(msg, True, color)
    dis.blit(mesg, [width / 6, height / 3 + y_offset])

# Duvarları çizme fonksiyonu (duvarlı modda kullanılacak)
def draw_walls():
    pygame.draw.rect(dis, orange, [0, 0, width, snake_block])  # Üst duvar
    pygame.draw.rect(dis, orange, [0, height - snake_block, width, snake_block])  # Alt duvar
    pygame.draw.rect(dis, orange, [0, 0, snake_block, height])  # Sol duvar
    pygame.draw.rect(dis, orange, [width - snake_block, 0, snake_block, height])  # Sağ duvar

# Renk Seçim Menüsü
def select_snake_color():
    selected_color = None
    while selected_color is None:
        dis.fill(light_blue)
        message("Yılan Rengini Seçin", green, -100, font=font_style)
        message("1: Yeşil", white, 0, font=menu_font)
        message("2: Kırmızı", white, 50, font=menu_font)
        message("3: Mavi", white, 100, font=menu_font)
        message("4: Sarı", white, 150, font=menu_font)

        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_1:
                    selected_color = green
                elif event.key == pygame.K_2:
                    selected_color = red
                elif event.key == pygame.K_3:
                    selected_color = blue
                elif event.key == pygame.K_4:
                    selected_color = yellow
    return selected_color

# Yılan hızı seçme menüsü
def select_speed():
    speed = None
    while speed is None:
        dis.fill(light_blue)
        message("Yılan Hızını Seçin", green, -100, font=font_style)
        message("1: Yavaş", white, 0, font=menu_font)
        message("2: Orta", white, 50, font=menu_font)
        message("3: Hızlı", white, 100, font=menu_font)

        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_1:
                    speed = 10  # Yavaş hız
                elif event.key == pygame.K_2:
                    speed = 20  # Orta hız
                elif event.key == pygame.K_3:
                    speed = 30  # Hızlı hız
    return speed

# Başlangıç menüsü
def game_intro():
    intro = True
    while intro:
        dis.fill(dark_blue)
        message("Modern Yılan Oyunu", yellow, -100)
        message("Başlamak için C, Çıkmak için Q tuşuna basın", white, 0, font=menu_font)

        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                intro = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_q:
                    pygame.quit()
                    quit()
                if event.key == pygame.K_c:
                    snake_color = select_snake_color()
                    speed = select_speed()
                    mod_select(snake_color, speed)

# Mod seçme fonksiyonu
def mod_select(snake_color, speed):
    selected_mode = None
    while selected_mode is None:
        dis.fill(light_blue)
        message("Mod Seçin", green, -100, font=font_style)
        message("1: Normal Mod", white, 0, font=menu_font)
        message("2: Duvarlı Mod", white, 50, font=menu_font)

        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_1:
                    selected_mode = "normal"
                if event.key == pygame.K_2:
                    selected_mode = "walls"
    gameLoop(selected_mode, snake_color, speed)

# Ana oyun fonksiyonu
def gameLoop(mode, snake_color, speed):
    game_over = False
    game_close = False

    # Başlangıçta yılanın başlangıç konumu
    x1 = width / 2
    y1 = height / 2

    x1_change = 0
    y1_change = 0

    snake_List = []
    Length_of_snake = 1

    # Yiyecek başlangıç konumu
    foodx = round(random.randrange(0, width - snake_block) / 20.0) * 20.0
    foody = round(random.randrange(0, height - snake_block) / 20.0) * 20.0

    # Yön kontrolü
    direction = "RIGHT"  # Başlangıçta yılan sağa hareket ediyor.

    # Oyun döngüsü
    while not game_over:

        while game_close == True:
            dis.fill(light_blue)
            message("Kaybettin! E-Devam Q-Çıkış", red, -100, font=font_style)
            your_score(Length_of_snake - 1)
            pygame.display.update()

            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_q:
                        game_over = True
                        game_close = False
                    if event.key == pygame.K_e:
                        gameLoop(mode, snake_color, speed)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game_over = True
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT and direction != "RIGHT":
                    x1_change = -snake_block
                    y1_change = 0
                    direction = "LEFT"
                elif event.key == pygame.K_RIGHT and direction != "LEFT":
                    x1_change = snake_block
                    y1_change = 0
                    direction = "RIGHT"
                elif event.key == pygame.K_UP and direction != "DOWN":
                    y1_change = -snake_block
                    x1_change = 0
                    direction = "UP"
                elif event.key == pygame.K_DOWN and direction != "UP":
                    y1_change = snake_block
                    x1_change = 0
                    direction = "DOWN"

        if mode == "normal":
            # Yılan ekranın bir tarafından çıkıp diğer tarafından giriş yapacak şekilde sınır kontrolü
            if x1 >= width:
                x1 = 0
            elif x1 < 0:
                x1 = width - snake_block
            if y1 >= height:
                y1 = 0
            elif y1 < 0:
                y1 = height - snake_block

        x1 += x1_change
        y1 += y1_change
        dis.fill(dark_blue)

        # Duvarlı modda duvarları çiziyoruz
        if mode == "walls":
            draw_walls()

        # Yiyeceği çiziyoruz
        pygame.draw.rect(dis, yellow, [foodx, foody, snake_block, snake_block])

        # Yılanın kafasını ekliyoruz
        snake_Head = []
        snake_Head.append(x1)
        snake_Head.append(y1)
        snake_List.append(snake_Head)
        if len(snake_List) > Length_of_snake:
            del snake_List[0]

        for x in snake_List[:-1]:
            if x == snake_Head:
                game_close = True

        # Yılanı oval şekilde çiziyoruz
        our_snake(snake_block, snake_List, snake_color)
        your_score(Length_of_snake - 1)

        pygame.display.update()

        # Yılanın yiyeceği yediğinde
        if x1 == foodx and y1 == foody:
            foodx = round(random.randrange(0, width - snake_block) / 20.0) * 20.0
            foody = round(random.randrange(0, height - snake_block) / 20.0) * 20.0
            Length_of_snake += 1
            eat_sound.play()

        pygame.time.Clock().tick(speed)

    pygame.quit()
    quit()

# Oyunu başlatıyoruz
game_intro()
