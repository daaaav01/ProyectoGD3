import pygame, sys, os
from utils import *
from player import Player



pygame.init()
WIDTH, HEIGHT = 918, 476
FPS = 60
screen = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()
TILE_SIZE = 34

lvl1 = 'imgs/fondo_lvl1.png'
lvl2 = 'imgs/lvl2.jpg'

# Estados del juego
MENU = "menu"
GAME = "game"

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
    def __init__(self, map_path, nivel):
        from camera import Camera
        self.blocks = pygame.sprite.Group()
        self.player = pygame.sprite.GroupSingle()
        self.background_image = load_image(nivel)
        self.backround_rect = self.background_image.get_rect()
        self.game_over = False

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
                self.game_over = True
        
        for spike in self.spike:
            if spike.mask.overlap(player.mask, (player.rect.x - spike.rect.x, player.rect.y - spike.rect.y)):
                self.game_over = True
  
                
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
        

def show_game_over(surface):
        font = pygame.font.Font(None, 100)
        game_over_text = font.render("Game Over", True, (255, 0, 0))
        text_rect = game_over_text.get_rect(center=(WIDTH // 2, HEIGHT // 2))
        surface.blit(game_over_text, text_rect)
        pygame.display.flip() 

class Menu:
    def __init__(self, surface):
        self.surface = surface
        self.background_image = load_image("imgs/inicio_juego.jpg")
        self.backround_rect = self.background_image.get_rect()
        self.state = MENU
        
    def show_start_screen(self): #pantalla de inicio
        self.image_button = load_image("imgs/start.png", (100, 50))
        self.button_rect = self.image_button.get_rect(center=(WIDTH // 2, (HEIGHT // 1.3)))
        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONDOWN:
                self.mouse_pos = pygame.mouse.get_pos()
                self.mouse_rect = pygame.Rect(self.mouse_pos, (1, 1))  # Crear un rectángulo pequeño en la posición del ratón
                if self.button_rect.contains(self.mouse_rect):
                    self.state = GAME
        self.surface.blit(self.image_button, self.button_rect)

def draw_grid(surface):
    for y in range(TILE_SIZE, WIDTH, TILE_SIZE):
        pygame.draw.line(surface, 'red', (y, 0), (y, HEIGHT))

    for x in range(TILE_SIZE, HEIGHT, TILE_SIZE):
        pygame.draw.line(surface, 'blue', (0, x), (WIDTH, x))

if __name__ == '__main__':
    game = Game('map.txt', lvl2)
    menu= Menu(screen)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        if menu.state == MENU:
            screen.blit(menu.background_image, menu.backround_rect)
            menu.show_start_screen()
        if menu.state == GAME:
            if not game.game_over:
                screen.blit(game.background_image, game.backround_rect)
                game.update()
                game.draw(screen)
                #draw_grid(screen)
            else:
                show_game_over(screen)
                
        
        clock.tick(FPS)
        pygame.display.update()