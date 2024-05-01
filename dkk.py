import pygame
from pygame.locals import *
from pygame import mixer


pygame.mixer.pre_init(44100, -16, 2, 512)
mixer.init()
pygame.init()

clock = pygame.time.Clock()
fps = 60

screen_width = 700
screen_height = 700

screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption('Zoro"s escape')



#define game variables
tile_size = 35
game_over = 0
main_menu = True
level = 1
max_levels = 3




#load images
moon_img = pygame.image.load('images/moon.png')
moon_img = pygame.transform.scale(moon_img, (100, 100))  

sky_img = pygame.image.load('images/sky.png')
sky_img = pygame.transform.scale(sky_img, (700, 700))  

restart_img = pygame.image.load('images/restart_btn.png')
restart_img = pygame. transform.scale(restart_img, (100, 40))

start_img = pygame.image.load('images/start_btn.png')

exit_img = pygame.image.load('images/exit_btn.png')

con_img = pygame.image.load('images/congrats.png')



level_fx = pygame.mixer.Sound('sounds/levelend.wav')
level_fx.set_volume(0.5)
death_fx = pygame.mixer.Sound('sounds/death.wav')
death_fx.set_volume(0.5)
end_fx = pygame.mixer.Sound('sounds/endsou.wav')
end_fx.set_volume(0.2)
jump_fx = pygame.mixer.Sound('sounds/jump.wav')
end_fx.set_volume(0.5)

def reset_level(level):
     player.reset(35, screen_height - 105)
     slime_group.empty()
     spike_group.empty()
     exit_group.empty()
     world = World(world_data)
     

     return world


class Button():
     def __init__(self, x, y, image):
          self.image = image
          self.rect = self.image. get_rect()
          self.rect.x = x 
          self.rect.y = y
          self.clicked = False

     def draw(self):
          action = False
          #mouse position     
          pos = pygame.mouse.get_pos()
          if self.rect.collidepoint(pos):
               if pygame.mouse.get_pressed()[0] == 1 and self.clicked == False:
                    action = True
                    self.clicked = True
          
          if pygame.mouse.get_pressed()[0] == 0:
               self.clicked = False
                    


          screen.blit(self.image, self.rect)

          return action
          

