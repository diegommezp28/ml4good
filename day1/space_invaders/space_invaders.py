import os
import sys

import pygame

# Initialize pygame
pygame.init()

# Constants
WIDTH, HEIGHT = 800, 800  # Increased height for more vertical space
FPS = 60
PLAYER_SPEED = 5
BULLET_SPEED = 7
ENEMY_SPEED = 1.5  # Slowed down enemy speed
ENEMY_DROP = 20  # Reduced drop distance

# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)

# Initialize screen
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Space Invaders")
clock = pygame.time.Clock()


# Load sprites
def load_sprite(path, scale=1):
    """Load a sprite image and scale it if needed"""
    try:
        sprite = pygame.image.load(path)
        if scale != 1:
            new_size = (
                int(sprite.get_width() * scale),
                int(sprite.get_height() * scale),
            )
            sprite = pygame.transform.scale(sprite, new_size)
        return sprite
    except pygame.error:
        print(f"Error loading sprite: {path}")
        # Create a placeholder sprite if loading fails
        sprite = pygame.Surface((50, 30), pygame.SRCALPHA)
        pygame.draw.rect(sprite, RED, (0, 0, 50, 30))
        return sprite


class Player:
    def __init__(self):
        self.sprite = load_sprite(
            os.path.join("sprites", "BattleShip", "Spaceship_tut.png"),
            0.5,  # Scale down the battleship
        )
        self.width = self.sprite.get_width()
        self.height = self.sprite.get_height()
        self.x = WIDTH // 2 - self.width // 2
        self.y = HEIGHT - self.height - 50  # Moved player up from bottom
        self.speed = PLAYER_SPEED
        self.bullets: list[tuple[int, int]] = []
        # Create a simple bullet sprite
        self.bullet_sprite = pygame.Surface((4, 10), pygame.SRCALPHA)
        pygame.draw.rect(self.bullet_sprite, WHITE, (0, 0, 4, 10))

    def move(self, direction: int):
        self.x += self.speed * direction
        self.x = max(0, min(WIDTH - self.width, self.x))

    def shoot(self):
        self.bullets.append(
            (self.x + self.width // 2, self.y),
        )

    def update_bullets(self):
        self.bullets = [(x, y - BULLET_SPEED) for x, y in self.bullets if y > 0]

    def draw(self, surface):
        # Draw player
        surface.blit(self.sprite, (self.x, self.y))
        # Draw bullets
        for x, y in self.bullets:
            surface.blit(self.bullet_sprite, (x - 2, y))


class Enemy:
    def __init__(self, x: int, y: int):
        # Use the first PNG file from the AlienShips/png directory
        alien_ship_path = os.path.join(
            "sprites",
            "AlienShips",
            "png",
            os.listdir(os.path.join("sprites", "AlienShips", "png"))[0],
        )
        self.sprite = load_sprite(alien_ship_path, 0.3)  # Scale down the alien ship
        self.width = self.sprite.get_width()
        self.height = self.sprite.get_height()
        self.x = x
        self.y = y
        self.speed = ENEMY_SPEED
        self.direction = 1

    def update(self):
        self.x += self.speed * self.direction

    def draw(self, surface):
        surface.blit(self.sprite, (self.x, self.y))


class Game:
    def __init__(self):
        self.player = Player()
        self.enemies: list[Enemy] = []
        self.score = 0
        self.game_over = False
        self.font = pygame.font.Font(None, 36)
        self.initialize_enemies()

    def initialize_enemies(self):
        for row in range(5):
            for col in range(10):
                x = 50 + col * 60
                y = 100 + row * 50  # Increased vertical spacing between enemies
                self.enemies.append(Enemy(x, y))

    def update_enemies(self):
        change_direction = False
        for enemy in self.enemies:
            enemy.update()
            if enemy.x <= 0 or enemy.x + enemy.width >= WIDTH:
                change_direction = True

        if change_direction:
            for enemy in self.enemies:
                enemy.direction *= -1
                enemy.y += ENEMY_DROP

    def check_collisions(self):
        # Check bullet-enemy collisions
        for bullet in self.player.bullets[:]:
            for enemy in self.enemies[:]:
                if (
                    enemy.x <= bullet[0] <= enemy.x + enemy.width
                    and enemy.y <= bullet[1] <= enemy.y + enemy.height
                ):
                    if bullet in self.player.bullets:
                        self.player.bullets.remove(bullet)
                    if enemy in self.enemies:
                        self.enemies.remove(enemy)
                    self.score += 10
                    break

        # Check if enemies reached bottom
        for enemy in self.enemies:
            if enemy.y + enemy.height >= HEIGHT - 100:  # Increased safe zone
                self.game_over = True
                break

    def draw(self, surface):
        surface.fill(BLACK)
        self.player.draw(surface)
        for enemy in self.enemies:
            enemy.draw(surface)

        # Draw score
        score_text = self.font.render(
            f"Score: {self.score}",
            True,
            WHITE,
        )
        surface.blit(score_text, (10, 10))

        if self.game_over:
            game_over_text = self.font.render(
                "Game Over!",
                True,
                WHITE,
            )
            surface.blit(
                game_over_text,
                (WIDTH // 2 - 100, HEIGHT // 2 - 18),
            )


def main():
    game = Game()
    running = True

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    game.player.shoot()

        if not game.game_over:
            keys = pygame.key.get_pressed()
            if keys[pygame.K_LEFT]:
                game.player.move(-1)
            if keys[pygame.K_RIGHT]:
                game.player.move(1)

            game.player.update_bullets()
            game.update_enemies()
            game.check_collisions()

        game.draw(screen)
        pygame.display.flip()
        clock.tick(FPS)

    pygame.quit()
    sys.exit()


if __name__ == "__main__":
    main()
