import pygame
from sys import exit
import os
from random import randint, choice
from pygame import mixer

pygame.init()
mixer.init()
screen = pygame.display.set_mode((800,600))
pygame.display.set_caption("Mythical Catcher")
clock = pygame.time.Clock()

# Variables
creature_size = (105,105)
large_creature_size = (105,96)
font = pygame.font.Font("font/PlayfulTimeBLBB8.ttf", 50)
pastel_lavender = pygame.Color("#B19CD9")  # Soft purple
pastel_aqua = pygame.Color("#9AD9D9")     # Soft teal
pastel_maroon = pygame.Color("#D8A5A5")    # Soft red/pink
pastel_cream = pygame.Color("#FFFDD0")    # Soft background
score = 0
game_active = False
failed_catches = 0
frame = 0
spawn_delay = 1200
black = (0,0,0)

# Sound/Music
mixer.music.load(os.path.join("audio", "MythicalExplorationTheme.mp3"))
mixer.music.set_volume(0.2)
mixer.music.play(-1)
channel = pygame.mixer.Channel(0)
channel2 = pygame.mixer.Channel(1)
channel3 = pygame.mixer.Channel(2)
magic_sound = pygame.mixer.Sound(os.path.join("audio", "CaptureNoise.mp3"))
magic_sound.set_volume(0.3)
success_sound = pygame.mixer.Sound(os.path.join("audio", "Success.mp3"))
success_sound.set_volume(0.1)
failure_sound = pygame.mixer.Sound(os.path.join("audio", "Failure.mp3"))
failure_sound.set_volume(0.3)

class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load(os.path.join("graphics", "CatWitch.png")).convert_alpha()
        self.image = pygame.transform.scale(self.image,(145,145))
        self.rect = self.image.get_rect(midbottom = (400,600))

    def player_input(self):
        keys = pygame.key.get_pressed()
        vel = 7

        if keys[pygame.K_RIGHT]:
            if self.rect.right < 800:
                if frame < 10:
                    self.rect.x += vel
                elif frame > 10 and frame <= 20:
                    vel = 8
                    self.rect.x += vel
                elif frame > 20 and frame <= 30:
                    vel = 10
                    self.rect.x += vel
                elif frame > 30 and frame <= 40:
                    vel = 11
                    self.rect.x += vel
                elif frame > 40:
                    vel = 12
                    self.rect.x += vel

        if keys[pygame.K_LEFT]:
            if self.rect.left > 0:
                if frame < 10:
                    self.rect.x -= vel
                elif frame > 10 and frame <= 15:
                    vel = 8
                    self.rect.x -= vel
                elif frame > 15 and frame <= 20:
                    vel = 9
                    self.rect.x -= vel
                elif frame > 20 and frame <= 25:
                    vel = 10
                    self.rect.x -= vel
                elif frame > 25:
                    vel = 11
                    self.rect.x -= vel

    def update(self):
        self.player_input()
     
class MythicalCreature(pygame.sprite.Sprite):
    def __init__(self,type):
        super().__init__()

        if type == "unicorn":
            unicorn_surf = pygame.image.load(os.path.join("graphics", "unicorn.png")).convert_alpha()
            unicorn_surf = pygame.transform.scale(unicorn_surf, creature_size)
            self.frames = [unicorn_surf]
            y_pos = randint(-50,-10)

        elif type == "cyclops":
            cyclops_surf = pygame.image.load(os.path.join("graphics", "cyclops.png")).convert_alpha()
            cyclops_surf = pygame.transform.scale(cyclops_surf, creature_size)
            self.frames = [cyclops_surf]
            y_pos = randint(-50,-10)

        elif type == "dragon":
            dragon_surf = pygame.image.load(os.path.join("graphics", "dragon.png")).convert_alpha()
            dragon_surf = pygame.transform.scale(dragon_surf, large_creature_size)
            self.frames = [dragon_surf]
            y_pos = randint(-50,-10)
        
        elif type == "mermaid":
            mermaid_surf = pygame.image.load(os.path.join("graphics","mermaid.png")).convert_alpha()
            mermaid_surf = pygame.transform.scale(mermaid_surf, creature_size)
            self.frames = [mermaid_surf]
            y_pos = randint(-50,-10)

        elif type == "centaur":
            centaur_surf = pygame.image.load(os.path.join("graphics","centaur.png")).convert_alpha()
            centaur_surf = pygame.transform.scale(centaur_surf, large_creature_size)
            self.frames = [centaur_surf]
            y_pos = randint(-50,-10)
        
        elif type == "gnome":
            gnome_surf = pygame.image.load(os.path.join("graphics", "gnome.png")).convert_alpha()
            gnome_surf = pygame.transform.scale(gnome_surf, creature_size)
            self.frames = [gnome_surf]
            y_pos = randint(-50,-10)

        self.index = 0
        self.image = self.frames[self.index]
        self.rect = self.image.get_rect(center = (randint(100,700), y_pos))    
    
    def update(self):
        vel = 6
        if frame < 10:
            self.rect.y += vel
        elif frame > 10 and frame <= 20:
            vel = 7
            self.rect.y += vel
        elif frame > 20 and frame <= 30:
            vel = 8
            self.rect.y += vel
        elif frame > 30 and frame <= 40:
            vel = 9
            self.rect.y += vel
        elif frame > 40 and frame <= 50:
            vel = 10
            self.rect.y += vel 
        elif frame > 50 and frame <= 60:
            vel = 11
            self.rect.y += vel
        elif frame > 60 and frame <= 70:
            vel = 12
            self.rect.y += vel
        elif frame > 60 and frame <= 80:
            vel = 14
            self.rect.y += vel
        elif frame > 80:
            vel = 15
            self.rect.y += vel

        self.destroy()
        self.collisions()
    
    def destroy(self):
        global failed_catches
        if self.rect.y >= 615:
            self.kill()
            channel3.play(failure_sound)
            failed_catches += 1

    def collisions(self):
        global score
        collidelist = pygame.sprite.spritecollide(player.sprite, creatures_group,False)
        for i in collidelist:
            if i.rect.bottom < player.sprite.rect.top + 20:
                i.kill()
                score += 1
                channel2.play(success_sound)
                return True
            else: return False

