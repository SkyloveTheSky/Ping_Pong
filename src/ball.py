import pygame

class Ball:
    def __init__(self, x, y):
        self.rect = pygame.Rect(x, y, 15, 15)
        self.vx = 5
        self.vy = 5

    def move(self):
        self.rect.x += self.vx
        self.rect.y += self.vy
        if self.rect.top <= 0 or self.rect.bottom >= 600:  # Hauteur de l'écran
            self.vy = -self.vy

    def draw(self, screen):
        pygame.draw.ellipse(screen, (255, 255, 255), self.rect)
