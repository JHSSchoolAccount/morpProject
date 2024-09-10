import pygame
import sys
import random
import math

# Initialize Pygame
pygame.init()

# Set up the display
width, height = 1280, 720
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Morp(1)")

# Load the Morp.png image and set it as the window icon
icon = pygame.image.load('Pictures/Morp.png')
pygame.display.set_icon(icon)

# Load the pause button image
pause_button = pygame.image.load('Pictures/Pause.png').convert_alpha()
pause_button_rect = pause_button.get_rect(topright=(width - 10, 10))  # Top right corner

# Define colors
white = (255, 255, 255)
black = (0, 0, 0)
green = (0, 255, 0)
red = (255, 0, 0)
blue = (0, 0, 255)
gray = (128, 128, 128)


# Define the Player class
class Player(pygame.sprite.Sprite):
    def __init__(self, x, y, image_path):
        super().__init__()
        self.x = x
        self.y = y
        self.image_path = image_path

        # Load the character image
        self.original_image = pygame.image.load(self.image_path).convert_alpha()
        self.image = self.original_image
        self.rect = self.image.get_rect()
        self.rect.topleft = (self.x, self.y)

        # Player attributes
        self.speed = 3
        self.hp = 100
        self.direction = 'right'

        # XP and Leveling attributes
        self.level = 1
        self.xp = 0
        self.xp_needed = 100  # Initial XP required to level up

        # Cooldown for taking damage (in milliseconds)
        self.damage_cooldown = 500  # 0.5 second cooldown
        self.last_damage_time = 0  # Tracks the last time the player took damage

        # Blinking effect when taking damage
        self.is_blinking = False
        self.blink_duration = 300  # Blink duration in milliseconds
        self.blink_start_time = 0

    def update(self, keys, obstacles, candies, slimes, screen_width, screen_height):
        # Movement logic with WASD keys
        if keys[pygame.K_w]:
            self.rect.y -= self.speed
        if keys[pygame.K_s]:
            self.rect.y += self.speed
        if keys[pygame.K_a]:
            self.rect.x -= self.speed
            if self.direction != 'left':
                self.image = pygame.transform.flip(self.original_image, True, False)
                self.direction = 'left'
        if keys[pygame.K_d]:
            self.rect.x += self.speed
            if self.direction != 'right':
                self.image = self.original_image
                self.direction = 'right'

        # Handle blinking when taking damage
        if self.is_blinking:
            current_time = pygame.time.get_ticks()
            if current_time - self.blink_start_time > self.blink_duration:
                self.is_blinking = False
                self.image = self.original_image  # Revert to normal image

        # Collision detection with window boundaries
        self.check_window_collision(screen_width, screen_height)

        # Check for candy collision and collect XP
        candy_collisions = pygame.sprite.spritecollide(self, candies, True)
        for candy in candy_collisions:
            self.gain_xp(10)

            # Check if the player can level up
            self.check_level_up()

        # Damage for player ------------------------------------------

        # Check for collisions with slimes and take damage (with cooldown)
        slime_collisions = pygame.sprite.spritecollide(self, slimes, False)
        for slime in slime_collisions:
            self.take_damage(10)  # Try to take 10 damage on slime collision

        # Check for collisions with obstacles (if any)
        if pygame.sprite.spritecollide(self, obstacles, False):
            self.hp -= 1  # Reduce HP on collision

    def take_damage(self, amount):
        # Get the current time
        current_time = pygame.time.get_ticks()

        # Check if enough time has passed since the last damage
        if current_time - self.last_damage_time > self.damage_cooldown:
            self.hp -= amount
            self.last_damage_time = current_time  # Update the last damage time
            print(f"Player took {amount} damage. Current HP: {self.hp}")

            # Trigger blinking effect
            self.is_blinking = True
            self.blink_start_time = current_time
            self.image = self.original_image.copy()  # Copy the original image
            self.image.fill((255, 0, 0), special_flags=pygame.BLEND_RGBA_MULT)  # Tint red

        if self.hp <= 0:
            print("Game Over!")
            pygame.quit()
            sys.exit()

        # -----------------------------------------------------------

    def gain_xp(self, amount):
        self.xp += amount
        print(f"Player gained {amount} XP. Current XP: {self.xp}/{self.xp_needed}")

    def get_xp_progress(self):
        return self.xp / self.xp_needed

    def check_level_up(self):
        if self.xp >= self.xp_needed:
            self.level += 1
            self.xp -= self.xp_needed  # Carry over remaining XP
            self.xp_needed = int(self.xp_needed * 1.2)
            print(f"Level Up! Player is now level {self.level}.")

    def check_window_collision(self, screen_width, screen_height):
        if self.rect.left < 0:
            self.rect.left = 0
        if self.rect.right > screen_width:
            self.rect.right = screen_width
        if self.rect.top < 0:
            self.rect.top = 0
        if self.rect.bottom > screen_height:
            self.rect.bottom = screen_height

    def get_hp(self):
        return self.hp


    def gain_xp(self, amount):
        self.xp += amount
        print(f"Player gained {amount} XP. Current XP: {self.xp}/{self.xp_needed}")

    def get_xp_progress(self):
        return self.xp / self.xp_needed


    def check_level_up(self):
        if self.xp >= self.xp_needed:
            self.level += 1
            self.xp -= self.xp_needed  # Carry over remaining XP
            self.xp_needed = int(self.xp_needed * 1.5)
            print(f"Level Up! Player is now level {self.level}.")

    def check_window_collision(self, screen_width, screen_height):
        if self.rect.left < 0:
            self.rect.left = 0
        if self.rect.right > screen_width:
            self.rect.right = screen_width
        if self.rect.top < 0:
            self.rect.top = 0
        if self.rect.bottom > screen_height:
            self.rect.bottom = screen_height

    def get_hp(self):
        return self.hp



