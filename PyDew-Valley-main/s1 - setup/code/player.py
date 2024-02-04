import pygame
from settings import *
from support import *
from timer import Timer


class Player(pygame.sprite.Sprite):
    def __init__(self, pos, group, collision_sprites):
        super().__init__(group)

        self.FRAME_CONSTANT = 4

        self.import_assets()
        self.status = 'down'
        self.frame_index = 0

        # general set up
        self.image = self.animations[self.status][self.frame_index]
        # self.image.fill('green')
        self.rect = self.image.get_rect(center=pos)
        self.z = LAYERS['main']

        # movement attributes
        self.direction = pygame.math.Vector2()
        self.pos = pygame.math.Vector2(self.rect.center)
        self.speed = 300

        #collision
        self.collision_sprites = collision_sprites
        self.hitbox = self.rect.copy().inflate((-126, -70))

        self.timers = {
            'tool use': Timer(350, self.use_tool),
            'seed use': Timer(300)
        }

        # tools
        self.tools = ['hoe','axe','water']
        self.tool_index = 0
        self.selected_tool = self.tools[self.tool_index]

        self.seeds = ['corn','tomato']
        self.seed_index = 0
        self.selected_seed = self.seeds[self.seed_index]

    def use_tool(self):
        pass

    def use_seed(self):
        pass

    def import_assets(self):
        self.animations = {'up': [], 'down': [], 'left': [], 'right': [], 'pam_idle': [],
                           'right_idle': [], 'left_idle': [], 'up_idle': [], 'down_idle': [],
                           'right_hoe': [], 'left_hoe': [], 'up_hoe': [], 'down_hoe': [],
                           'right_axe': [], 'left_axe': [], 'up_axe': [], 'down_axe': [],
                           'right_water': [], 'left_water': [], 'up_water': [], 'down_water': []}

        for animation in self.animations.keys():
            full_path = '../graphics/character/' + animation
            self.animations[animation] = import_folder(full_path)

    def animate(self, dt):
        self.frame_index += self.FRAME_CONSTANT * dt
        if self.frame_index >= len(self.animations[self.status]):
            self.frame_index = 0

        self.image = self.animations[self.status][int(self.frame_index)]

    def input(self):
        keys = pygame.key.get_pressed()
        if not self.timers['tool use'].active:
            tool_usage = 1
        else:
            tool_usage = 0.5

        if keys[pygame.K_UP]:
            self.direction.y = -1*tool_usage
            self.status = 'up'
        elif keys[pygame.K_DOWN]:
            self.direction.y = 1*tool_usage
            self.status = 'down'
        else:
            self.direction.y = 0
        if keys[pygame.K_RIGHT]:
            self.direction.x = 1*tool_usage
            self.status = 'right'
        elif keys[pygame.K_LEFT]:
            self.direction.x = -1*tool_usage
            self.status = 'left'
        else:
            self.direction.x = 0

        if keys[pygame.K_SPACE]:
            self.timers['tool use'].activate()
            self.frame_index = 0

        if keys[pygame.K_1]:
            self.tool_index = 0
        elif keys[pygame.K_2]:
            self.tool_index = 1
        elif keys[pygame.K_3]:
            self.tool_index = 2
        self.selected_tool = self.tools[self.tool_index]

        if keys[pygame.K_q]:
            self.timers['seed use'].activate()
            self.frame_index = 0
            print('use seed')

        if keys[pygame.K_4]:
            self.selected_seed = self.seeds[0]
        if keys[pygame.K_5]:
            self.selected_seed = self.seeds[1]

    def get_status(self):
        # idle
        if self.direction.magnitude() == 0:
            self.status = self.status.split('_')[0] + '_idle'

        if self.timers['tool use'].active:
            self.status = self.status.split('_')[0] + '_' + self.selected_tool

    def update_timers(self):
        for timer in self.timers.values():
            timer.update()

    def collision(self, direction):
        for sprite in self.collision_sprites.sprites():
            if hasattr(sprite, 'hitbox'):
                if sprite.hitbox.colliderect(self.hitbox):
                    if direction == 'horizontal':
                        if self.direction.x > 0: #moving right
                            self.hitbox.right = sprite.hitbox.left
                        if self.direction.x < 0: #moving left
                            self.hitbox.left = sprite.hitbox.right
                        self.rect.centerx = self.hitbox.centerx
                        self.pos.x = self.hitbox.centerx
                    if direction == 'vertical':
                        if self.direction.y > 0:  # moving down
                            self.hitbox.bottom = sprite.hitbox.top
                        if self.direction.y < 0: #moving down
                            self.hitbox.top = sprite.hitbox.bottom
                        self.rect.centery = self.hitbox.centery
                        self.pos.y = self.hitbox.centery
                    # if direction == 'vertical':
                    #     if self.direction.y > 0:  # moving down
                    #         self.hitbox.bottom = sprite.hitbox.top
                    #     if self.direction.y < 0:  # moving up
                    #         self.hitbox.top = sprite.hitbox.bottom
                    #     self.rect.centery = self.hitbox.centery
                    #     self.pos.y = self.hitbox.centery



    def move(self, dt):
        # normalise vector
        # if self.direction.magnitude() > 0:
        #     self.direction = self.direction.normalize()
        # horizontal
        self.pos.x += self.direction.x * self.speed * dt
        self.hitbox.centerx = round(self.pos.x)
        self.rect.centerx = self.hitbox.centerx
        self.collision('horizontal')
        # vertical
        self.pos.y += self.direction.y * self.speed * dt
        self.hitbox.centery = round(self.pos.y)
        self.rect.centery = self.hitbox.centery
        self.collision('vertical')

    def update(self, dt):
        self.input()
        self.get_status()
        self.update_timers()

        self.move(dt)
        self.animate(dt)
