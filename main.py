import pygame
import random

pygame.init()

# Colores
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)

# Pantalla
screen = pygame.display.set_mode((1000, 800))
pygame.display.set_caption("BJJ Game")

# Fuentes
font_small = pygame.font.SysFont("Arial", 20)
font_bold = pygame.font.SysFont("Arial", 30, bold=True)
font_button = pygame.font.SysFont("Arial", 25)

# Técnicas
TECNICAS = ["Armbar", "Kimura", "Triangle", "Guillotine", "Rear Naked Choke"]
DESCRIPCIONES = {
    "Armbar": "Un armbar es una técnica de sumisión que forza el codo del oponente.",
    "Kimura": "La kimura usa el brazo del oponente para rendirlo.",
    "Triangle": "El triángulo atrapa el cuello del oponente con las piernas.",
    "Guillotine": "La guillotina es una estrangulación con el brazo al cuello.",
    "Rear Naked Choke": "Estrangulación por la espalda usando los brazos."
}

class Player(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.Surface((50, 50))
        self.image.fill(RED)
        self.rect = self.image.get_rect(topleft=(x, y))

    def move(self, keys):
        if keys[pygame.K_LEFT]: self.rect.x -= 5
        if keys[pygame.K_RIGHT]: self.rect.x += 5
        if keys[pygame.K_UP]: self.rect.y -= 5
        if keys[pygame.K_DOWN]: self.rect.y += 5

    def draw(self):
        screen.blit(self.image, self.rect)

class Enemy(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.Surface((50, 50))
        self.image.fill(BLUE)
        self.rect = self.image.get_rect(topleft=(x, y))

    def move(self, player):
        if player.rect.x > self.rect.x: self.rect.x += 2
        elif player.rect.x < self.rect.x: self.rect.x -= 2
        if player.rect.y > self.rect.y: self.rect.y += 2
        elif player.rect.y < self.rect.y: self.rect.y -= 2

    def draw(self):
        screen.blit(self.image, self.rect)

def get_random_position():
    return random.randint(100, 900), random.randint(100, 700)

class Message:
    @staticmethod
    def show(text, y, color=WHITE, font=font_small):
        text_surface = font.render(text, True, color)
        screen.blit(text_surface, (100, y))

class Game:
    def __init__(self):
        self.button_rect = pygame.Rect(300, 500, 250, 50)
        self.tecnicas_aprendidas = []
        self.tecnica_3 = []
        self.puntos = 0
        self.intentos = 0
        self.tecnica_seleccionada = None
        self.jugador_capturado = False
        self.continuar = False
        self.reset_game()

    def reset_game(self):
        self.player = Player(*get_random_position())
        self.enemy = Enemy(*get_random_position())
        while self.player.rect.colliderect(self.enemy.rect):
            self.enemy = Enemy(*get_random_position())
        self.jugador_capturado = False
        self.continuar = False
        self.tecnica_seleccionada = None

    def update(self):
        keys = pygame.key.get_pressed()
        if self.intentos >= 4:
            mouse_pos = pygame.mouse.get_pos()
            if self.button_rect.collidepoint(mouse_pos) and pygame.mouse.get_pressed()[0]:
                self.tecnicas_aprendidas = []
                self.intentos = 0
                self.puntos = 0
                self.reset_game()
            return

        if not self.jugador_capturado:
            self.player.move(keys)
            self.enemy.move(self.player)
            if self.player.rect.colliderect(self.enemy.rect):
                self.jugador_capturado = True
                self.tecnica_3 = random.sample(TECNICAS, 3)
        else:
            if keys[pygame.K_1]: self.select_technique(0)
            elif keys[pygame.K_2]: self.select_technique(1)
            elif keys[pygame.K_3]: self.select_technique(2)

        if self.continuar:
            self.intentos += 1
            self.continuar = False
            self.reset_game()

    def select_technique(self, index):
        if index < len(self.tecnica_3):
            self.tecnica_seleccionada = self.tecnica_3[index]
            self.show_technique_description()

    def draw(self):
        screen.fill(BLACK)
        if self.intentos >= 4:
            self.show_end_game_screen()
        elif self.jugador_capturado:
            Message.show(f"Técnicas aprendidas: {self.puntos}", 20, YELLOW, font_bold)
            self.display_techniques()
        else:
            self.player.draw()
            self.enemy.draw()

    def display_techniques(self):
        Message.show("¡Te atraparon! Elige una técnica:", 100, YELLOW)
        for i, tecnica in enumerate(self.tecnica_3):
            Message.show(f"{i+1}. {tecnica}", 150 + (i * 50))
        if self.tecnica_seleccionada:
            Message.show(f"Elegiste: {self.tecnica_seleccionada}", 320)
            Message.show(DESCRIPCIONES[self.tecnica_seleccionada], 360)

    def show_technique_description(self):
        if self.tecnica_seleccionada and self.tecnica_seleccionada not in self.tecnicas_aprendidas:
            self.tecnicas_aprendidas.append(self.tecnica_seleccionada)
            self.puntos += 1
        self.tecnica_seleccionada = None
        self.continuar = True

    def show_end_game_screen(self):
        Message.show("Conociste estas técnicas:", 80, YELLOW, font_bold)
        y_offset = 130
        for tecnica in self.tecnicas_aprendidas:
            Message.show(f"{tecnica}: {DESCRIPCIONES[tecnica]}", y_offset)
            y_offset += 40
        Message.show("Gracias por jugar", y_offset + 20, YELLOW, font_bold)
        pygame.draw.rect(screen, YELLOW, self.button_rect)
        button_text = font_button.render("Volver a jugar", True, BLACK)
        screen.blit(button_text, (self.button_rect.x + 30, self.button_rect.y + 10))

def main():
    game = Game()
    clock = pygame.time.Clock()
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        game.update()
        game.draw()
        pygame.display.flip()
        clock.tick(30)
    pygame.quit()

if __name__ == "__main__":
    main()
