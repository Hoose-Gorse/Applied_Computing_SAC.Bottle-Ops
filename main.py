import pygame as pg
import random
from sys import exit
import logging
import traceback
import json
import os

# Configure logging for error handling
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('bottle_ops.log'),
        logging.StreamHandler()
    ]
)

def safe_init():
    """Safely initialize pygame with error handling"""
    try:
        pg.init()
        logging.info("Pygame initialized successfully")
        return True
    except Exception as e:
        logging.error(f"Failed to initialize pygame: {e}")
        return False

def create_display(width, height, caption):
    """Safely create display with error handling"""
    try:
        screen = pg.display.set_mode((width, height))
        pg.display.set_caption(caption)
        logging.info(f"Display created: {width}x{height}")
        return screen
    except Exception as e:
        logging.error(f"Failed to create display: {e}")
        raise

def load_font(font_name, size):
    """Safely load font with fallback"""
    try:
        return pg.font.SysFont(font_name, size)
    except Exception as e:
        logging.warning(f"Failed to load font {font_name}: {e}")
        try:
            return pg.font.Font(None, size)  # Fallback to default font
        except Exception as e2:
            logging.error(f"Failed to load fallback font: {e2}")
            raise

# Safe initialization
if not safe_init():
    exit(1)

try:
    clock = pg.time.Clock()
    
    # Get screen dimensions and create fullscreen display
    info = pg.display.Info()
    SCREEN_WIDTH = info.current_w
    SCREEN_HEIGHT = info.current_h
    screen = pg.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), pg.FULLSCREEN)
    pg.display.set_caption("Bottle Ops")
    logging.info(f"Fullscreen display created: {SCREEN_WIDTH}x{SCREEN_HEIGHT}")
    
    # Colors
    WHITE = (255, 255, 255)
    BLACK = (0, 0, 0)
    RED = (200, 0, 0)
    BLUE = (0, 100, 255)
    GREEN = (0, 255, 100)
    GRAY = (128, 128, 128)
    DARK_GRAY = (64, 64, 64)
    YELLOW = (255, 255, 0)
    
    # Safe font loading
    font_large = load_font(None, 72)
    font_medium = load_font(None, 48)
    font_small = load_font(None, 36)
    
    # Game settings
    is_fullscreen = True
    
    # Player constants with depth
    player_width, player_height = 80, 100
    player_x = SCREEN_WIDTH // 2
    player_speed = 6
    vel_y = 0
    gravity = 0.5
    jump_power = -12
    is_on_ground = False
    
    # Player depth properties - moved closer to drunk guy
    player_z_ground_start = 0.4  # Player z-space when on ground (0.4 to 0.6) - 2x closer
    player_z_ground_end = 0.6
    player_z_air_start = 0.2     # Player z-space when jumping (0.2 to 0.4) - 2x closer  
    player_z_air_end = 0.4
    player_collision_depth = 0.2  # Always 0.2 units of depth
    
    # Ground and player positioning
    ground_level = SCREEN_HEIGHT - 50
    player_base_y = ground_level - player_height
    player_y = player_base_y
    
    # Drunk guy
    drunk_width = 60
    drunk_height = 80
    drunk_x = SCREEN_WIDTH // 2
    drunk_speed = 3
    drunk_direction = 1
    drunk_y = 100
    
    # Game state
    lives = 9
    start_time = pg.time.get_ticks()
    bottle_spawn_time = 1000
    last_bottle_time = pg.time.get_ticks()
    bottles = []
    
    # Game states
    MENU = 0
    PLAYING = 1
    SETTINGS = 2
    LEADERBOARD = 3
    USERNAME_INPUT = 4
    GAME_OVER = 5
    
    current_state = MENU
    current_username = ""
    input_active = False
    final_score = 0

except Exception as e:
    logging.error(f"Failed to initialize game: {e}")
    pg.quit()
    exit(1)

