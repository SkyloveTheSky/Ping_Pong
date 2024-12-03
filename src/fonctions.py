import pygame

class Fonctions:
    
    @staticmethod
    def check_win(ball, score_left, score_right, reset_ball):
        # Si la balle sort du côté gauche, le joueur de droite marque
        if ball.rect.left <= 0:
            score_right += 1
            pygame.mixer.Sound("assets/sounds/ball_maty.mp3").play()
            reset_ball()
        # Si la balle sort du côté droit, le joueur de gauche marque
        elif ball.rect.right >= 1200:
            score_left += 1
            pygame.mixer.Sound("assets/sounds/ball_maty.mp3").play()
            reset_ball()
        return score_left, score_right

    @staticmethod
    def show_winner(screen, font, message):
        # Afficher un message de victoire
        screen.fill((0, 0, 0))  # Fond noir
        text = font.render(message, True, (255, 255, 255))  # Texte blanc
        text_rect = text.get_rect(center=(600, 300))  # Centrer le texte
        screen.blit(text, text_rect)
        pygame.display.flip()
        pygame.time.delay(3000)

    @staticmethod
    def reset_ball(ball):
        ball.rect.x = 600
        ball.rect.y = 300
        ball.vx = -ball.vx

    @staticmethod
    def draw_scores(screen, font, score_left, score_right):
        # Texte pour le joueur de gauche
        score_left_text = font.render(str(score_left), True, (255, 255, 255))
        screen.blit(score_left_text, (500, 20))  # Position (x: 500, y: 20)

        # Texte pour le joueur de droite
        score_right_text = font.render(str(score_right), True, (255, 255, 255))
        screen.blit(score_right_text, (650, 20))  # Position (x: 650, y: 20)

    @staticmethod
    def draw_court(screen):
        # Couleur de la ligne (blanc)
        line_color = (255, 255, 255)
        # Position et épaisseur de la ligne
        line_start = (600, 0)  # Point de départ (milieu haut)
        line_end = (600, 600)  # Point de fin (milieu bas)
        line_width = 4
        # Dessiner la ligne
        pygame.draw.line(screen, line_color, line_start, line_end, line_width)

    
    @staticmethod
    def show_pause_message(screen, font):
        # Afficher un message de pause au centre de l'écran
        pause_text = font.render("PAUSE", True, (255, 255, 255))
        pause_rect = pause_text.get_rect(center=(600, 300))
        screen.blit(pause_text, pause_rect)
        pygame.display.flip()