class Player():
     def __init__(self, x, y):
        self.reset(x, y)


     def update(self,game_over):
        dx = 0 
        dy = 0
        walk_cooldown = 5
        default_image_path = 'images/guy1.png'
        default_image_path2 = 'images/guy0.png'

        if game_over == 0:
          #keys
          key = pygame.key.get_pressed()  
          if  key[pygame.K_SPACE] and self.jumped == False and self.in_air == False:
               jump_fx.play()
               self.vel_y = -13
               self.jumped = True
          if key[pygame.K_SPACE] == False:
               self.jumped = False
          if key[pygame.K_LEFT]:
               dx -= 5
               self.counter += 1
               self.direction = -1
          if key[pygame.K_RIGHT]:
               dx += 5
               self.counter += 1
               self.direction = 1
          if key[pygame.K_LEFT] == False and key[pygame.K_RIGHT] == False:
               self.counter = 0 
               self.index = 0
               self.image = pygame.image.load(default_image_path)
               self.image = pygame.transform.scale(self.image, (30, 60))
               if self.counter > walk_cooldown:
                    self.counter = 0
                    self.index += 1
               if self.index >= len(self.images_right):
                    self.index = 0
               if self.direction == 1:
                    self.image = pygame.image.load(default_image_path)
                    self.image = pygame.transform.scale(self.image, (30, 60))
               if self.direction == -1:
                    self.image = pygame.image.load(default_image_path2)
                    self.image = pygame.transform.scale(self.image, (30, 60))

               
          
          #animation
          if self.counter > walk_cooldown:
               self.counter = 0
               self.index += 1
               if self.index >= len(self.images_right):
                    self.index = 0
               if self.direction == 1:
                    self.image = self.images_right[self.index]
               if self.direction == -1:
                    self.image = self.images_left[self.index]
          #gravity
          self.vel_y += 1
          if self.vel_y > 10:
               self.vel_y = 10

          dy += self.vel_y

          #collision
          self.in_air = True
          for tile in world.tile_list:
               if tile[1].colliderect(self.rect.x + dx, self.rect.y, self.width, self.height):
                    dx = 0
                            
               if tile[1].colliderect(self.rect.x, self.rect.y + dy, self.width, self.height):

                    if self.vel_y < 0:
                         dy = tile[1].bottom - self.rect.top
                         self.vel_y = 0

                    elif self.vel_y >= 0:
                         dy = tile[1].top - self.rect.bottom
                         self.vel_y = 0
                         self.in_air = False

          #collision with enemies
          if pygame.sprite.spritecollide(self, slime_group, False):
               death_fx.play()
               game_over = -1
          if pygame.sprite.spritecollide(self, spike_group, False):
               death_fx.play()
               game_over = -1 
          if pygame.sprite.spritecollide(self, spike2_group, False):
               death_fx.play()
               game_over = -1
          if pygame.sprite.spritecollide(self, spike3_group, False):
               death_fx.play()
               game_over = -1
          if pygame.sprite.spritecollide(self, exit_group, False):
               level_fx.play()
               game_over = 1         


          self.rect.x += dx
          self.rect.y += dy

         
        elif game_over == -1:
             self.image = self.dead_image 
             if self.rect.y > 200:
               self.rect.y -= 5
             
             
              


        screen.blit(self.image, self.rect)
        

        return game_over
     

     def reset(self, x, y):
          self.images_right = []
          self.images_left = []
          self.index = 0
          self.counter = 0 
          self.last_pressed = None
        
        
          for num in range (2, 8):
               img_right = pygame.image.load(f'images/guy{num}.png')
               img_right = pygame.transform.scale(img_right, (30, 60))
               img_left = pygame.transform.flip(img_right, True, False)
               self.images_right.append(img_right)
               self.images_left.append(img_left)
          self.dead_image = pygame.image.load('images/dead.png')    
          self.image = self.images_right[self.index]   
          self.rect = self.image.get_rect()
          self.rect.x = x
          self.rect.y = y
          self.width = self.image.get_width()
          self.height = self.image.get_height()
          self.vel_y = 0
          self.jumped = False
          self.direction = 0
          self.in_air = True

