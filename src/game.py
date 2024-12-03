import pygame
from fonctions import Fonctions


from paddle import Paddle
from ball import Ball

class Game:
    # Initialiseur
    def __init__(self):
        pygame.init()
        pygame.mixer.init()
        self.screen = pygame.display.set_mode((1200, 600))
        pygame.display.set_caption("Ping Pong")
        self.clock = pygame.time.Clock()
        self.hit_sound = pygame.mixer.Sound("assets/sounds/ball_hit.mp3")
        self.superpower_sound = pygame.mixer.Sound("assets/sounds/in_fire.mp3")
        self.hit_sound.set_volume(0.5)
        self.superpower_sound.set_volume(0.5)
        self.running = True
        self.paused = False 
        self.paddle1 = Paddle(20, 250)
        self.paddle2 = Paddle(1160, 250)
        self.ball = Ball(600, 300)
        self.font = pygame.font.Font(None, 74)
        self.score_left = 0
        self.score_right = 0
        self.paddle1_hits = 0
        self.paddle2_hits = 0
        self.superpower_active = False
        self.superpower_start_time = None

    def run(self):
        choice = self.show_welcome_screen()

        if choice == 0:  # Jouer avec AI
            print("Starting game with AI...")
            self.play_with_ai()
        elif choice == 1:  # Jouer en local
            print("Starting local game...")
            self.play_local()
        elif choice == 2:  # Jouer en multijoueur
            print("Starting multiplayer game...")
            self.play_multiplayer()

    """************************************Propriétés de la page menu**********************************************"""
    def show_welcome_screen(self):
        self.screen.fill((0, 0, 0))
        font = pygame.font.Font(None, 74)
        option_font = pygame.font.Font(None, 50)

        # Texte de bienvenue
        title_text = font.render("Welcome to Pong!", True, (255, 255, 255))
        title_rect = title_text.get_rect(center=(600, 100))
        self.screen.blit(title_text, title_rect)

        # Options du menu
        options = ["Play with AI", "Play Locally", "Play Multiplayer"]
        selected_option = 0

        # Boucle pour le menu
        waiting = True
        while waiting:
            self.screen.fill((0, 0, 0))  # Réinitialiser l'écran
            self.screen.blit(title_text, title_rect)

            # Affichage des options
            for i, option in enumerate(options):
                color = (255, 255, 255) if i == selected_option else (150, 150, 150)
                option_text = option_font.render(option, True, color)
                option_rect = option_text.get_rect(center=(600, 200 + i * 100))
                self.screen.blit(option_text, option_rect)

            pygame.display.flip()  # Actualiser l'écran

            # Gestion des événements
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                    waiting = False
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_UP:  # Naviguer vers le haut
                        selected_option = (selected_option - 1) % len(options)
                    elif event.key == pygame.K_DOWN:  # Naviguer vers le bas
                        selected_option = (selected_option + 1) % len(options)
                    elif event.key == pygame.K_RETURN:  # Sélectionner une option
                        waiting = False

        return selected_option
    
    """**************************************Jouer avec AI********************************************"""
    def play_with_ai(self):
        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:  # Si touche Echap pressée
                        self.paused = not self.paused  # Alterne l'état de la pause

            if not self.paused:  # Si le jeu n'est pas en pause
                self.paddle1.move(pygame.K_z, pygame.K_s)  # Contrôle avec Z et S

                # Contrôle de l'IA pour paddle2
                if self.ball.rect.centery > self.paddle2.rect.centery:
                    self.paddle2.rect.y += 5
                elif self.ball.rect.centery < self.paddle2.rect.centery:
                    self.paddle2.rect.y -= 5

                self.ball.move()
            
                # Mise à jour des scores
                self.score_left, self.score_right = Fonctions.check_win(
                    self.ball, self.score_left, self.score_right, lambda: Fonctions.reset_ball(self.ball)
                )

                # Vérification de la collision avec les paddles
                if self.ball.rect.colliderect(self.paddle1.rect) or self.ball.rect.colliderect(self.paddle2.rect):
                    self.ball.vx = -self.ball.vx  # Inverser la direction de la balle
                    self.hit_sound.play()  # Jouer le son


                # Mise à jour de l'affichage
                self.screen.fill((0, 0, 0))
                Fonctions.draw_court(self.screen)
                self.paddle1.draw(self.screen)
                self.paddle2.draw(self.screen)
                self.ball.draw(self.screen)
                Fonctions.draw_scores(self.screen, self.font, self.score_left, self.score_right)
                pygame.display.flip()
                self.clock.tick(60)
            else:
                Fonctions.show_pause_message(self.screen, self.font)  # Afficher le message de pause


    """**************************************Jouer local********************************************"""
    def play_local(self):
        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:  # Si touche Echap pressée
                        self.paused = not self.paused  # Alterne l'état de la pause

            if not self.paused:  # Si le jeu n'est pas en pause
                self.paddle1.move(pygame.K_z, pygame.K_s)  # Contrôle du joueur 1
                self.paddle2.move(pygame.K_UP, pygame.K_DOWN)  # Contrôle du joueur 2

                # Mouvements de la balle
                self.ball.move()

                # Vérification de la collision entre la balle et les paddles
                if self.ball.rect.colliderect(self.paddle1.rect):
                    self.ball.vx = -self.ball.vx
                    self.hit_sound.play()
                    self.paddle1_hits += 1
                    self.paddle2_hits = 0

                elif self.ball.rect.colliderect(self.paddle2.rect):
                    self.ball.vx = -self.ball.vx
                    self.hit_sound.play()
                    self.paddle2_hits += 1
                    self.paddle1_hits = 0 

                # Activer le superpouvoir
                if self.paddle1_hits == 2 or self.paddle2_hits == 2:
                    self.superpower_active = True
                    self.superpower_start_time = pygame.time.get_ticks()  # Temps en millisecondes
                    self.ball.vx *= 2  # Double la vitesse horizontale
                    self.ball.vy *= 2  # Double la vitesse verticale
                    self.paddle1_hits = 0
                    self.paddle2_hits = 0
                    self.superpower_sound.play()

                # Désactiver le superpouvoir après 10 secondes
                if self.superpower_active:
                    superpower_text = self.font.render("Superpower Active!", True, (255, 0, 0))
                    self.screen.blit(superpower_text, (400, 50))
                    current_time = pygame.time.get_ticks()
                    if current_time - self.superpower_start_time > 10000:  # 10 000 ms = 10 secondes
                        self.superpower_active = False
                        self.ball.vx /= 2  # Réduit la vitesse
                        self.ball.vy /= 2

                
                    


                # Vérification des scores
                self.score_left, self.score_right = Fonctions.check_win(
                    self.ball, self.score_left, self.score_right, lambda: Fonctions.reset_ball(self.ball)
                )

                # Mise à jour de l'affichage
                self.screen.fill((0, 0, 0))  # Efface l'écran
                Fonctions.draw_court(self.screen)  # Dessine le terrain
                self.paddle1.draw(self.screen)
                self.paddle2.draw(self.screen)
                self.ball.draw(self.screen)
                Fonctions.draw_scores(self.screen, self.font, self.score_left, self.score_right)  # Affiche les scores
                pygame.display.flip()  # Actualise l'écran
                self.clock.tick(60)  # Limite à 60 FPS
            else:
                Fonctions.show_pause_message(self.screen, self.font)  # Afficher le message de pause


    def check_win(self):
        self.score_left, self.score_right = Fonctions.check_win(
        self.ball, self.score_left, self.score_right, lambda: Fonctions.reset_ball(self.ball)
    )

    def show_winner(self, message):
        Fonctions.show_winner(self.screen, self.font, message)

    def reset_ball(self):
        Fonctions.reset_ball(self.ball)
        

    def draw_scores(self):
        Fonctions.draw_scores(self.screen, self.font, self.score_left, self.score_right)

    def draw_court(self):
        Fonctions.draw_court(self.screen)
