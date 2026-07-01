"""Guts Invaders: un mini Geometry Dash con aviones y disparos.

Ejecuta con: python main.py
Controles: ESPACIO/click para saltar, F/J para disparar, R para reiniciar.
"""

from __future__ import annotations

import math
import random
import sys
from dataclasses import dataclass

import pygame


def show_login_screen() -> bool:
    """Muestra pantalla de login y retorna True si el usuario ingresa."""
    pygame.init()
    ANCHO, ALTO = 800, 600
    ventana = pygame.display.set_mode((ANCHO, ALTO))
    pygame.display.set_caption("Menú de Inicio de Sesión - Guts Invaders")

    # Colores
    BLANCO = (255, 255, 255)
    NEGRO = (0, 0, 0)
    GRIS_CLARO = (200, 200, 200)
    AZUL = (50, 150, 250)

    # Fuentes
    fuente_titulo = pygame.font.SysFont(None, 50)
    fuente_texto = pygame.font.SysFont(None, 35)

    # Variables de entrada
    usuario = ""
    password = ""
    activo_usuario = False
    activo_password = False

    reloj = pygame.time.Clock()

    while True:
        ventana.fill(BLANCO)
        
        # Definir rects antes de los eventos
        input_usuario = pygame.Rect(ANCHO // 2 - 200, 250, 400, 50)
        input_password = pygame.Rect(ANCHO // 2 - 200, 380, 400, 50)
        boton_login = pygame.Rect(ANCHO // 2 - 100, 480, 200, 50)
        
        # Eventos
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
                
            if evento.type == pygame.MOUSEBUTTONDOWN:
                if input_usuario.collidepoint(evento.pos):
                    activo_usuario = True
                    activo_password = False
                elif input_password.collidepoint(evento.pos):
                    activo_usuario = False
                    activo_password = True
                elif boton_login.collidepoint(evento.pos):
                    print(f"✅ Sesión iniciada con Usuario: {usuario or 'invitado'}")
                    pygame.quit()  # Cerrar ventana de login
                    return True
                else:
                    activo_usuario = False
                    activo_password = False
                    
            if evento.type == pygame.KEYDOWN:
                if activo_usuario:
                    if evento.key == pygame.K_BACKSPACE:
                        usuario = usuario[:-1]
                    elif evento.key != pygame.K_RETURN:
                        usuario += evento.unicode
                elif activo_password:
                    if evento.key == pygame.K_BACKSPACE:
                        password = password[:-1]
                    elif evento.key != pygame.K_RETURN:
                        password += evento.unicode

        # Dibujar Título
        titulo = fuente_titulo.render("Iniciar Sesión", True, NEGRO)
        ventana.blit(titulo, (ANCHO // 2 - titulo.get_width() // 2, 100))

        # Campo Usuario
        color_rect_user = AZUL if activo_usuario else GRIS_CLARO
        pygame.draw.rect(ventana, color_rect_user, input_usuario, border_radius=5)
        texto_usuario = fuente_texto.render(usuario, True, NEGRO)
        ventana.blit(texto_usuario, (input_usuario.x + 10, input_usuario.y + 10))
        
        label_user = fuente_texto.render("Usuario:", True, NEGRO)
        ventana.blit(label_user, (input_usuario.x, input_usuario.y - 30))

        # Campo Contraseña
        color_rect_pass = AZUL if activo_password else GRIS_CLARO
        pygame.draw.rect(ventana, color_rect_pass, input_password, border_radius=5)
        password_oculto = "*" * len(password)
        texto_password = fuente_texto.render(password_oculto, True, NEGRO)
        ventana.blit(texto_password, (input_password.x + 10, input_password.y + 10))
        
        label_pass = fuente_texto.render("Contraseña:", True, NEGRO)
        ventana.blit(label_pass, (input_password.x, input_password.y - 30))

        # Botón de Login
        pygame.draw.rect(ventana, AZUL, boton_login, border_radius=5)
        texto_boton = fuente_texto.render("Ingresar", True, BLANCO)
        ventana.blit(texto_boton, (boton_login.x + (boton_login.width - texto_boton.get_width()) // 2, 
                                   boton_login.y + (boton_login.height - texto_boton.get_height()) // 2))

        # Instrucción
        instr = fuente_texto.render("Haz clic en 'Ingresar' para jugar", True, (100, 100, 100))
        ventana.blit(instr, (ANCHO // 2 - instr.get_width() // 2, 550))

        pygame.display.flip()
        reloj.tick(60)


# ====================== JUEGO ======================
WIDTH, HEIGHT = 960, 540
GROUND_Y = 448
FPS = 60
GRAVITY = 0.85
JUMP_FORCE = -15.5
SCROLL_SPEED = 5.8
PLAYER_X = 170

SKY = (13, 18, 42)
CYAN = (91, 221, 255)
YELLOW = (255, 216, 89)
ORANGE = (255, 139, 55)
RED = (255, 73, 92)
GREEN = (86, 255, 157)
PURPLE = (177, 93, 255)
WHITE = (245, 247, 255)


@dataclass
class Bullet:
    rect: pygame.Rect
    speed: float = 13.0

    def update(self) -> None:
        self.rect.x += int(self.speed)

    def draw(self, screen: pygame.Surface) -> None:
        pygame.draw.rect(screen, YELLOW, self.rect, border_radius=5)
        pygame.draw.circle(screen, WHITE, self.rect.midright, 4)


@dataclass
class Enemy:
    rect: pygame.Rect
    phase: float
    kind: str = "drone"

    def update(self, speed: float) -> None:
        self.rect.x -= int(speed)
        self.rect.y += int(math.sin(pygame.time.get_ticks() * 0.006 + self.phase) * 2)

    def draw(self, screen: pygame.Surface) -> None:
        if self.kind == "drone":
            pygame.draw.ellipse(screen, RED, self.rect)
            pygame.draw.ellipse(screen, (80, 14, 35), self.rect, 3)
            pygame.draw.circle(screen, CYAN, (self.rect.centerx + 10, self.rect.centery - 2), 7)
            pygame.draw.polygon(
                screen, ORANGE,
                [(self.rect.left + 8, self.rect.centery),
                 (self.rect.left - 18, self.rect.top + 8),
                 (self.rect.left - 18, self.rect.bottom - 8)]
            )
        else:
            pygame.draw.polygon(screen, PURPLE, [self.rect.midleft, self.rect.midtop, self.rect.midright, self.rect.midbottom])
            pygame.draw.polygon(screen, WHITE, [self.rect.midleft, self.rect.midtop, self.rect.midright, self.rect.midbottom], 2)


@dataclass
class Spike:
    rect: pygame.Rect

    def update(self, speed: float) -> None:
        self.rect.x -= int(speed)

    def draw(self, screen: pygame.Surface) -> None:
        points = [(self.rect.left, self.rect.bottom), (self.rect.centerx, self.rect.top), (self.rect.right, self.rect.bottom)]
        pygame.draw.polygon(screen, ORANGE, points)
        pygame.draw.polygon(screen, WHITE, points, 3)


class Player:
    def __init__(self) -> None:
        self.rect = pygame.Rect(PLAYER_X, GROUND_Y - 68, 88, 54)
        self.velocity_y = 0.0
        self.on_ground = True
        self.angle = 0.0

    def jump(self) -> None:
        if self.on_ground:
            self.velocity_y = JUMP_FORCE
            self.on_ground = False

    def update(self) -> None:
        self.velocity_y += GRAVITY
        self.rect.y += int(self.velocity_y)
        if self.rect.bottom >= GROUND_Y:
            self.rect.bottom = GROUND_Y
            self.velocity_y = 0
            self.on_ground = True
        self.angle = max(-22, min(22, -self.velocity_y * 2.2))

    def muzzle(self) -> tuple[int, int]:
        return self.rect.right - 6, self.rect.centery - 3

    def draw(self, screen: pygame.Surface) -> None:
        plane = pygame.Surface((100, 70), pygame.SRCALPHA)
        pygame.draw.polygon(plane, CYAN, [(8, 36), (60, 14), (94, 34), (58, 55)])
        pygame.draw.polygon(plane, (30, 95, 145), [(25, 36), (52, 0), (66, 31)])
        pygame.draw.polygon(plane, (30, 95, 145), [(30, 42), (52, 68), (64, 42)])
        pygame.draw.circle(plane, WHITE, (64, 30), 8)
        pygame.draw.polygon(plane, YELLOW, [(92, 34), (101, 29), (101, 39)])
        pygame.draw.polygon(plane, WHITE, [(8, 36), (60, 14), (94, 34), (58, 55)], 2)
        rotated = pygame.transform.rotate(plane, self.angle)
        screen.blit(rotated, rotated.get_rect(center=self.rect.center))


class Game:
    def __init__(self) -> None:
        pygame.init()
        pygame.display.set_caption("Guts Invaders - Aviones Dash")
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        self.clock = pygame.time.Clock()
        self.font = pygame.font.Font(None, 42)
        self.small_font = pygame.font.Font(None, 28)
        self.reset()

    def reset(self) -> None:
        self.player = Player()
        self.bullets: list[Bullet] = []
        self.enemies: list[Enemy] = []
        self.spikes: list[Spike] = []
        self.spawn_timer = 55
        self.score = 0
        self.distance = 0
        self.game_over = False
        self.clouds = [(random.randrange(WIDTH), random.randrange(35, 185), random.randrange(30, 80)) for _ in range(9)]

    # ... (el resto del código del juego se mantiene igual) ...

    def spawn_obstacle(self) -> None:
        if random.random() < 0.64:
            y = random.randint(175, GROUND_Y - 82)
            self.enemies.append(Enemy(pygame.Rect(WIDTH + 30, y, 70, 42), random.random() * 6.28, random.choice(["drone", "ship"])))
        else:
            self.spikes.append(Spike(pygame.Rect(WIDTH + 30, GROUND_Y - 62, 54, 62)))
        self.spawn_timer = random.randint(42, 82)

    def handle_events(self) -> bool:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
            if event.type == pygame.KEYDOWN:
                if event.key in (pygame.K_SPACE, pygame.K_UP, pygame.K_w):
                    self.player.jump()
                if event.key in (pygame.K_f, pygame.K_j):
                    self.shoot()
                if event.key == pygame.K_r and self.game_over:
                    self.reset()
            if event.type == pygame.MOUSEBUTTONDOWN:
                self.player.jump()
        return True

    def shoot(self) -> None:
        if not self.game_over:
            x, y = self.player.muzzle()
            self.bullets.append(Bullet(pygame.Rect(x, y, 24, 8)))

    def update(self) -> None:
        if self.game_over:
            return
        self.distance += 1
        speed = SCROLL_SPEED + min(3.4, self.distance / 1800)
        self.player.update()
        self.spawn_timer -= 1
        if self.spawn_timer <= 0:
            self.spawn_obstacle()
        for bullet in self.bullets:
            bullet.update()
        for enemy in self.enemies:
            enemy.update(speed)
        for spike in self.spikes:
            spike.update(speed)
        self.bullets = [b for b in self.bullets if b.rect.left < WIDTH]
        self.enemies = [e for e in self.enemies if e.rect.right > -20]
        self.spikes = [s for s in self.spikes if s.rect.right > -20]
        self.check_collisions()

    def check_collisions(self) -> None:
        for enemy in self.enemies[:]:
            if self.player.rect.colliderect(enemy.rect.inflate(-16, -12)):
                self.game_over = True
            for bullet in self.bullets[:]:
                if bullet.rect.colliderect(enemy.rect):
                    self.enemies.remove(enemy)
                    self.bullets.remove(bullet)
                    self.score += 100
                    break
        for spike in self.spikes:
            if self.player.rect.colliderect(spike.rect.inflate(-18, -8)):
                self.game_over = True
        self.score = max(self.score, self.distance // 6)

    def draw_background(self) -> None:
        self.screen.fill(SKY)
        for i in range(70):
            x = (i * 137 - self.distance * 2) % WIDTH
            y = (i * 71) % 230 + 10
            self.screen.set_at((x, y), (120, 142, 190))
        for idx, (x, y, size) in enumerate(self.clouds):
            cx = int((x - self.distance * (0.35 + idx * 0.02)) % (WIDTH + 160) - 80)
            pygame.draw.ellipse(self.screen, (28, 42, 80), (cx, y, size * 2, size // 2))
        for x in range(-80, WIDTH + 80, 80):
            offset = int((x - self.distance * SCROLL_SPEED) % 80)
            pygame.draw.rect(self.screen, (24, 31, 58), (offset - 80, GROUND_Y, 80, HEIGHT - GROUND_Y))
            pygame.draw.line(self.screen, CYAN, (offset - 80, GROUND_Y), (offset, GROUND_Y), 3)

    def draw_hud(self) -> None:
        score = self.font.render(f"Puntos: {self.score}", True, WHITE)
        help_text = self.small_font.render("ESPACIO/click: saltar  ·  F/J: disparar", True, (190, 205, 230))
        self.screen.blit(score, (24, 20))
        self.screen.blit(help_text, (24, 62))
        if self.game_over:
            overlay = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
            overlay.fill((0, 0, 0, 150))
            self.screen.blit(overlay, (0, 0))
            title = self.font.render("¡Game Over! Presiona R para reiniciar", True, YELLOW)
            self.screen.blit(title, title.get_rect(center=(WIDTH // 2, HEIGHT // 2)))

    def draw(self) -> None:
        self.draw_background()
        for spike in self.spikes:
            spike.draw(self.screen)
        for enemy in self.enemies:
            enemy.draw(self.screen)
        for bullet in self.bullets:
            bullet.draw(self.screen)
        self.player.draw(self.screen)
        self.draw_hud()
        pygame.display.flip()

    def run(self) -> None:
        running = True
        while running:
            running = self.handle_events()
            self.update()
            self.draw()
            self.clock.tick(FPS)
        pygame.quit()


if __name__ == "__main__":
    if show_login_screen():
        Game().run()