class LeaderboardManager:
    def __init__(self, filename="leaderboard.json"):
        self.filename = filename
        self.scores = self.load_scores()
    
    def load_scores(self):
        """Load scores from file"""
        try:
            if os.path.exists(self.filename):
                with open(self.filename, 'r') as f:
                    data = json.load(f)
                    return data.get('scores', [])
            return []
        except Exception as e:
            logging.error(f"Error loading leaderboard: {e}")
            return []
    
    def save_scores(self):
        """Save scores to file"""
        try:
            with open(self.filename, 'w') as f:
                json.dump({'scores': self.scores}, f, indent=2)
        except Exception as e:
            logging.error(f"Error saving leaderboard: {e}")
    
    def add_score(self, username, score):
        """Add a new score to the leaderboard"""
        self.scores.append({'username': username, 'score': score})
        self.scores.sort(key=lambda x: x['score'], reverse=True)
        self.scores = self.scores[:10]  # Keep only top 10
        self.save_scores()
    
    def get_top_scores(self, limit=10):
        """Get top scores"""
        return self.scores[:limit]

class Button:
    def __init__(self, x, y, width, height, text, font, color=WHITE, hover_color=YELLOW):
        self.rect = pg.Rect(x, y, width, height)
        self.text = text
        self.font = font
        self.color = color
        self.hover_color = hover_color
        self.is_hovered = False
    
    def handle_event(self, event):
        if event.type == pg.MOUSEMOTION:
            self.is_hovered = self.rect.collidepoint(event.pos)
        elif event.type == pg.MOUSEBUTTONDOWN:
            if self.rect.collidepoint(event.pos):
                return True
        return False
    
    def draw(self, surface):
        color = self.hover_color if self.is_hovered else self.color
        pg.draw.rect(surface, DARK_GRAY, self.rect)
        pg.draw.rect(surface, color, self.rect, 3)
        
        text_surface = self.font.render(self.text, True, color)
        text_rect = text_surface.get_rect(center=self.rect.center)
        surface.blit(text_surface, text_rect)