# Game functions
def display_score():
    score_surf = font.render((f"Caught: {score}"),True, pastel_cream)
    score_surf = pygame.transform.scale(score_surf, (250,60))
    score_rect = score_surf.get_rect(center = (400,45))
    screen.blit(score_surf,score_rect)

def check_failed():
    if failed_catches >= 3:
        return False
    else:
        return True

def gameover_screen():
    global score, game_active, failed_catches, frame
    screen.fill((pastel_aqua))
    
    # Game Over text
    gameover_surf = font.render("GAME OVER", False, pastel_maroon)
    gameover_surf = pygame.transform.scale(gameover_surf, (400, 100))
    gameover_rect = gameover_surf.get_rect(center=(400, 150))
    
    # Final score
    score_surf = font.render(f"Final Score: {score}", False, pastel_cream)
    score_rect = score_surf.get_rect(center=(400, 250))
    
    # Play again prompt
    continue_surf = font.render("Press SPACE to play again", False, black)
    continue_rect = continue_surf.get_rect(center=(400, 350))
    
    # Quit prompt
    quit_surf = font.render("Press Q to quit", False, black)
    quit_rect = quit_surf.get_rect(center=(400, 400))
    
    # Draw everything
    screen.blit(gameover_surf, gameover_rect)
    screen.blit(score_surf, score_rect)
    screen.blit(continue_surf, continue_rect)
    screen.blit(quit_surf, quit_rect)

    # Check for key presses
    keys = pygame.key.get_pressed()
    if keys[pygame.K_SPACE]:
        # Reset game
        game_active = True
        creatures_group.empty()
        player.sprite.rect.midbottom = (400, 600)
        score = 0
        failed_catches = 0
        frame = 0
        channel.play(magic_sound)
    elif keys[pygame.K_q]:
        pygame.quit()
        exit()

def update_health():
    if failed_catches == 0:
        screen.blit(life_surf, life_rect)
        screen.blit(life_surf2, life_rect2)
        screen.blit(life_surf3, life_rect3)
    elif failed_catches == 1:
        screen.blit(life_surf2, life_rect2)
        screen.blit(life_surf3, life_rect3)
    else:
        screen.blit(life_surf3, life_rect3)

# Groups
player = pygame.sprite.GroupSingle()
player.add(Player())
creatures_group = pygame.sprite.Group()

# Backgrounds
starry_surf = pygame.image.load(os.path.join("graphics", "StarryBackground.png")).convert_alpha()
starry_surf = pygame.transform.scale(starry_surf,(850,300)).convert_alpha()
stars_rect = starry_surf.get_rect(midbottom =(350,715))

starry_surf2 = pygame.image.load(os.path.join("graphics", "StarryBackground.png")).convert_alpha()
starry_surf2 = pygame.transform.scale(starry_surf2,(850,300)).convert_alpha()
stars_rect2 = starry_surf2.get_rect(midbottom = (520,725))

magic_effect_surf = pygame.image.load(os.path.join("graphics", "Sparkles.png")).convert_alpha()
magic_effect_surf = pygame.transform.scale(magic_effect_surf, (450,550))
magic_effect_rect = magic_effect_surf.get_rect(midbottom = (400,600))

# Life Counter
life_surf = pygame.image.load(os.path.join("graphics", "pawprint.png")).convert_alpha()
life_surf = pygame.transform.scale(life_surf, (40,40))
life_rect = life_surf.get_rect(center = (650, 35))

life_surf2 = pygame.image.load(os.path.join("graphics", "pawprint.png")).convert_alpha()
life_surf2 = pygame.transform.scale(life_surf2, (40,40))
life_rect2 = life_surf.get_rect(center = (690, 35))

