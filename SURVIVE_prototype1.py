import pygame, sys, random, math

pygame.init()
screen = pygame.display.set_mode((1500, 1200))
clock = pygame.time.Clock()

running = True
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

class bullet:
    def __init__(self, x, y, angle_deg):
        self.image = pygame.image.load('WEAPONS_AMMO\\revolver_bullet.png').convert_alpha()
        self.image = pygame.transform.scale(self.image, (20, 20))
        self.x = x
        self.y = y
        self.angle = math.radians(angle_deg)
        self.speed = 600  # pixels per second
        self.dx = self.speed * math.cos(self.angle)
        self.dy = self.speed * -math.sin(self.angle)
        self.rect = self.image.get_rect(center=(self.x, self.y))

    def update(self, dt):
        self.x += self.dx * dt
        self.y += self.dy * dt
        self.rect.center = (self.x, self.y)

    def draw(self):
        screen.blit(self.image, self.rect.topleft)

class Revolver:
    def __init__(self, x, y):
        global revolver_img
        self.original_image = revolver_img
        self.image = revolver_img
        self.x = x
        self.y = y
        self.angle = 0
        self.frequency = 2  # Hz
        self.amplitude = 5
        self.rect = self.image.get_rect(center=(self.x, self.y))
        self.equipped = False
        self.fire_delay = 500
        self.last_fire_time = 0

    def update(self, dt, player_x=None, player_y=None):
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
            self.angle += self.frequency * dt * 2 * math.pi  # 2πf for angular motion
            self.y = y_revolver + self.amplitude * math.cos(self.angle)
            self.rect.center = (self.x, self.y)

    def draw(self):
        screen.blit(self.image, self.rect.topleft)

    def equip(self):
        self.equipped = True

    def can_fire(self):
        return pygame.time.get_ticks() - self.last_fire_time >= self.fire_delay

    def fire(self, bullets_list):
        if self.can_fire() and self.equipped:
            new_bullet = bullet(self.x, self.y, self.angle)
            bullets_list.append(new_bullet)
            self.last_fire_time = pygame.time.get_ticks()

class Player:
    def __init__(self, x, y):
        global player_img
        self.image = player_img
        self.x = x
        self.y = y
        self.speed = 200  # pixels per second
        self.rect = self.image.get_rect(center=(self.x, self.y))

    def movement(self, dt):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_w] or keys[pygame.K_UP]:
            self.y -= self.speed * dt
        if keys[pygame.K_s] or keys[pygame.K_DOWN]:
            self.y += self.speed * dt
        if keys[pygame.K_a] or keys[pygame.K_LEFT]:
            self.x -= self.speed * dt
        if keys[pygame.K_d] or keys[pygame.K_RIGHT]:
            self.x += self.speed * dt
        self.rect.center = (self.x, self.y)

    def draw(self):
        screen.blit(self.image, self.rect.topleft)

revolver = Revolver(x_revolver, y_revolver)
player = Player(x, y)
Bullets = []

while running:
    dt = clock.tick(60) / 1000.0  # Delta time in seconds

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    if pygame.mouse.get_pressed()[0]:
        revolver.fire(Bullets)

    screen.blit(background, (0, 0))
    player.movement(dt)

    if player.rect.colliderect(revolver.rect) and not revolver.equipped:
        revolver.equip()

    if revolver.equipped:
        revolver.update(dt, player.x, player.y)
    else:
        revolver.update(dt)

    player.draw()
    revolver.draw()

    for b in Bullets[:]:
        b.update(dt)
        b.draw()
        if b.x < 0 or b.x > 1500 or b.y < 0 or b.y > 1200:
            Bullets.remove(b)

    pygame.display.update()

pygame.quit()