class World():
     def __init__(self,data):
          self.tile_list = []
          #load images
          plat_img = pygame.image.load('images/plat3.png')
          
          plat1_img = pygame.image.load('images/plat3_0.png')
            
          row_count = 0  
          for row in data:
                col_count = 0 
                for tile in row:
                    if tile == 1:
                         img = pygame.transform.scale(plat_img, (tile_size, tile_size))
                         img_rect = img.get_rect()
                         img_rect.x = col_count * tile_size
                         img_rect.y = row_count * tile_size
                         tile = (img, img_rect)
                         self.tile_list.append(tile)
                    if tile == 2:
                         spike = Spike(col_count * tile_size, row_count * tile_size)
                         spike_group.add(spike)                        
                    if tile == 3:
                         img = pygame.transform.scale(plat1_img, (tile_size, tile_size))
                         img_rect = img.get_rect()
                         img_rect.x = col_count * tile_size
                         img_rect.y = row_count * tile_size
                         tile = (img, img_rect)
                         self.tile_list.append(tile)
                    if tile == 4:
                        slime = Enemy(col_count * tile_size, row_count * tile_size)
                        slime_group.add(slime)
                    if tile == 5:
                         spike = Spike2(col_count * tile_size, row_count * tile_size)
                         spike_group.add(spike) 
                    if tile == 6:
                         spike = Spike3(col_count * tile_size, row_count * tile_size)
                         spike_group.add(spike)
                    if tile == 7:
                        exit = Exit(col_count * tile_size, row_count * tile_size - (tile_size // 2)) 
                        exit_group.add(exit)
                    col_count += 1
                row_count += 1


     def draw(self):
          for tile in self.tile_list:
               screen.blit(tile[0], tile[1])
               



class Enemy(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load('images/slime.png')
        self.rect = self.image.get_rect()
        self.rect.x = x 
        self.rect.y = y
        self.move_direction = 1
        self.move_counter = 0 

    def update(self):
        self.rect.x += self.move_direction
        self.move_counter += 1
        if abs(self.move_counter) > 40:
            self.move_direction *= -1
            self.move_counter *= -1

class Spike(pygame.sprite.Sprite):
     def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        img = pygame.image.load('images/spikes1.png')
        self.image = pygame.transform.scale(img, (tile_size, tile_size))
        self.rect = self.image.get_rect()
        self.rect.x = x 
        self.rect.y = y
class Spike2(pygame.sprite.Sprite):
     def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        img = pygame.image.load('images/spikes2.png')
        self.image = pygame.transform.scale(img, (tile_size, tile_size))
        self.rect = self.image.get_rect()
        self.rect.x = x 
        self.rect.y = y
class Spike3(pygame.sprite.Sprite):
     def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        img = pygame.image.load('images/spikes3.png')
        self.image = pygame.transform.scale(img, (tile_size, tile_size))
        self.rect = self.image.get_rect()
        self.rect.x = x 
        self.rect.y = y
           
class Exit(pygame.sprite.Sprite):
     def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        img = pygame.image.load('images/exit.png')
        self.image = pygame.transform.scale(img, (tile_size, int(tile_size *1.5)))
        self.rect = self.image.get_rect()
        self.rect.x = x 
        self.rect.y = y



if level == 1:
     world_data = [
     [3, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 3], 
     [3, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 3], 
     [3, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 3], 
     [3, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 3], 
     [3, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 3], 
     [3, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 3], 
     [3, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 3], 
     [3, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 3], 
     [3, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 3], 
     [3, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 3], 
     [3, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 3], 
     [3, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 3], 
     [3, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 3], 
     [3, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 3], 
     [3, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 3], 
     [3, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 3], 
     [3, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 7, 3], 
     [3, 0, 0, 0, 4, 0, 1, 0, 0, 5, 1, 6, 0, 5, 1, 6, 0, 1, 1, 3], 
     [3, 0, 1, 1, 1, 1, 3, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 3, 3, 3], 
     [3, 1, 3, 3, 3, 3, 3, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 3, 3, 3]
     ]


player = Player(35, screen_height - 105)

slime_group = pygame.sprite.Group()
spike_group = pygame.sprite.Group()
spike2_group = pygame.sprite.Group()
spike3_group = pygame.sprite.Group()
exit_group = pygame.sprite.Group()


world = World(world_data)

restart_button = Button(screen_width // 2 -35, screen_height // 2 + 70, restart_img)

start_button = Button(screen_width // 2 - 290, screen_height // 2 - 100, start_img)
exit_button = Button(screen_width // 2 + 50, screen_height // 2 - 100, exit_img)




run = True 
while run == True: 

    clock.tick(fps)
    
    screen.blit(sky_img, (0, 0))
    screen.blit(moon_img, (50, 50))
    
    

    if main_menu == True:
          if exit_button.draw():
               run = False
          if start_button.draw():
               main_menu = False
    else:

          world.draw()

          if game_over == 0:
               slime_group.update()

          slime_group.draw(screen)
          spike_group.draw(screen)
          exit_group.draw(screen)

          game_over = player.update(game_over)

          if game_over == -1:
               if restart_button.draw():
                    player.reset(35, screen_height - 105)
                    game_over = 0

          if game_over == 1:
               level += 1
               if level <= max_levels:
                    world_data = []
                    if level == 1:
                         world_data = [
                         [3, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 3], 
                         [3, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 3], 
                         [3, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 3], 
                         [3, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 3], 
                         [3, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 3], 
                         [3, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 3], 
                         [3, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 3], 
                         [3, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 3], 
                         [3, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 3], 
                         [3, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 3], 
                         [3, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 3], 
                         [3, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 3], 
                         [3, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 3], 
                         [3, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 3], 
                         [3, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 3], 
                         [3, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 3], 
                         [3, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 7, 3], 
                         [3, 0, 0, 0, 4, 0, 1, 0, 0, 5, 1, 6, 0, 5, 1, 6, 0, 1, 1, 3], 
                         [3, 0, 1, 1, 1, 1, 3, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 3, 3, 3], 
                         [3, 1, 3, 3, 3, 3, 3, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 3, 3, 3]
                         ]

                    if level == 2:
                         world_data = [
                         [3, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 5], 
                         [3, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 5], 
                         [3, 0, 0, 0, 0, 0, 0, 0, 4, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 5], 
                         [3, 0, 0, 0, 1, 2, 1, 1, 1, 1, 2, 1, 1, 1, 1, 6, 0, 0, 0, 5], 
                         [3, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 3, 6, 0, 0, 0, 5], 
                         [3, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 3, 6, 0, 0, 0, 5], 
                         [3, 3, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 3, 6, 0, 0, 0, 5], 
                         [3, 3, 3, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 3, 6, 0, 0, 0, 5], 
                         [3, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 3, 6, 0, 0, 0, 5], 
                         [3, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 3, 1, 6, 0, 5, 1], 
                         [3, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 4, 0, 3, 6, 0, 0, 0, 5], 
                         [3, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 3, 6, 0, 0, 0, 5], 
                         [3, 0, 0, 0, 0, 1, 2, 1, 0, 0, 0, 0, 0, 0, 3, 6, 0, 0, 0, 5], 
                         [3, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 3, 6, 0, 0, 0, 5], 
                         [3, 2, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 3, 6, 0, 0, 0, 5], 
                         [3, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 3, 1, 2, 0, 2, 1], 
                         [3, 0, 0, 0, 0, 1, 1, 0, 0, 0, 0, 0, 0, 0, 3, 3, 1, 7, 1, 3], 
                         [3, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 3, 3, 3, 3, 3, 3], 
                         [3, 0, 0, 1, 1, 0, 0, 2, 2, 2, 2, 2, 2, 2, 3, 3, 3, 3, 3, 3], 
                         [3, 1, 1, 3, 3, 1, 1, 1, 1, 1, 1, 1, 1, 1, 3, 3, 3, 3, 3, 3]
                         ]
                    if level == 3:
                         world_data = [
                         [3, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 3], 
                         [3, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 3], 
                         [3, 7, 0, 0, 0, 0, 0, 4, 0, 0, 4, 0, 0, 0, 0, 0, 0, 0, 0, 3], 
                         [3, 1, 1, 2, 2, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 3], 
                         [3, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 5, 3], 
                         [3, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 5, 3], 
                         [3, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 5, 3], 
                         [3, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 3, 1, 3], 
                         [3, 0, 0, 0, 1, 1, 2, 2, 1, 2, 2, 1, 2, 2, 1, 0, 0, 0, 0, 3], 
                         [3, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 3], 
                         [3, 6, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 3], 
                         [3, 6, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 3], 
                         [3, 6, 0, 0, 4, 0, 0, 4, 0, 0, 4, 0, 0, 0, 0, 0, 0, 0, 0, 3], 
                         [3, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 3], 
                         [3, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 4, 0, 3], 
                         [3, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 3], 
                         [3, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 3], 
                         [3, 0, 0, 1, 1, 1, 0, 0, 1, 0, 0, 1, 0, 0, 1, 0, 0, 0, 0, 3], 
                         [3, 0, 0, 3, 3, 3, 2, 2, 3, 2, 2, 3, 2, 2, 3, 2, 2, 2, 2, 3], 
                         [3, 1, 1, 3, 3, 3, 1, 1, 3, 1, 1, 3, 1, 1, 3, 1, 1, 1, 1, 3]
                         ]
                   
                         
                    world = reset_level(level)
                    game_over = 0
               else:
                    img = pygame.image.load('images/congrats.png')
                    screen.blit(img, (-10, 150))
                    end_fx.play()
                   

                    if restart_button.draw():
                         main_menu = True
                         level = 0
                         game_over = 0
                         
                         

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False 

    pygame.display.update()
pygame.quit()