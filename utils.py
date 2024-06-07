import pygame

def load_image(path, size=None): #funcion para subir imagenes y ajustar el tamaño
    img = pygame.image.load(path)
    if size:
        img = pygame.transform.scale(img, size)
    return img