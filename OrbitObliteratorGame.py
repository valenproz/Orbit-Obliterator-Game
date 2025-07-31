import pygame
import os
import random
from pygame import mixer

class SpaceExploder:
    def __init__(self):
        pygame.init()
        mixer.init()
        
        # Game constants
        self.SCREEN_WIDTH = 800
        self.SCREEN_HEIGHT = 600
        self.FPS = 60
        
        # Initialize game
        self.screen = pygame.display.set_mode((self.SCREEN_WIDTH, self.SCREEN_HEIGHT))
        pygame.display.set_caption("Space Exploder")
        self.clock = pygame.time.Clock()
        self.font = self.load_font("font/Pixeltype.ttf", 50)
        
        # Game assets
        self.load_assets()
        self.setup_game()
        
        # Start main loop
        self.run()

    def load_font(self, path, size):
        """Load custom font with error handling"""
        try:
            return pygame.font.Font(path, size)
        except:
            return pygame.font.SysFont("arial", size)

    def load_assets(self):
        """Load all game assets"""
        # Colors
        self.colors = {
            "space": pygame.Color("#0F0F1B"),
            "accent": pygame.Color("#FF4500"),
            "text": pygame.Color("#FFFFFF"),
            "warning": pygame.Color("#FF0000")
        }
        
        # Sounds
        self.sounds = {
            "background": self.load_sound("audio/background.mp3", volume=0.2),
            "explosion": self.load_sound("audio/explosion.mp3", volume=0.3),
            "success": self.load_sound("audio/success.mp3", volume=0.3),
            "failure": self.load_sound("audio/failure.mp3", volume=0.3)
        }
        
        # Channels
        self.channels = [pygame.mixer.Channel(i) for i in range(3)]

    def load_sound(self, path, volume=1.0):
        """Load sound with error handling"""
        try:
            sound = pygame.mixer.Sound(os.path.join("audio", os.path.basename(path)))
            sound.set_volume(volume)
            return sound
        except:
            print(f"Failed to load sound: {path}")
            return None

    def setup_game(self):
        """Initialize game state"""
        self.score = 0
        self.game_active = False
        self.failed_catches = 0
        self.frame_count = 0
        self.spawn_interval = 1200
        
        # Sprite groups
        self.player = pygame.sprite.GroupSingle()
        self.player.add(Player(self))
        self.obstacle_group = pygame.sprite.Group()
        
        # Background elements
        self.background = self.create_starfield()
        self.setup_obstacle_timer()

    def create_starfield(self):
        """Generate dynamic starfield background"""
        stars = []
        for _ in range(100):
            x = random.randint(0, self.SCREEN_WIDTH)
            y = random.randint(0, self.SCREEN_HEIGHT)
            size = random.randint(1, 3)
            speed = random.uniform(0.1, 0.5)
            stars.append({"pos": [x, y], "size": size, "speed": speed})
        return stars

    def setup_obstacle_timer(self):
        """Initialize obstacle spawning timer"""
        self.obstacle_timer = pygame.USEREVENT + 1
        pygame.time.set_timer(self.obstacle_timer, self.spawn_interval)

    def run(self):
        """Main game loop"""
        while True:
            self.handle_events()
            self.update()
            self.draw()
            self.clock.tick(self.FPS)

    def handle_events(self):
        """Process all game events"""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
                
            if self.game_active:
                self.handle_gameplay_events(event)
            else:
                self.handle_menu_events(event)

    def handle_gameplay_events(self, event):
        """Handle events during active gameplay"""
        if event.type == self.obstacle_timer:
            self.spawn_obstacle()
            self.adjust_difficulty()

    def handle_menu_events(self, event):
        """Handle events in menu/restart screen"""
        if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
            self.reset_game()

    def spawn_obstacle(self):
        """Create new space obstacle"""
        obstacle_types = ["asteroid", "comet", "satellite", "ufo", "debris"]
        self.obstacle_group.add(Obstacle(self, random.choice(obstacle_types)))

    def adjust_difficulty(self):
        """Increase game difficulty over time"""
        if self.frame_count < 600:  # 10 seconds
            self.spawn_interval = max(750, 1200 - int(self.frame_count * 0.75))
            pygame.time.set_timer(self.obstacle_timer, self.spawn_interval)

    def reset_game(self):
        """Reset game state for new round"""
        self.game_active = True
        self.obstacle_group.empty()
        self.player.sprite.rect.midbottom = (400, 600)
        self.score = 0
        self.failed_catches = 0
        self.frame_count = 0
        self.spawn_interval = 1200
        self.play_sound("background", loop=True)
        self.play_sound("explosion")

    def update(self):
        """Update game state"""
        if self.game_active:
            self.frame_count += 1
            self.player.update()
            self.obstacle_group.update()
            self.check_game_over()

    def check_game_over(self):
        """Check if game should end"""
        if self.failed_catches >= 3:
            self.game_active = False
            self.stop_music()

    def draw(self):
        """Render all game elements"""
        if self.game_active:
            self.draw_game()
        else:
            self.draw_menu()

        pygame.display.update()

    def draw_game(self):
        """Draw gameplay screen"""
        self.screen.fill(self.colors["space"])
        self.draw_starfield()
        self.draw_score()
        self.draw_health()
        self.player.draw(self.screen)
        self.obstacle_group.draw(self.screen)

    def draw_menu(self):
        """Draw menu/restart screen"""
        self.screen.fill(self.colors["space"])
        self.draw_starfield()
        
        if self.frame_count == 0:
            self.draw_start_screen()
        else:
            self.draw_game_over()

    def draw_starfield(self):
        """Animate starfield background"""
        for star in self.background:
            pygame.draw.circle(self.screen, (255, 255, 255), 
                             (int(star["pos"][0]), int(star["pos"][1])), 
                             star["size"])
            star["pos"][1] += star["speed"]
            if star["pos"][1] > self.SCREEN_HEIGHT:
                star["pos"][1] = 0
                star["pos"][0] = random.randint(0, self.SCREEN_WIDTH)

    def draw_score(self):
        """Render score display"""
        score_surf = self.font.render(f"Score: {self.score}", True, self.colors["text"])
        self.screen.blit(score_surf, (20, 20))

    def draw_health(self):
        """Render health indicator"""
        for i in range(3 - self.failed_catches):
            pygame.draw.circle(self.screen, self.colors["warning"], 
                             (self.SCREEN_WIDTH - 30 - (i * 40), 30), 15)

    def draw_start_screen(self):
        """Draw initial start screen"""
        title = self.font.render("SPACE EXPLODER", True, self.colors["accent"])
        instructions = self.font.render("Press SPACE to begin", True, self.colors["text"])
        controls = self.font.render("Use ARROW KEYS to move", True, self.colors["text"])
        
        self.screen.blit(title, (self.SCREEN_WIDTH//2 - title.get_width()//2, 100))
        self.screen.blit(instructions, (self.SCREEN_WIDTH//2 - instructions.get_width()//2, 200))
        self.screen.blit(controls, (self.SCREEN_WIDTH//2 - controls.get_width()//2, 270))

    def draw_game_over(self):
        """Draw game over screen"""
        title = self.font.render("GAME OVER", True, self.colors["accent"])
        score = self.font.render(f"Final Score: {self.score}", True, self.colors["text"])
        restart = self.font.render("Press SPACE to try again", True, self.colors["text"])
        
        self.screen.blit(title, (self.SCREEN_WIDTH//2 - title.get_width()//2, 100))
        self.screen.blit(score, (self.SCREEN_WIDTH//2 - score.get_width()//2, 180))
        self.screen.blit(restart, (self.SCREEN_WIDTH//2 - restart.get_width()//2, 260))

    def play_sound(self, sound_name, loop=False):
        """Play specified sound"""
        if sound_name in self.sounds and self.sounds[sound_name]:
            if loop:
                self.sounds[sound_name].play(-1)
            else:
                self.sounds[sound_name].play()

    def stop_music(self):
        """Stop background music"""
        pygame.mixer.music.stop()


class Player(pygame.sprite.Sprite):
    def __init__(self, game):
        super().__init__()
        self.game = game
        self.image = self.load_image("graphics/spaceship.png", (80, 80))
        self.rect = self.image.get_rect(midbottom=(400, 600))
        self.speed = 7
        self.boost_multiplier = 1.0

    def load_image(self, path, size):
        """Load and scale image with error handling"""
        try:
            img = pygame.image.load(os.path.join("graphics", os.path.basename(path))).convert_alpha()
            return pygame.transform.scale(img, size)
        except:
            # Fallback surface if image fails to load
            surf = pygame.Surface(size)
            surf.fill((255, 0, 0))
            return surf

    def update(self):
        """Update player position"""
        keys = pygame.key.get_pressed()
        
        # Dynamic speed based on boost (hold time)
        if keys[pygame.K_LEFT] or keys[pygame.K_RIGHT]:
            self.boost_multiplier = min(1.75, self.boost_multiplier + 0.01)
        else:
            self.boost_multiplier = max(1.0, self.boost_multiplier - 0.05)
        
        current_speed = self.speed * self.boost_multiplier
        
        if keys[pygame.K_LEFT] and self.rect.left > 0:
            self.rect.x -= current_speed
        if keys[pygame.K_RIGHT] and self.rect.right < self.game.SCREEN_WIDTH:
            self.rect.x += current_speed


class Obstacle(pygame.sprite.Sprite):
    def __init__(self, game, obstacle_type):
        super().__init__()
        self.game = game
        self.type = obstacle_type
        self.image = self.load_image()
        self.rect = self.image.get_rect(center=(random.randint(100, 700), random.randint(-50, -10)))
        self.speed = 6
        self.dynamic_speed = 1.0

    def load_image(self):
        """Load appropriate image based on obstacle type"""
        size = (60, 60) if random.random() > 0.3 else (80, 60)
        
        # Fallback color coding if images fail to load
        colors = {
            "asteroid": (169, 169, 169),
            "comet": (173, 216, 230),
            "satellite": (192, 192, 192),
            "ufo": (0, 255, 0),
            "debris": (139, 69, 19)
        }
        
        try:
            img = pygame.image.load(f"graphics/{self.type}.png").convert_alpha()
            return pygame.transform.scale(img, size)
        except:
            surf = pygame.Surface(size)
            surf.fill(colors.get(self.type, (255, 0, 255)))
            return surf

    def update(self):
        """Update obstacle position and check collisions"""
        self.dynamic_speed = min(2.5, 1.0 + self.game.frame_count / 240)  # Scale over 4 seconds
        self.rect.y += self.speed * self.dynamic_speed
        
        self.check_boundaries()
        self.check_collision()

    def check_boundaries(self):
        """Remove obstacle if it goes off screen"""
        if self.rect.y >= self.game.SCREEN_HEIGHT + 15:
            self.kill()
            self.game.play_sound("failure")
            self.game.failed_catches += 1

    def check_collision(self):
        """Handle collision with player"""
        if pygame.sprite.collide_rect(self, self.game.player.sprite):
            if self.rect.bottom < self.game.player.sprite.rect.top + 20:
                self.kill()
                self.game.score += 1
                self.game.play_sound("success")


if __name__ == "__main__":
    game = SpaceExploder()