life_surf3 = pygame.image.load(os.path.join("graphics", "pawprint.png")).convert_alpha()
life_surf3 = pygame.transform.scale(life_surf3, (40,40))
life_rect3 = life_surf.get_rect(center = (730, 35))

# Creature Spawner
creature_timer = pygame.USEREVENT + 1
pygame.time.set_timer(creature_timer,spawn_delay)

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()

        if game_active:
            # Spawns random creature
            if event.type == creature_timer:
                creatures_group.add(MythicalCreature(choice(["unicorn","cyclops","dragon","mermaid","centaur","gnome"])))
                if frame < 10:
                    spawn_delay = 1200
                    pygame.time.set_timer(creature_timer,spawn_delay)
                elif frame > 10 and frame <= 20:
                    spawn_delay = 1000
                    pygame.time.set_timer(creature_timer,spawn_delay)
                elif frame > 20 and frame <= 30:
                    spawn_delay = 950
                    pygame.time.set_timer(creature_timer,spawn_delay) 
                elif frame > 30 and frame <= 40:
                    spawn_delay = 850
                    pygame.time.set_timer(creature_timer,spawn_delay)
                elif frame >= 40:
                    spawn_delay = 750
                    pygame.time.set_timer(creature_timer,spawn_delay)
        else:
            # Restart Game
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                game_active = True
                creatures_group.empty()
                player.sprite.rect.midbottom = (400,600)
                score = 0
                failed_catches = 0
                frame = 0
                mixer.music.play()
                channel.play(magic_sound)

    if game_active:
        screen.fill((pastel_aqua))
        screen.blit(pygame.transform.scale(starry_surf, (1000, 800)), (0, 0))
        screen.blit(starry_surf2,stars_rect2)
        
        update_health()
        
        display_score()

        player.draw(screen)
        player.update()
        creatures_group.draw(screen)
        creatures_group.update()
        game_active = check_failed()

        # Game Timer
        frame += 1 / 60

    else:
        # Initial game screen
        if frame == 0:
            screen.fill((pastel_aqua))
            gameover_surf = font.render(("Myth Catcher"),False,(pastel_lavender))
            gameover_surf = pygame.transform.scale(gameover_surf, (600, 150))
            gameover_rect = gameover_surf.get_rect(center = (400,100))
            magic_effect_surf = pygame.image.load(os.path.join("graphics", "CatWitch.png")).convert_alpha()
            magic_effect_surf = pygame.transform.scale(magic_effect_surf, (300,350)) 
            magic_effect_rect = magic_effect_surf.get_rect(midbottom = (400,525))
            continue_surf = font.render(("Press space to play"),False,(black))
            continue_rect = continue_surf.get_rect(center = (400,200))
            controls_surf = font.render(("Use arrow keys to move"),False,(black))
            controls_rect = controls_surf.get_rect(midbottom = (400,275))

            unicorn_surf = pygame.image.load(os.path.join("graphics", "unicorn.png")).convert_alpha()
            unicorn_surf = pygame.transform.scale(unicorn_surf, creature_size)
            unicorn_rect = unicorn_surf.get_rect(center = (150,200))

            mermaid_surf = pygame.image.load(os.path.join("graphics", "mermaid.png")).convert_alpha()
            mermaid_surf = pygame.transform.scale(mermaid_surf, creature_size)
            mermaid_rect = mermaid_surf.get_rect(center = (210,530))

            centaur_surf = pygame.image.load(os.path.join("graphics", "centaur.png")).convert_alpha()
            centaur_surf = pygame.transform.scale(centaur_surf, large_creature_size)
            centaur_rect = centaur_surf.get_rect(center = (670,195))

            cyclops_surf = pygame.image.load(os.path.join("graphics", "cyclops.png")).convert_alpha()
            cyclops_surf = pygame.transform.scale(cyclops_surf, creature_size)
            cyclops_rect = cyclops_surf.get_rect(center = (725,545))

            dragon_surf = pygame.image.load(os.path.join("graphics", "dragon.png")).convert_alpha()
            dragon_surf = pygame.transform.scale(dragon_surf, large_creature_size)
            dragon_rect = dragon_surf.get_rect(center = (615,380))

            gnome_surf = pygame.image.load(os.path.join("graphics", "gnome.png")).convert_alpha()
            gnome_surf = pygame.transform.scale(gnome_surf, creature_size)
            gnome_rect = gnome_surf.get_rect(center = (80,400))  

            screen.blit(gameover_surf,gameover_rect)
            screen.blit(magic_effect_surf,magic_effect_rect)
            screen.blit(continue_surf,continue_rect)
            screen.blit(controls_surf,controls_rect)
            screen.blit(unicorn_surf,unicorn_rect)
            screen.blit(mermaid_surf,mermaid_rect)
            screen.blit(centaur_surf,centaur_rect)
            screen.blit(cyclops_surf,cyclops_rect)
            screen.blit(dragon_surf,dragon_rect)
            screen.blit(gnome_surf,gnome_rect)

        else:
            mixer.music.stop()
            gameover_screen()

    pygame.display.update()
    clock.tick(60)