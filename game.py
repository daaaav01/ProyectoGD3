import pygame, sys, os
from utils import *
from player import Player



pygame.init()
WIDTH, HEIGHT = 918, 476
FPS = 60
screen = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()
TILE_SIZE = 34

class Block(pygame.sprite.Sprite):
    def __init__(self, pos, width, height, img_path):
        super().__init__()
        self.image = load_image(img_path, (width, height))
        self.rect = self.image.get_rect(topleft = pos)
        self.mask = pygame.mask.from_surface(self.image)

class Spike(pygame.sprite.Sprite):
    def __init__(self, pos, width, height, img_path):
        super().__init__()
        self.image = load_image(img_path, (width, height))
        self.rect = self.image.get_rect(topleft = pos)
        self.mask = pygame.mask.from_surface(self.image)
                    
                    #spike

class Game:
    def __init__(self, map_path):
        from camera import Camera
        self.blocks = pygame.sprite.Group()
        self.player = pygame.sprite.GroupSingle()

        self.spike = pygame.sprite.Group() #spike

        self.map = self.read_file(map_path)
        
        self.map_width = len(self.map[0])*TILE_SIZE
        self.map_height = len(self.map)*TILE_SIZE
        self.camera = Camera(self.map_width, self.map_height)

        self.load_map()

    def read_file(self, path):
        file = ''
        with open(path, 'r') as f:
            file = f.read().splitlines()
        return file
    
    def load_map(self):
        for y, row in enumerate(self.map):
            for x, char in enumerate(row):
                if char == 'B':
                    self.blocks.add(Block((x*TILE_SIZE, y*TILE_SIZE), TILE_SIZE, TILE_SIZE, os.path.join('imgs', 'block.jpg')))
                elif char == 'P':
                    self.player.add(Player((x*TILE_SIZE, y*TILE_SIZE), TILE_SIZE, TILE_SIZE, os.path.join('imgs', 'player.jpg')))
                elif char == 'S':
                    self.spike.add(Spike((x*TILE_SIZE, y*TILE_SIZE), TILE_SIZE, TILE_SIZE, os.path.join('imgs', 'spike.png'))) #spike

    def horizontal_movement(self):
        player = self.player.sprite
        player.pos.x += player.direction.x
        player.rect.x = player.pos.x
        for block in self.blocks:
            if block.rect.colliderect(player.rect):
                pygame.quit()
                sys.exit()
        
        for spike in self.spike:
            if spike.mask.overlap(player.mask, (player.rect.x - spike.rect.x, player.rect.y - spike.rect.y)):
                pygame.quit()
                sys.exit()
  
                
    def vertical_movement(self):
        player = self.player.sprite
        player.apply_gravity()
        for block in self.blocks:
            if block.rect.colliderect(player.rect):
                if player.direction.y < 0:
                    player.rect.top = block.rect.bottom
                    player.pos.y = player.rect.y
                    player.direction.y = 0
                if player.direction.y > 0:
                    player.on_ground = True
                    player.rect.bottom = block.rect.top
                    player.pos.y = player.rect.y
                    player.direction.y = 0
        
        if player.on_ground and player.direction.y < 0 or player.direction.y > 0:
            player.on_ground = False

    def update(self):
        self.horizontal_movement()
        self.vertical_movement()
        self.player.update()
        self.camera.update(self.player.sprite.rect)

    def draw(self, surface):
        for block in self.blocks:
            surface.blit(block.image, self.camera.apply(block.rect))
        surface.blit(self.player.sprite.image, self.camera.apply(self.player.sprite.rect))
        for spike in self.spike:
            surface.blit(spike.image, self.camera.apply(spike.rect))
        surface.blit(self.player.sprite.image, self.camera.apply(self.player.sprite.rect))

def draw_grid(surface):
    for y in range(TILE_SIZE, WIDTH, TILE_SIZE):
        pygame.draw.line(surface, 'red', (y, 0), (y, HEIGHT))

    for x in range(TILE_SIZE, HEIGHT, TILE_SIZE):
        pygame.draw.line(surface, 'blue', (0, x), (WIDTH, x))

if __name__ == '__main__':
    game = Game('map.txt')
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
        screen.fill('lightblue')
        game.update()
        game.draw(screen)
        #draw_grid(screen)
        clock.tick(FPS)
        pygame.display.update()