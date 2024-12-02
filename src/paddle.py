import pygame

class Paddle:
    def __init__(self, x, y):
        self.rect = pygame.Rect(x, y, 20, 100)
        self.speed = 5
    
    def move(self, up_key, down_key):
        keys = pygame.key.get_pressed()  # Vérifie les touches appuyées
        if keys[up_key] and self.rect.top > 0:  # Déplacer vers le haut
            self.rect.y -= self.speed
        if keys[down_key] and self.rect.bottom < 600:  # Déplacer vers le bas
            self.rect.y += self.speed

    def draw(self, screen):
        pygame.draw.rect(screen, (255, 255, 255), self.rect)