# Define the Candy class
class Candy(pygame.sprite.Sprite):
    def __init__(self, image_path):
        super().__init__()
        self.image = pygame.image.load(image_path).convert_alpha()
        self.rect = self.image.get_rect()
        self.spawn_random()

    def spawn_random(self):
        self.rect.x = random.randint(0, width - self.rect.width)
        self.rect.y = random.randint(0, height - self.rect.height)

# Define the Slime class
class Slime(pygame.sprite.Sprite):
    def __init__(self, image_path):
        super().__init__()
        self.image = pygame.image.load(image_path).convert_alpha()
        self.original_image = self.image  # Store the original image for flipping
        self.rect = self.image.get_rect()
        self.spawn_within_screen()

        # Slime attributes
        self.hp = 10
        self.speed = 2
        self.direction = 'right'  # Initialize slime facing right

    def spawn_within_screen(self):
        """Spawn slime at a random position within the screen."""
        self.rect.x = random.randint(0, width - self.rect.width)
        self.rect.y = random.randint(0, height - self.rect.height)

    def move_towards_player(self, player):
        """Moves the slime towards the player."""
        direction_x = player.rect.x - self.rect.x
        direction_y = player.rect.y - self.rect.y
        distance = math.hypot(direction_x, direction_y)

        # Flip the slime based on its direction relative to the player
        if direction_x < 0 and self.direction != 'left':  # Moving left
            self.image = pygame.transform.flip(self.original_image, True, False)
            self.direction = 'left'
        elif direction_x > 0 and self.direction != 'right':  # Moving right
            self.image = self.original_image  # Restore original image
            self.direction = 'right'

        if distance > 0:  # Normalize direction
            direction_x /= distance
            direction_y /= distance

        # Move the slime towards the player
        self.rect.x += int(direction_x * self.speed)
        self.rect.y += int(direction_y * self.speed)


# Function to draw the XP bar and level text
def draw_xp_bar(screen, player):
    bar_width = 150
    bar_height = 15
    bar_x = 15
    bar_y = 15
    fill_width = int(bar_width * player.get_xp_progress())
    pygame.draw.rect(screen, gray, (bar_x, bar_y, bar_width, bar_height))
    pygame.draw.rect(screen, blue, (bar_x, bar_y, fill_width, bar_height))
    font = pygame.font.Font(None, 25)
    text = font.render(f'XP: {player.xp}/{player.xp_needed}', True, black)
    screen.blit(text, (bar_x, bar_y + bar_height + 5))
    text = font.render(f'Level: {player.level}', True, black)
    screen.blit(text, (bar_x, bar_y + bar_height + 20))


# Function to draw the HP bar and HP text
def draw_HP_bar(screen, player):
    bar_width = 150
    bar_height = 15
    bar_x = 15
    bar_y = 70
    fill_width = int(bar_width * (player.get_hp() / 100))
    pygame.draw.rect(screen, gray, (bar_x, bar_y, bar_width, bar_height))
    pygame.draw.rect(screen, red, (bar_x, bar_y, fill_width, bar_height))
    font = pygame.font.Font(None, 25)
    text = font.render(f'HP: {player.hp}', True, black)
    screen.blit(text, (bar_x, bar_y + bar_height + 5))


# Create the player instance
player = Player(640, 360, 'Pictures/Morp.png')