class Bottle:
    def __init__(self, start_x, start_y, target_x, target_y):
        try:
            self.start_x = start_x
            self.start_y = start_y
            self.x = start_x
            self.y = start_y
            
            # Target is always the player's base position (ground level)
            self.target_x = target_x
            self.target_y = target_y
            
            # Z-axis properties for enhanced 3D effect
            self.z = 0.01  # Start far away
            self.target_z = 0.7  # Stop just past the player's ground position (0.4-0.6)
            self.z_speed = 0.008  # Adjusted speed for the new distance
            
            # Calculate movement per frame
            self.total_frames = int((self.target_z - self.z) / self.z_speed)
            if self.total_frames > 0:
                self.dx = (self.target_x - self.start_x) / self.total_frames
                self.dy = (self.target_y - self.start_y) / self.total_frames
            else:
                self.dx = self.dy = 0
            
            # Visual properties
            self.base_width = 6
            self.base_height = 18
            self.rotation = 0
            self.rotation_speed = random.uniform(3, 8)
            
            # Create bottle surface
            self.original_image = pg.Surface((self.base_width, self.base_height), pg.SRCALPHA)
            self.original_image.fill(RED)
            
            self.active = True
            self.hit_player = False  # Track if bottle hit player
            
        except Exception as e:
            logging.error(f"Failed to create bottle: {e}")
            self.active = False

    def update(self):
        """Update bottle position and state with error handling"""
        try:
            if not self.active:
                return True
            
            # Move along z-axis (simulating depth)
            self.z += self.z_speed
            
            # Move towards target position
            self.x += self.dx
            self.y += self.dy
            
            # Update rotation
            self.rotation = (self.rotation + self.rotation_speed) % 360
            
            # Remove bottle if it has gone past the target z
            if self.z >= self.target_z:
                return True
            
            # Check if bottle is completely off-screen
            scale_factor = (self.z ** 1.8) * 20
            scale_factor = max(scale_factor, 0.1)
            max_size = max(self.base_width, self.base_height) * scale_factor
            
            if (self.x + max_size < -100 or self.x - max_size > SCREEN_WIDTH + 100 or
                self.y + max_size < -100 or self.y - max_size > SCREEN_HEIGHT + 100):
                return True
                
            return False
            
        except Exception as e:
            logging.error(f"Error updating bottle: {e}")
            return True

    def draw(self, surface):
        """Draw bottle with perspective scaling and error handling"""
        try:
            if not self.active or self.z <= 0:
                return
            
            # Calculate size based on z-position
            scale_factor = (self.z ** 1.8) * 20
            scale_factor = max(scale_factor, 0.1)
            
            current_width = max(int(self.base_width * scale_factor), 1)
            current_height = max(int(self.base_height * scale_factor), 1)
            
            # Scale the original image
            scaled_image = pg.transform.scale(
                self.original_image, 
                (current_width, current_height)
            )
            
            # Rotate the scaled image
            rotated_image = pg.transform.rotate(scaled_image, self.rotation)
            
            # Position the bottle
            rect = rotated_image.get_rect(center=(int(self.x), int(self.y)))
            
            # Only draw if on screen
            if (rect.right > 0 and rect.left < SCREEN_WIDTH and 
                rect.bottom > 0 and rect.top < SCREEN_HEIGHT):
                surface.blit(rotated_image, rect.topleft)
                
        except Exception as e:
            logging.error(f"Error drawing bottle: {e}")
            self.active = False

    def is_in_player_collision_zone(self, player_is_jumping):
        """Check if bottle is within the player's current depth collision zone"""
        try:
            if not self.active:
                return False
            
            # Player has different z-positions when jumping vs on ground
            if player_is_jumping:
                return (self.z >= player_z_air_start and 
                        self.z <= player_z_air_end)
            else:
                return (self.z >= player_z_ground_start and 
                        self.z <= player_z_ground_end)
        except:
            return False

    def get_collision_rect(self, player_is_jumping):
        """Get collision rectangle for bottles in the player's depth zone"""
        try:
            if not self.active or not self.is_in_player_collision_zone(player_is_jumping):
                return pg.Rect(0, 0, 0, 0)
            
            # Use exact same scaling logic as visual drawing
            scale_factor = (self.z ** 1.8) * 20
            scale_factor = max(scale_factor, 0.1)
            
            current_width = max(int(self.base_width * scale_factor), 1)
            current_height = max(int(self.base_height * scale_factor), 1)
            
            # Make hitbox 20% smaller than visual representation
            hitbox_width = max(int(current_width * 0.8), 1)
            hitbox_height = max(int(current_height * 0.8), 1)
            
            # Center the smaller hitbox at the same position as the visual bottle
            return pg.Rect(
                int(self.x - hitbox_width // 2),
                int(self.y - hitbox_height // 2),
                hitbox_width,
                hitbox_height
            )
            
        except Exception as e:
            logging.error(f"Error getting collision rect: {e}")
            return pg.Rect(0, 0, 0, 0)

def draw_player_with_depth(surface, x, y, width, height, is_jumping):
    """Draw player with visual depth representation based on jumping state"""
    try:
        if is_jumping:
            # When jumping, player appears "behind" ground-level bottles
            # Use lighter colors to show they're in the background
            main_color = (200, 200, 200)  # Lighter white
            shadow_color = (100, 100, 100)  # Lighter gray
            shadow_offset = 2  # Smaller shadow when in back
        else:
            # When on ground, player appears "in front" 
            main_color = WHITE
            shadow_color = GRAY
            shadow_offset = 3
        
        # Main player body
        player_rect = pg.Rect(int(x), int(y), width, height)
        
        # Add depth shadow/outline
        shadow_rect = pg.Rect(int(x + shadow_offset), int(y + shadow_offset), width, height)
        pg.draw.rect(surface, shadow_color, shadow_rect)
        
        # Draw main body on top
        pg.draw.rect(surface, main_color, player_rect)
        
        # Add depth indicator lines
        pg.draw.line(surface, shadow_color, (int(x), int(y)), (int(x + shadow_offset), int(y + shadow_offset)), 2)
        pg.draw.line(surface, shadow_color, (int(x + width), int(y)), (int(x + width + shadow_offset), int(y + shadow_offset)), 2)
        
    except Exception as e:
        logging.error(f"Error drawing player with depth: {e}")
        # Fallback to simple rectangle
        player_rect = pg.Rect(int(x), int(y), width, height)
        pg.draw.rect(surface, WHITE, player_rect)

def reset_game():
    """Reset all game variables for a new game"""
    global player_x, player_y, vel_y, is_on_ground, drunk_x, drunk_direction, lives, start_time, last_bottle_time, bottles
    
    player_x = SCREEN_WIDTH // 2
    player_y = player_base_y
    vel_y = 0
    is_on_ground = False
    drunk_x = SCREEN_WIDTH // 2
    drunk_direction = 1
    lives = 9
    start_time = pg.time.get_ticks()
    last_bottle_time = pg.time.get_ticks()
    bottles = []

def show_menu():
    """Display the main menu"""
    screen.fill(BLACK)
    
    # Title
    title_text = font_large.render("BOTTLE OPS", True, WHITE)
    title_rect = title_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 4))
    screen.blit(title_text, title_rect)
    
    # Buttons
    button_width = 300
    button_height = 60
    button_x = SCREEN_WIDTH // 2 - button_width // 2
    
    play_button = Button(button_x, SCREEN_HEIGHT // 2 - 100, button_width, button_height, "PLAY", font_medium)
    settings_button = Button(button_x, SCREEN_HEIGHT // 2 - 20, button_width, button_height, "SETTINGS", font_medium)
    leaderboard_button = Button(button_x, SCREEN_HEIGHT // 2 + 60, button_width, button_height, "LEADERBOARD", font_medium)
    exit_button = Button(button_x, SCREEN_HEIGHT // 2 + 140, button_width, button_height, "EXIT", font_medium)
    
    play_button.draw(screen)
    settings_button.draw(screen)
    leaderboard_button.draw(screen)
    exit_button.draw(screen)
    
    return play_button, settings_button, leaderboard_button, exit_button

def show_settings():
    """Display the settings menu"""
    screen.fill(BLACK)
    
    # Title
    title_text = font_large.render("SETTINGS", True, WHITE)
    title_rect = title_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 4))
    screen.blit(title_text, title_rect)
    
    # Fullscreen toggle
    fullscreen_text = "Fullscreen: ON" if is_fullscreen else "Fullscreen: OFF"
    fs_button = Button(SCREEN_WIDTH // 2 - 200, SCREEN_HEIGHT // 2 - 50, 400, 60, fullscreen_text, font_medium)
    fs_button.draw(screen)
    
    # Back button
    back_button = Button(SCREEN_WIDTH // 2 - 150, SCREEN_HEIGHT // 2 + 50, 300, 60, "BACK", font_medium)
    back_button.draw(screen)
    
    return fs_button, back_button

def show_leaderboard():
    """Display the leaderboard"""
    screen.fill(BLACK)
    
    # Title
    title_text = font_large.render("LEADERBOARD", True, WHITE)
    title_rect = title_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 6))
    screen.blit(title_text, title_rect)
    
    # Get scores
    scores = leaderboard.get_top_scores()
    
    # Display scores
    y_offset = SCREEN_HEIGHT // 4
    for i, score_data in enumerate(scores):
        username = score_data['username']
        score = score_data['score']
        minutes = score // 60
        seconds = score % 60
        
        rank_text = f"{i+1}. {username} - {minutes:02d}:{seconds:02d}"
        color = YELLOW if i == 0 else WHITE
        
        score_surface = font_small.render(rank_text, True, color)
        score_rect = score_surface.get_rect(center=(SCREEN_WIDTH // 2, y_offset + i * 40))
        screen.blit(score_surface, score_rect)
    
    # Back button
    back_button = Button(SCREEN_WIDTH // 2 - 150, SCREEN_HEIGHT - 150, 300, 60, "BACK", font_medium)
    back_button.draw(screen)
    
    return back_button

def show_username_input():
    """Display username input screen"""
    screen.fill(BLACK)
    
    # Title
    title_text = font_large.render("ENTER USERNAME", True, WHITE)
    title_rect = title_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 3))
    screen.blit(title_text, title_rect)
    
    # Input box
    input_box = pg.Rect(SCREEN_WIDTH // 2 - 200, SCREEN_HEIGHT // 2 - 30, 400, 60)
    color = WHITE if input_active else GRAY
    pg.draw.rect(screen, color, input_box, 3)
    
    # Username text
    username_surface = font_medium.render(current_username, True, WHITE)
    screen.blit(username_surface, (input_box.x + 10, input_box.y + 15))
    
    # Instructions
    inst_text = font_small.render("Press ENTER to continue", True, GRAY)
    inst_rect = inst_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 60))
    screen.blit(inst_text, inst_rect)
    
    return input_box

def show_game_over_screen():
    """Display game over screen"""
    screen.fill(BLACK)
    
    # Game Over text
    go_text = font_large.render("GAME OVER", True, RED)
    go_rect = go_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 3))
    screen.blit(go_text, go_rect)
    
    # Final score
    minutes = final_score // 60
    seconds = final_score % 60
    score_text = font_medium.render(f"Final Time: {minutes:02d}:{seconds:02d}", True, WHITE)
    score_rect = score_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))
    screen.blit(score_text, score_rect)
    
    # Continue button
    continue_button = Button(SCREEN_WIDTH // 2 - 150, SCREEN_HEIGHT // 2 + 80, 300, 60, "CONTINUE", font_medium)
    continue_button.draw(screen)
    
    return continue_button

def safe_game_loop():
    """Main game loop with comprehensive error handling"""
    global player_x, player_y, vel_y, is_on_ground, drunk_x, drunk_direction, lives, last_bottle_time, bottles, start_time, screen
    
    running = True
    frame_count = 0
    
    try:
        while running:
            frame_count += 1
            current_time = pg.time.get_ticks()
            
            try:
                screen.fill(BLACK)
                keys = pg.key.get_pressed()
                
                # Player movement with bounds checking
                try:
                    if keys[pg.K_LEFT] or keys[pg.K_a]:
                        player_x = max(0, player_x - player_speed)
                    if keys[pg.K_RIGHT] or keys[pg.K_d]:
                        player_x = min(SCREEN_WIDTH - player_width, player_x + player_speed)
                    
                    # Jumping
                    if (keys[pg.K_SPACE] or keys[pg.K_w] or keys[pg.K_UP]) and is_on_ground:
                        vel_y = jump_power
                        is_on_ground = False
                    
                    # Physics
                    vel_y += gravity
                    player_y += vel_y
                    
                    # Ground collision
                    if player_y >= player_base_y:
                        player_y = player_base_y
                        vel_y = 0
                        is_on_ground = True
                        
                except Exception as e:
                    logging.error(f"Error in player movement: {e}")
                
                # Drunk guy movement
                try:
                    drunk_x += drunk_speed * drunk_direction
                    if drunk_x <= 0 or drunk_x >= SCREEN_WIDTH - drunk_width:
                        drunk_direction *= -1
                        drunk_x = max(0, min(drunk_x, SCREEN_WIDTH - drunk_width))
                    
                    drunk_rect = pg.Rect(int(drunk_x), drunk_y, drunk_width, drunk_height)
                    pg.draw.rect(screen, BLUE, drunk_rect)
                except Exception as e:
                    logging.error(f"Error with drunk guy: {e}")
                
                # Bottle spawning
                try:
                    if current_time - last_bottle_time > bottle_spawn_time:
                        new_bottle = Bottle(
                            drunk_x + drunk_width // 2,
                            drunk_y + drunk_height,
                            player_x + player_width // 2,
                            player_base_y + player_height // 2
                        )
                        if new_bottle.active:
                            bottles.append(new_bottle)
                        last_bottle_time = current_time
                except Exception as e:
                    logging.error(f"Error spawning bottle: {e}")
                
                # Update bottles and separate by layer
                bottles_to_remove = []
                bottles_behind = []
                bottles_in_front = []
                
                try:
                    for i, bottle in enumerate(bottles):
                        try:
                            if bottle.update():
                                bottles_to_remove.append(i)
                            elif bottle.hit_player:
                                # Remove bottles that have hit the player
                                bottles_to_remove.append(i)
                            else:
                                # Determine current player z-range based on jumping state
                                if is_on_ground:
                                    current_player_z_start = player_z_ground_start
                                    current_player_z_end = player_z_ground_end
                                else:
                                    current_player_z_start = player_z_air_start
                                    current_player_z_end = player_z_air_end
                                
                                # Separate bottles by z-position for proper layering
                                if bottle.z < current_player_z_start:
                                    bottles_behind.append(bottle)
                                elif bottle.z > current_player_z_end:
                                    bottles_in_front.append(bottle)
                                else:
                                    # Bottle is in player's current z-space - potential collision
                                    bottles_in_front.append(bottle)  # Draw in front for visibility
                                
                                # Enhanced collision detection with jumping dodge mechanic
                                if bottle.is_in_player_collision_zone(not is_on_ground):
                                    player_rect = pg.Rect(int(player_x), int(player_y), player_width, player_height)
                                    bottle_collision_rect = bottle.get_collision_rect(not is_on_ground)
                                    
                                    if (bottle_collision_rect.width > 0 and bottle_collision_rect.height > 0 and
                                        player_rect.colliderect(bottle_collision_rect)):
                                        lives -= 1
                                        bottle.hit_player = True  # Mark for removal
                                        bottles_to_remove.append(i)
                                        jump_status = "jumping" if not is_on_ground else "on ground"
                                        player_z = f"{current_player_z_start:.1f}-{current_player_z_end:.1f}"
                                        logging.info(f"Player hit while {jump_status} (z={player_z}) by bottle at z={bottle.z:.3f}! Lives remaining: {lives}")
                                        
                                        if lives <= 0:
                                            logging.info("Game over - no lives remaining")
                                            return current_time - start_time  # Return survival time
                                        
                        except Exception as e:
                            logging.error(f"Error with bottle {i}: {e}")
                            bottles_to_remove.append(i)
                    
                    # Remove bottles safely (reverse order to maintain indices)
                    for i in reversed(sorted(set(bottles_to_remove))):
                        if 0 <= i < len(bottles):
                            bottles.pop(i)
                            
                except Exception as e:
                    logging.error(f"Error managing bottles: {e}")
                
                # Draw ALL bottles first (behind player)
                try:
                    for bottle in bottles_behind:
                        bottle.draw(screen)
                    for bottle in bottles_in_front:
                        bottle.draw(screen)
                except Exception as e:
                    logging.error(f"Error drawing bottles: {e}")
                
                # Draw player LAST - ALWAYS ON TOP OF EVERYTHING
                try:
                    draw_player_with_depth(screen, player_x, player_y, player_width, player_height, not is_on_ground)
                except Exception as e:
                    logging.error(f"Error drawing player: {e}")
                
                # HUD
                try:
                    # Lives on top-left
                    life_text = font_medium.render(f"Lives: {lives}", True, GREEN)
                    screen.blit(life_text, (20, 20))
                    
                    # Time survived on top-right
                    time_survived = (current_time - start_time) // 1000
                    minutes = time_survived // 60
                    seconds = time_survived % 60
                    time_text = font_medium.render(f"Time: {minutes:02d}:{seconds:02d}", True, GREEN)
                    time_rect = time_text.get_rect()
                    screen.blit(time_text, (SCREEN_WIDTH - time_rect.width - 20, 20))
                        
                except Exception as e:
                    logging.error(f"Error drawing HUD: {e}")
                
                # Event handling
                try:
                    for event in pg.event.get():
                        if event.type == pg.QUIT:
                            logging.info("User quit game")
                            return -1  # Special return code for quit
                        elif event.type == pg.KEYDOWN:
                            if event.key == pg.K_ESCAPE:
                                logging.info("User pressed escape")
                                return -1  # Return to menu
                except Exception as e:
                    logging.error(f"Error handling events: {e}")
                
                # Update display
                try:
                    pg.display.flip()
                    clock.tick(60)
                except Exception as e:
                    logging.error(f"Error updating display: {e}")
                    
            except Exception as e:
                logging.error(f"Error in main game loop: {e}")
                continue
                
    except KeyboardInterrupt:
        logging.info("Game interrupted by user")
        return -1
    except Exception as e:
        logging.error(f"Critical error in game loop: {e}")
        logging.error(traceback.format_exc())
        return -1

def main():
    """Main game function with menu system"""
    global current_state, current_username, input_active, final_score, is_fullscreen, screen, leaderboard
    
    leaderboard = LeaderboardManager()
    
    try:
        while True:
            if current_state == MENU:
                play_btn, settings_btn, leaderboard_btn, exit_btn = show_menu()
                
                for event in pg.event.get():
                    if event.type == pg.QUIT:
                        return
                    elif event.type == pg.KEYDOWN:
                        if event.key == pg.K_ESCAPE:
                            return
                    
                    # Handle button clicks
                    play_btn.handle_event(event)
                    settings_btn.handle_event(event)
                    leaderboard_btn.handle_event(event)
                    exit_btn.handle_event(event)
                    
                    if play_btn.handle_event(event):
                        current_state = USERNAME_INPUT
                        current_username = ""
                        input_active = True
                    elif settings_btn.handle_event(event):
                        current_state = SETTINGS
                    elif leaderboard_btn.handle_event(event):
                        current_state = LEADERBOARD
                    elif exit_btn.handle_event(event):
                        return
            
            elif current_state == USERNAME_INPUT:
                input_box = show_username_input()
                
                for event in pg.event.get():
                    if event.type == pg.QUIT:
                        return
                    elif event.type == pg.KEYDOWN:
                        if event.key == pg.K_ESCAPE:
                            current_state = MENU
                        elif event.key == pg.K_RETURN:
                            if current_username.strip():
                                reset_game()
                                current_state = PLAYING
                        elif event.key == pg.K_BACKSPACE:
                            current_username = current_username[:-1]
                        else:
                            if len(current_username) < 15 and event.unicode.isprintable():
                                current_username += event.unicode
                    elif event.type == pg.MOUSEBUTTONDOWN:
                        input_active = input_box.collidepoint(event.pos)
            
            elif current_state == PLAYING:
                survival_time = safe_game_loop()
                if survival_time == -1:  # User quit or escaped
                    current_state = MENU
                else:
                    final_score = survival_time // 1000  # Convert to seconds
                    leaderboard.add_score(current_username, final_score)
                    current_state = GAME_OVER
            
            elif current_state == SETTINGS:
                fs_btn, back_btn = show_settings()
                
                for event in pg.event.get():
                    if event.type == pg.QUIT:
                        return
                    elif event.type == pg.KEYDOWN:
                        if event.key == pg.K_ESCAPE:
                            current_state = MENU
                    
                    fs_btn.handle_event(event)
                    back_btn.handle_event(event)
                    
                    if fs_btn.handle_event(event):
                        # Toggle fullscreen
                        try:
                            is_fullscreen = not is_fullscreen
                            if is_fullscreen:
                                screen = pg.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), pg.FULLSCREEN)
                                logging.info("Switched to fullscreen mode")
                            else:
                                screen = pg.display.set_mode((1280, 720))
                                logging.info("Switched to windowed mode")
                        except Exception as e:
                            logging.error(f"Error toggling fullscreen: {e}")
                    elif back_btn.handle_event(event):
                        current_state = MENU
            
            elif current_state == LEADERBOARD:
                back_btn = show_leaderboard()
                
                for event in pg.event.get():
                    if event.type == pg.QUIT:
                        return
                    elif event.type == pg.KEYDOWN:
                        if event.key == pg.K_ESCAPE:
                            current_state = MENU
                    
                    back_btn.handle_event(event)
                    
                    if back_btn.handle_event(event):
                        current_state = MENU
            
            elif current_state == GAME_OVER:
                continue_btn = show_game_over_screen()
                
                for event in pg.event.get():
                    if event.type == pg.QUIT:
                        return
                    elif event.type == pg.KEYDOWN:
                        if event.key == pg.K_ESCAPE or event.key == pg.K_RETURN:
                            current_state = MENU
                    
                    continue_btn.handle_event(event)
                    
                    if continue_btn.handle_event(event):
                        current_state = MENU
            
            pg.display.flip()
            clock.tick(60)
            
    except Exception as e:
        logging.error(f"Error in main loop: {e}")
        logging.error(traceback.format_exc())
    finally:
        try:
            pg.quit()
            logging.info("Game shut down successfully")
        except:
            pass

# Main execution
if __name__ == "__main__":
    try:
        logging.info("Starting Bottle Ops game")
        main()
        
    except Exception as e:
        logging.error(f"Fatal error: {e}")
        logging.error(traceback.format_exc())
        
    finally:
        try:
            pg.quit()
            logging.info("Game shut down successfully")
        except:
            pass
        exit(0)
