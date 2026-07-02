# src/entities/base.py
import pygame


class Entity(pygame.sprite.Sprite):
    """
    🧱 BASE ENTITY (Now a real pygame.sprite.Sprite)

    الفرق عن الكلاس القديم:
    - بيورث من pygame.sprite.Sprite عشان ينضم لأي Group (all_sprites, zombies_group...)
    - لازم كل subclass يحدد self.image (Surface) عشان الـ Group تقدر ترسمه تلقائيًا
      عن طريق group.draw(screen)
    - self.kill() بقت متاحة افتراضيًا بدل ما تعمل remove() يدوي من اللستة
    """

    def __init__(self, x, y, width, height, *groups):
        super().__init__(*groups)
        self.x = x
        self.y = y
        self.width = width
        self.height = height

        self.health = 100
        self.health_limit = 100

        # كل entity لازم يكون عنده image (حتى لو placeholder شفاف لحد ما الـ subclass يحددها)
        self.image = pygame.Surface((width, height), pygame.SRCALPHA)
        self.rect = self.image.get_rect(topleft=(x, y))

    def update_rect(self):
        self.rect.x = self.x
        self.rect.y = self.y
        self.rect.width = self.width
        self.rect.height = self.height

    def health_system(self, entity=None, health=None):
        if entity:
            self.health -= entity.damage
            if self.health <= 0:
                self.is_dead = True
        if health:
            if self.health_limit >= self.health + health:
                self.health += health
            else:
                self.health = self.health_limit

    def get_health_bar_index(self, slices):
        base = self.health_limit / slices
        value = self.health_limit - self.health
        idx = int(value // base)
        return max(0, min(idx, slices - 1))

    def world_draw(self, screen, camera_x, camera_y):
        """
        رسم بسيط بإزاحة الكاميرا. متاحة لأي entity بسيط (Tree, DeadBullet...)
        Player/Zombie عندهم منطق رسم خاص (اختيار frame) فبيعملوا override.
        """
        screen.blit(self.image, (self.x - camera_x, self.y - camera_y))
