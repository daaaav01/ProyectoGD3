import pygame, sys
from game import Game, TILE_SIZE, WIDTH, HEIGHT
from player import Player

pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
fps = 60
clock = pygame.time.Clock()
font = pygame.font.SysFont('Vera', 22)


class Camera: #clase general de la camara
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.rect = pygame.Rect(0,0,self.width, self.height)
    
    def apply(self, target_rect): #funcion que genera el desplazamiento de camara
        return pygame.Rect(target_rect.x+self.rect.x, target_rect.y+self.rect.y, target_rect.width, target_rect.height)
    
    def update(self, target_rect): #funcion update que a su vez determina las condiciones del comportamiento de la camara
        x = -target_rect.centerx + WIDTH//2
        y = -target_rect.centery + HEIGHT//2
        x = min(x,0) # left
        x = max(WIDTH-self.width,x) # right
        y = min(y,0) # top
        y = max(HEIGHT-self.height, y) # bottom
        self.rect = pygame.Rect(x, y, self.width, self.height)
        pygame.draw.rect(screen, 'red', self.rect, 3)


