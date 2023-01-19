import pygame
import math
import random
pygame.font.init()
pygame.mixer.init()

pygame.mixer.music.load("Low Roar-Dont be so serious (Death Stranding Music).mp3")
pygame.mixer.music.play(-1)

FPS = 60
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
TRANSPARENT = (0, 0, 0, 0)
screen_x = 500
screen_y = 700
size = (screen_x, screen_y)
#set up screen
screen = pygame.display.set_mode(size)

def main():
    car_x = screen_x//2 - 50
    car_y = screen_y -200
    vel_road = 1
    vel_car = 8
    vel_enemy = 3
    enemies = []
    wave_lenght = 3
    lives = 1
    points = -10
    scroll = 0
    vel_laser = 8

    #set up background
    bg  = pygame.image.load("road.png").convert()
    bg = pygame.transform.scale(bg, (screen_x, screen_y))

    #set clock for gamne
    clock = pygame.time.Clock()

    #calculate tiles 
    bg_height = bg.get_height()
    tiles = math.ceil(screen_y / bg_height) + 1

    #font for text 
    main_font = pygame.font.SysFont("Helvetica", 38, bold = False, italic = True)


    class Shoot(pygame.sprite.Sprite):
        def __init__(self, x, y):
            super(Shoot, self).__init__()
            self.image = pygame.image.load("laser.png")
            self.image = pygame.transform.scale(self.image, (100, 150))
            self.image = pygame.transform.rotate(self.image, (90))
            self.rect = self.image.get_rect()
            self.x = x
            self.y = y

        def draw(self, screen):
            screen.blit(self.image, (self.rect.x, self.rect.y))

        def move(self, vel_laser):
            print("move")
            self.y -= vel_laser

        def off_screen(self, screen_y):
            return not(self.rect.y < 0)



    class Car(pygame.sprite.Sprite):
        COOLDOWN = 30
        def __init__(self, pos):
            super(Car, self).__init__()
            self.image = pygame.image.load("car.png")
            self.image = pygame.transform.scale(self.image, (80, 130))
            self.image = pygame.transform.rotate(self.image, (180))
            self.rect = self.image.get_rect()
            self.rect.centerx, self.rect.centery = pos
            self.cool_down_counter = 0
            self.lasers = []



        def update(self):
            #set varibale for keys 
            keys = pygame.key.get_pressed()

            #input
            if keys[pygame.K_w] and car.rect.y > 0:
                car.rect.y -= vel_car
            if keys[pygame.K_s] and car.rect.y < 540:
                car.rect.y += vel_car
            if keys[pygame.K_d] and car.rect.x < 400:
                car.rect.x += vel_car
            if keys[pygame.K_a] and car.rect.x > 0:
                car.rect.x -= vel_car
            if keys[pygame.K_SPACE]:
                self.shoot(screen)
                
            #if keys[pygame.K_SPACE]:
                #laser.rect.y -= vel_laser
                #group_laser.update()
                #group_laser.draw(screen)
                #car.shoot()



            """ if laser.rect.y < 0:
                    laser.rect.x = car.rect.x-43
                    laser.rect.y = car.rect.y
                
            for event in pygame.event.get():
                if event.type == pygame.KEYUP:
                    if event.key == pygame.K_SPACE:
                        laser.rect.x = car.rect.x-43
                        laser.rect.y = car.rect.y
                if event.type == pygame.QUIT:
                    quit() """

        def draw(self, screen):
            for laser in self.lasers:
                laser.draw(screen)

        def move_laser(self, vel_laser):
            self.cooldown()
            for laser in self.lasers:
                laser.move(vel_laser)

                if laser.off_screen(screen_y):
                    self.lasers.remove(laser)

                        
        def shoot(self, screen):

            print(self.cool_down_counter)

            if self.cool_down_counter >= 0:
                laser = Shoot(car.rect.x , car.rect.y)
                self.lasers.append(laser)
                self.cool_down_counter = 1

                group_laser = pygame.sprite.RenderPlain()
                group_laser.add(laser)
                group_laser.update()
                group_laser.draw(screen)
                #self.move_laser(vel_laser)



        def cooldown(self):
            if self.cool_down_counter >= self.COOLDOWN:
                self.cool_down_counter = 0

            if self.cool_down_counter > 0:
                self.cool_down_counter +=1

                
        def killcar(self):
            self.kill()

        def get_width(self):
            self.image.get_width()
 

    class Enemy(pygame.sprite.Sprite):
        def __init__(self, pos):
            super(Enemy, self).__init__()
            self.image = pygame.image.load("enemy.png")
            self.image = pygame.transform.scale(self.image, (100, 150))
            self.rect = self.image.get_rect()
            self.rect.x, self.rect.y = pos
            #self.hitbox = pygame.Rect(1100, 236, 50, 70)

        def update(self):
            self.rect.y += vel_enemy

        def die(self):
            self.kill()

        def get_width(self):
            self.image.get_width()

    #variable for car
    car = Car((car_x, car_y))
    group = pygame.sprite.RenderPlain()
    group.add(car)

    #sprite group for enemy 
    group_enemies = pygame.sprite.RenderPlain()

    #laser = shoot((car.rect.x-43, car.rect.y))
    #group_laser = pygame.sprite.RenderPlain()
    #group_laser.add(laser)

    #run game
    run = True
    while run == True:
        screen.fill(BLACK)

        


        #scrolling bg 
        for i in range(0, tiles):
            screen.blit(bg, ( 0, -i * bg_height - scroll))
        scroll -= 6
        
        #reset scrool
        if abs(scroll) > bg_height:
            scroll = 0

        #draw car
        group.update()
        group.draw(screen)
        #draw hitbox
        #pygame.draw.rect(screen, (255, 0, 0), car.rect, 1)


        
        
        if len(group_enemies) < 2:

            add_enemy = True
            for enemy in group_enemies:
                if enemy.rect.top < enemy.rect.height * 1.5:
                    add_enemy = False


        if add_enemy:
            if len(enemies) == 0:
                wave_lenght += 1
                points += 10

                if points == 30:
                    vel_enemy += 1
                    scroll += 2
                    
                for i in range(wave_lenght):
                    while True:
                        x, y = random.randint(0, 350), random.randint(-2000, -100)
                        new_rect = pygame.Rect(x, y, 100, 150)
                        if not any(enemy for enemy in enemies if new_rect.colliderect(enemy.rect.x, enemy.rect.y, 100, 150)):
                            break

                    enemy = Enemy((x, y))
                    group_enemies.add(enemy)
                    enemies.append(enemy)




            for enemy in enemies[:]:  #create a copy of the enemies list [:]

                if car.rect.colliderect(enemy.rect):  #collision with car
                    enemies.remove(enemy)
                    enemy.image.fill(TRANSPARENT)
                    lives -=1

                #off screen
                if enemy.rect.y > screen_y:
                    enemies.remove(enemy)
                    enemy.image.fill(TRANSPARENT)
                

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                quit()
        
        group_enemies.update()
        group_enemies.draw(screen)

        lives_label = main_font.render(f'Lives:{lives}', 1, WHITE)
        score_label = main_font.render(f'Score:{points}', 1, WHITE)

        screen.blit(lives_label, (19, 0))
        screen.blit(score_label, (screen_x-score_label.get_width()-19, 0))

        if lives <= 0:
                car.killcar()
                group.remove(car)

                for i in range(0, tiles):
                    screen.blit(bg, ( 0, -i * bg_height - scroll))
                scroll -= 1
                #reset scrool
                if abs(scroll) > bg_height:
                    scroll = 0

                #group_enemies.update()
                #group_enemies.draw(screen)

                #blit game over
                lost = main_font.render("GAME OVER", 1, WHITE)
                screen.blit(lost, (screen_x//2-lost.get_width()//2, screen_y//2))

                #blit play again
                play_again = main_font.render("Press to play again", 1, WHITE)
                screen.blit(play_again, (screen_x//2-play_again.get_width()//2, screen_y//2 + 50))

                if event.type == pygame.MOUSEBUTTONDOWN:
                    main()
                
        
        pygame.display.update()
        clock.tick(FPS)

def Menu():
    bg  = pygame.image.load("road.png").convert()
    bg = pygame.transform.scale(bg, (screen_x, screen_y))
    bg.set_alpha(128)
    #bg.fill((255, 255, 255, alpha), None, pygame.BLEND_RGBA_MULT)

    screen.blit(bg, (0, 0))
    main_font = pygame.font.SysFont("Helvetica", 35, bold = False, italic = True)
    title_lable = main_font.render("Press mouse botton to begin", 1, WHITE)

    #blit label title
    screen.blit(title_lable, (screen_x//2-title_lable.get_width()//2, screen_y//2))
    

    pygame.display.update()

    run = True

    while run == True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                main()
    pygame.quit()

Menu()