# Création de la classe mère pour les ennemis
import pygame

class Ennemi(pygame.sprite.Sprite):
    def __init__(self, x, y, image_path=None):
        super().__init__()
        
        #quand l'image d'un ennemi sera prete:
        #self.image = pygame.image.load(image_path).convert_alpha()

    #en attendant un carre rouge
        self.image = pygame.Surface((32, 32))
        self.image.fill((255, 0, 0)) # RGB du rouge
            
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.vitesse = 1
        self.direction = -1

    def update(self):
        # Logique de mouvement de base
        self.rect.x += self.vitesse * self.direction

    def inverser_direction(self):
        self.direction *= -1