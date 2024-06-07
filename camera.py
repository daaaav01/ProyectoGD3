import pygame, sys
from game import Game, TILE_SIZE, WIDTH, HEIGHT
from player import Player

pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
fps = 60
clock = pygame.time.Clock()
font = pygame.font.SysFont('Vera', 22)

def draw_topright_text(surface, text, x, y, color):    
    image = font.render(text, True, color)
    rect = image.get_rect(topright = (x,y))
    surface.blit(image, rect)

def draw_topleft_text(surface, text, x, y, color):
    image = font.render(text, True, color)
    rect = image.get_rect(topleft = (x,y))
    surface.blit(image, rect)

class Camera:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.rect = pygame.Rect(0,0,self.width, self.height)
    
    def apply(self, target_rect):
        return pygame.Rect(target_rect.x+self.rect.x, target_rect.y+self.rect.y, target_rect.width, target_rect.height)
    
    def update(self, target_rect):
        x = -target_rect.centerx + WIDTH//2
        y = -target_rect.centery + HEIGHT//2
        x = min(x,0) # left
        x = max(WIDTH-self.width,x) # right
        y = min(y,0) # top
        y = max(HEIGHT-self.height, y) # bottom
        self.rect = pygame.Rect(x, y, self.width, self.height)
        pygame.draw.rect(screen, 'red', self.rect, 3)

class Player(pygame.sprite.Sprite):
    def __init__(self, pos):
        super().__init__()
        self.image = pygame.Surface((TILE_SIZE,TILE_SIZE))
        self.image.fill('red')
        self.rect = self.image.get_rect(topleft = pos)
    
    def update(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_d]:
            self.rect.x += 6
        if keys[pygame.K_a]:
            self.rect.x -= 6
        if keys[pygame.K_w]:
            self.rect.y -= 6
        if keys[pygame.K_s]:
            self.rect.y += 6

class GameCamera(Game):
    def __init__(self):
        super().__init__("camera_map.txt")
        self.map_width = len(self.map[0])*TILE_SIZE
        self.map_height = len(self.map)*TILE_SIZE
        self.camera = Camera(self.map_width, self.map_height)
        self.player.add(Player((316, 186)))
    
    
    def draw(self, surface):
        player_sprite = self.player.sprite
        for block in self.blocks:
            block_rect_from_camera = self.camera.apply(block.rect)
            if not block.rect.x:
                x,y = block_rect_from_camera.topright
                draw_topleft_text(screen, 'apply(rect): ', x, y, 'black')
                draw_topleft_text(screen, 'x: {}, y: {}'.format(block_rect_from_camera.x, block_rect_from_camera.y), x, y+16, 'black')
            else:
                x,y = block_rect_from_camera.topleft
                draw_topright_text(screen, 'apply(rect): ', x, y, 'black')
                draw_topright_text(screen, 'x: {}, y: {}'.format(x, y), x, y+16, 'black')
            surface.blit(block.image, block_rect_from_camera)
        draw_topright_text(screen, 'update(player_rect) x: {}, y: {}'.format(self.camera.rect.x, self.camera.rect.y), 385, 60, 'black')
        player_rect_from_camera = self.camera.apply(player_sprite.rect)
        draw_topright_text(screen, 'apply(rect) x: {}, y: {}'.format(player_rect_from_camera.x, player_rect_from_camera.y), player_rect_from_camera.x, player_rect_from_camera.y, 'black')
        draw_topright_text(screen, 'rect x: {}, y: {}'.format(player_sprite.rect.x, player_sprite.rect.y), player_rect_from_camera.x, player_rect_from_camera.y+20, 'black')
        surface.blit(player_sprite.image, player_rect_from_camera)

    def update(self):
        self.camera.update(self.player.sprite.rect)
        self.player.update()

if __name__ == '__main__':
    game = GameCamera()
    while True:
        screen.fill('lightblue')
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
        game.update()
        game.draw(screen)
        pygame.draw.line(screen, 'green', (WIDTH//2, 0), (WIDTH//2, HEIGHT), 2)
        pygame.draw.line(screen, 'blue', (0, HEIGHT//2), (WIDTH, HEIGHT//2), 2)
        clock.tick(fps)
        pygame.display.update()

    def draw(self, surface):
        player_sprite = self.player.sprite
        for block in self.blocks:
            block_rect_from_camera = self.camera.apply(block.rect)
            if not block.rect.x:
                x,y = block_rect_from_camera.topright
                draw_topleft_text(screen, 'apply(rect): ', x, y, 'black')
                draw_topleft_text(screen, 'x: {}, y: {}'.format(block_rect_from_camera.x, block_rect_from_camera.y), x, y+16, 'black')
            else:
                x,y = block_rect_from_camera.topleft
                draw_topright_text(screen, 'apply(rect): ', x, y, 'black')
                draw_topright_text(screen, 'x: {}, y: {}'.format(x, y), x, y+16, 'black')
            surface.blit(block.image, block_rect_from_camera)
        draw_topright_text(screen, 'update(player_rect) x: {}, y: {}'.format(self.camera.rect.x, self.camera.rect.y), 385, 60, 'black')
        player_rect_from_camera = self.camera.apply(player_sprite.rect)
        draw_topright_text(screen, 'apply(rect) x: {}, y: {}'.format(player_rect_from_camera.x, player_rect_from_camera.y), player_rect_from_camera.x, player_rect_from_camera.y, 'black')
        draw_topright_text(screen, 'rect x: {}, y: {}'.format(player_sprite.rect.x, player_sprite.rect.y), player_rect_from_camera.x, player_rect_from_camera.y+20, 'black')
        surface.blit(player_sprite.image, player_rect_from_camera)

    def update(self):
        self.camera.update(self.player.sprite.rect)
        self.player.update()

if __name__ == '__main__':
    game = GameCamera()
    while True:
        screen.fill('lightblue')
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
        game.update()
        game.draw(screen)
        pygame.draw.line(screen, 'green', (WIDTH//2, 0), (WIDTH//2, HEIGHT), 2)
        pygame.draw.line(screen, 'blue', (0, HEIGHT//2), (WIDTH, HEIGHT//2), 2)
        clock.tick(fps)
        pygame.display.update()