# Create sprite groups
all_sprites = pygame.sprite.Group()
all_sprites.add(player)

candies = pygame.sprite.Group()
slimes = pygame.sprite.Group()

# Timer to spawn candy every 15 seconds
candy_spawn_event = pygame.USEREVENT + 1
pygame.time.set_timer(candy_spawn_event, 5000)

# Timer to spawn slimes every # seconds
slime_spawn_event = pygame.USEREVENT + 2
pygame.time.set_timer(slime_spawn_event, 5000)

# Create a group for obstacles (currently empty, but you can add obstacles here)
obstacles = pygame.sprite.Group()

#Pause menu function ------------------------------------------------

# Initialize paused flag
paused = False  # Game starts in running state

# Define the pause menu function
def pause_menu():
    """Pause menu with a transparent background, title, resume, and quit buttons."""
    button_width = 150
    button_height = 40
    resume_button = pygame.Rect(width // 2 - button_width // 2, height // 2 - 50, button_width, button_height)
    quit_button = pygame.Rect(width // 2 - button_width // 2, height // 2 + 10, button_width, button_height)

    # Create a semi-transparent surface for the frosted effect
    transparent_surface = pygame.Surface((width, height), pygame.SRCALPHA)
    transparent_surface.fill((0, 0, 0, 128))  # Black with 50% transparency

    # Pause menu loop
    while True:
        # First, draw the game state underneath
        draw_game()

        # Draw the transparent overlay and pause menu on top of the current game state
        screen.blit(transparent_surface, (0, 0))  # Draw the transparent overlay

        font = pygame.font.Font(None, 36)
        title_font = pygame.font.Font(None, 48)  # Larger font for the title

        # Draw the title "Morp(1)"
        title_text = title_font.render('Morp(1)', True, black)
        title_rect = title_text.get_rect(center=(width // 2, height // 2 - 100))
        screen.blit(title_text, title_rect)

        # Draw the buttons (Resume and Quit)
        pygame.draw.rect(screen, green, resume_button)
        pygame.draw.rect(screen, red, quit_button)

        resume_text = font.render('Resume', True, black)
        quit_text = font.render('Quit', True, black)

        # Center the text within the buttons
        resume_text_rect = resume_text.get_rect(center=resume_button.center)
        quit_text_rect = quit_text.get_rect(center=quit_button.center)

        screen.blit(resume_text, resume_text_rect)
        screen.blit(quit_text, quit_text_rect)

        # Only one call to update the display
        pygame.display.flip()

        # Handle pause menu events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if resume_button.collidepoint(event.pos):
                    return False  # Resume the game
                if quit_button.collidepoint(event.pos):
                    pygame.quit()
                    sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    return False  # Resume the game if ESC is pressed


# Function to draw the game state (player, slimes, candies, etc.)
def draw_game():
    # Fill the screen with a background color (white in this case)
    screen.fill(white)

    # Draw the XP bar in the top-left corner of the screen
    draw_xp_bar(screen, player)

    # Draw the HP bar in the top-left corner of the screen
    draw_HP_bar(screen, player)

    # Draw the pause button
    screen.blit(pause_button, pause_button_rect)

    # Draw all sprites (this includes the player, candies, and slimes)
    all_sprites.draw(screen)

#---------------------------------------------------------------

# Main game loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        # Check if the ESC key is pressed to open the pause menu
        if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
            paused = True  # Trigger pause state

        # Check if the pause button is clicked
        if event.type == pygame.MOUSEBUTTONDOWN:
            if pause_button_rect.collidepoint(event.pos):
                paused = True  # Trigger pause state

        # Spawn a new candy every 5 seconds
        if event.type == candy_spawn_event:
            candy = Candy('Pictures/Candy.png')
            candies.add(candy)
            all_sprites.add(candy)

        # Spawn a new slime every # seconds
        if event.type == slime_spawn_event:
            slime = Slime('Pictures/Slime.png')
            slimes.add(slime)
            all_sprites.add(slime)

    # Pause menu logic
    if paused:
        paused = pause_menu()  # Show the pause menu and resume/quit options
    else:
        # Regular game update logic
        keys = pygame.key.get_pressed()

        # Update the player (pass in the keys, obstacles, candies, and slimes for collision detection)
        player.update(keys, obstacles, candies, slimes, width, height)

        # Move all slimes towards the player
        for slime in slimes:
            slime.move_towards_player(player)

        # Draw the game state
        draw_game()

        # Update the display
        pygame.display.flip()

        # Cap the frame rate to 60 FPS
        pygame.time.Clock().tick(60)

# Quit the game when the loop ends
pygame.quit()
sys.exit()


