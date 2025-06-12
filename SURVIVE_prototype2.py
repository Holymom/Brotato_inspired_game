import pygame, sys, random, math

pygame.init()
screen = pygame.display.set_mode((1500, 1200))
pygame.display.set_caption("Brotato Inspired Game")

# Load homescreen and play button
homescreen = pygame.image.load('homescreen.jpg')
homescreen = pygame.transform.scale(homescreen, (1500, 1200))

play_button = pygame.image.load('play_button.png')
play_button = pygame.transform.scale(play_button, (300, 100))
play_button_rect = play_button.get_rect(center=(750, 600))

def load_assets():
    background = pygame.image.load('MAPS\\background.png').convert_alpha()
    background = pygame.transform.scale(background, (1500, 1200))

    player_img = pygame.image.load('player.png').convert_alpha()
    player_img = pygame.transform.scale(player_img, (120, 120))

    revolver_img = pygame.image.load('WEAPONS\\revolver.png').convert_alpha()
    revolver_img = pygame.transform.scale(revolver_img, (60, 60))

    x = 400
    y = 300
    x_revolver = random.randint(600, 900)
    y_revolver = random.randint(450, 750)

    return background, player_img, revolver_img, x, y, x_revolver, y_revolver

class Bullet:
    def __init__(self, x, y, angle_deg):
        self.image = pygame.image.load('WEAPONS_AMMO\\revolver_bullet.png').convert_alpha()
        self.image = pygame.transform.scale(self.image, (20, 20))
        self.x = x
        self.y = y
        self.angle = math.radians(angle_deg)
        self.speed = 5
        self.dx = self.speed * math.cos(self.angle)
        self.dy = self.speed * -math.sin(self.angle)
        self.rect = self.image.get_rect(center=(self.x, self.y))

    def update(self):
        self.x += self.dx
        self.y += self.dy
        self.rect.center = (self.x, self.y)

    def draw(self, screen):
        screen.blit(self.image, self.rect.topleft)

class Revolver:
    def __init__(self, x, y, image):
        self.original_image = image
        self.image = image
        self.x = x
        self.y = y
        self.y_original = y
        self.angle = 0
        self.frequency = 0.01
        self.amplitude = 5
        self.rect = self.image.get_rect(center=(self.x, self.y))
        self.equipped = False
        self.fire_delay = 500
        self.last_fire_time = 0

    def update(self, screen, player_x=None, player_y=None):
        if self.equipped and player_x is not None and player_y is not None:
            mx, my = pygame.mouse.get_pos()
            dx = mx - player_x
            dy = my - player_y
            distance = math.hypot(dx, dy)
            if distance == 0:
                distance = 1
            dx /= distance
            dy /= distance
            offset = 50
            self.x = player_x + dx * offset
            self.y = player_y + dy * offset
            self.angle = math.degrees(math.atan2(-dy, dx))
            self.image = pygame.transform.rotate(self.original_image, self.angle)
            self.rect = self.image.get_rect(center=(self.x, self.y))
        else:
            self.angle += self.frequency
            self.y = self.y_original + self.amplitude * math.cos(self.angle)
            self.rect.center = (self.x, self.y)

    def draw(self, screen):
        screen.blit(self.image, self.rect.topleft)

    def equip(self):
        self.equipped = True

    def can_fire(self):
        return pygame.time.get_ticks() - self.last_fire_time >= self.fire_delay

    def fire(self, bullets_list):
        if self.can_fire() and self.equipped:
            new_bullet = Bullet(self.x, self.y, self.angle)
            bullets_list.append(new_bullet)
            self.last_fire_time = pygame.time.get_ticks()

class Player:
    def __init__(self, x, y, image):
        self.image = image
        self.x = x
        self.y = y
        self.speed = 0.5
        self.rect = self.image.get_rect(center=(self.x, self.y))

    def movement(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_w] or keys[pygame.K_UP]:
            self.y -= self.speed
        if keys[pygame.K_s] or keys[pygame.K_DOWN]:
            self.y += self.speed
        if keys[pygame.K_a] or keys[pygame.K_LEFT]:
            self.x -= self.speed
        if keys[pygame.K_d] or keys[pygame.K_RIGHT]:
            self.x += self.speed
        self.rect.center = (self.x, self.y)

    def draw(self, screen):
        screen.blit(self.image, self.rect.topleft)

def main():
    background, player_img, revolver_img, x, y, x_revolver, y_revolver = load_assets()
    player = Player(x, y, player_img)
    revolver = Revolver(x_revolver, y_revolver, revolver_img)
    bullets = []

    clock = pygame.time.Clock()
    running = True
    while running:
        clock.tick(60)  # Ensure this is called exactly once per frame
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        if pygame.mouse.get_pressed()[0]:
            revolver.fire(bullets)

        screen.blit(background, (0, 0))
        player.movement()

        if player.rect.colliderect(revolver.rect) and not revolver.equipped:
            revolver.equip()

        if revolver.equipped:
            revolver.update(screen, player.x, player.y)
        else:
            revolver.update(screen)

        player.draw(screen)
        revolver.draw(screen)

        # Update and draw bullets, remove those out of bounds efficiently
        bullets = [b for b in bullets if 0 <= b.x <= 1500 and 0 <= b.y <= 1200]
        for b in bullets:
            b.update()
            b.draw(screen)

        pygame.display.update()

    pygame.quit()

def show_home_screen():
    while True:
        screen.blit(homescreen, (0, 0))
        screen.blit(play_button, play_button_rect.topleft)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                if play_button_rect.collidepoint(pygame.mouse.get_pos()):
                    return  # Exit home screen and start main game

        pygame.display.update()

if __name__ == "__main__":
    show_home_screen()
    main()

