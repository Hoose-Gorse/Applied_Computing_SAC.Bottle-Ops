import pygame as pg
import random
from sys import exit
import logging
import traceback

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
    SCREEN_WIDTH, SCREEN_HEIGHT = 1280, 720
    screen = create_display(SCREEN_WIDTH, SCREEN_HEIGHT, "Bottle Ops")
    
    # Colors
    WHITE = (255, 255, 255)
    BLACK = (0, 0, 0)
    RED = (200, 0, 0)
    BLUE = (0, 100, 255)
    GREEN = (0, 255, 100)
    
    # Safe font loading
    font = load_font(None, 48)
    
    # Player constants
    player_width, player_height = 80, 100  # Increased from 50, 60
    player_x = SCREEN_WIDTH // 2
    player_speed = 6
    vel_y = 0
    gravity = 0.5
    jump_power = -12
    is_on_ground = False
    
    # Ground and player positioning
    ground_level = SCREEN_HEIGHT - 50
    player_base_y = ground_level - player_height  # Fixed base position
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
    start_time = pg.time.get_ticks()  # Track game start time
    bottle_spawn_time = 1000
    last_bottle_time = pg.time.get_ticks()
    bottles = []

except Exception as e:
    logging.error(f"Failed to initialize game: {e}")
    pg.quit()
    exit(1)

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
            self.z = 0.05  # Start very far away (smaller initial value)
            self.target_z = 1.0  # End close to player
            self.z_speed = 0.012  # Slightly faster z movement for better visibility
            
            # Calculate movement per frame
            self.total_frames = int((self.target_z - self.z) / self.z_speed)
            if self.total_frames > 0:
                self.dx = (self.target_x - self.start_x) / self.total_frames
                self.dy = (self.target_y - self.start_y) / self.total_frames
            else:
                self.dx = self.dy = 0
            
            # Visual properties (smaller bottles)
            self.base_width = 6  # Reduced from 8
            self.base_height = 18  # Reduced from 24
            self.rotation = 0
            self.rotation_speed = random.uniform(3, 8)
            
            # Create bottle surface
            self.original_image = pg.Surface((self.base_width, self.base_height), pg.SRCALPHA)
            self.original_image.fill(RED)
            
            self.active = True
            
        except Exception as e:
            logging.error(f"Failed to create bottle: {e}")
            self.active = False

    def update(self):
        """Update bottle position and state with error handling"""
        try:
            if not self.active:
                return True  # Remove inactive bottles
            
            # Move along z-axis (simulating depth)
            self.z += self.z_speed
            
            # Move towards target position
            self.x += self.dx
            self.y += self.dy
            
            # Update rotation
            self.rotation = (self.rotation + self.rotation_speed) % 360
            
            # Remove bottle if it has reached target z OR is off-screen
            if self.z >= self.target_z:
                return True
            
            # Check if bottle is completely off-screen (accounting for large size)
            scale_factor = (self.z ** 1.8) * 20
            scale_factor = max(scale_factor, 0.1)
            max_size = max(self.base_width, self.base_height) * scale_factor
            
            # Remove if bottle center is way off screen (considering its large size)
            if (self.x + max_size < -100 or self.x - max_size > SCREEN_WIDTH + 100 or
                self.y + max_size < -100 or self.y - max_size > SCREEN_HEIGHT + 100):
                return True
                
            return False
            
        except Exception as e:
            logging.error(f"Error updating bottle: {e}")
            return True  # Remove problematic bottles

    def draw(self, surface):
        """Draw bottle with perspective scaling and error handling"""
        try:
            if not self.active or self.z <= 0:
                return
            
            # Calculate size based on z-position (unlimited scaling for continuous growth)
            # Exponential growth that continues indefinitely
            scale_factor = (self.z ** 1.8) * 20  # Exponential growth for dramatic effect
            scale_factor = max(scale_factor, 0.1)  # Only minimum size when far away
            
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
            
            # Only draw if on screen (bottles continue growing beyond screen bounds)
            if (rect.right > 0 and rect.left < SCREEN_WIDTH and 
                rect.bottom > 0 and rect.top < SCREEN_HEIGHT):
                surface.blit(rotated_image, rect.topleft)
                
        except Exception as e:
            logging.error(f"Error drawing bottle: {e}")
            self.active = False

    def can_hit_player(self):
        """Check if bottle is close enough to hit player"""
        try:
            return self.active and self.z >= 0.7  # Slightly earlier hit detection
        except:
            return False

    def is_at_player_position(self):
        """Check if bottle has reached the player's z-position (ground level)"""
        try:
            return self.active and self.z >= 0.95  # Very close to player's position
        except:
            return False

    def get_collision_rect(self):
        """Get collision rectangle that's 20% smaller than visual representation"""
        try:
            if not self.active:
                return pg.Rect(0, 0, 0, 0)
            
            # Use exact same scaling and rotation logic as the visual drawing
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

def safe_game_loop():
    """Main game loop with comprehensive error handling"""
    global player_x, player_y, vel_y, is_on_ground, drunk_x, drunk_direction, lives, last_bottle_time, bottles, start_time
    
    running = True
    frame_count = 0
    
    try:
        while running:
            frame_count += 1
            
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
                
                # Draw player safely
                try:
                    player_rect = pg.Rect(int(player_x), int(player_y), player_width, player_height)
                    pg.draw.rect(screen, WHITE, player_rect)
                except Exception as e:
                    logging.error(f"Error drawing player: {e}")
                
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
                    current_time = pg.time.get_ticks()
                    if current_time - last_bottle_time > bottle_spawn_time:
                        # Always target the player's base position (ground level)
                        new_bottle = Bottle(
                            drunk_x + drunk_width // 2,  # Start at drunk guy
                            drunk_y + drunk_height,  # Start at bottom of drunk guy
                            player_x + player_width // 2,  # Target player's current x
                            player_base_y + player_height // 2  # Target base y position
                        )
                        if new_bottle.active:
                            bottles.append(new_bottle)
                        last_bottle_time = current_time
                except Exception as e:
                    logging.error(f"Error spawning bottle: {e}")
                
                # Update and draw bottles
                bottles_to_remove = []
                try:
                    for i, bottle in enumerate(bottles):
                        try:
                            if bottle.update():
                                bottles_to_remove.append(i)
                            else:
                                bottle.draw(screen)
                                
                                # Collision detection - only if bottle is at player's z-level
                                if (bottle.can_hit_player() and 
                                    bottle.is_at_player_position() and
                                    player_rect.colliderect(bottle.get_collision_rect())):
                                    lives -= 1
                                    bottles_to_remove.append(i)
                                    logging.info(f"Player hit! Lives remaining: {lives}")
                                    
                                    if lives <= 0:
                                        logging.info("Game over - no lives remaining")
                                        return False  # Game over
                                        
                        except Exception as e:
                            logging.error(f"Error with bottle {i}: {e}")
                            bottles_to_remove.append(i)
                    
                    # Remove bottles safely (reverse order to maintain indices)
                    for i in reversed(bottles_to_remove):
                        if 0 <= i < len(bottles):
                            bottles.pop(i)
                            
                except Exception as e:
                    logging.error(f"Error managing bottles: {e}")
                
                # HUD
                try:
                    # Lives on top-left
                    life_text = font.render(f"Lives: {lives}", True, GREEN)
                    screen.blit(life_text, (20, 20))
                    
                    # Time survived on top-right
                    current_time = pg.time.get_ticks()
                    time_survived = (current_time - start_time) // 1000  # Convert to seconds
                    minutes = time_survived // 60
                    seconds = time_survived % 60
                    time_text = font.render(f"Time: {minutes:02d}:{seconds:02d}", True, GREEN)
                    time_rect = time_text.get_rect()
                    screen.blit(time_text, (SCREEN_WIDTH - time_rect.width - 20, 20))
                        
                except Exception as e:
                    logging.error(f"Error drawing HUD: {e}")
                
                # Event handling
                try:
                    for event in pg.event.get():
                        if event.type == pg.QUIT:
                            logging.info("User quit game")
                            return True  # Clean exit
                        elif event.type == pg.KEYDOWN:
                            if event.key == pg.K_ESCAPE:
                                logging.info("User pressed escape")
                                return True
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
                # Continue running unless it's a critical error
                continue
                
    except KeyboardInterrupt:
        logging.info("Game interrupted by user")
        return True
    except Exception as e:
        logging.error(f"Critical error in game loop: {e}")
        logging.error(traceback.format_exc())
        return False

def show_game_over_screen(clean_exit=False):
    """Show game over screen with error handling"""
    try:
        screen.fill(BLACK)
        
        if clean_exit:
            message = "Thanks for playing!"
            color = GREEN
        else:
            message = "GAME OVER 💀"
            color = RED
            
        go_text = font.render(message, True, color)
        text_rect = go_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))
        screen.blit(go_text, text_rect)
        
        # Instructions
        inst_text = font.render("Press ESC to exit", True, WHITE)
        inst_rect = inst_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 60))
        screen.blit(inst_text, inst_rect)
        
        pg.display.flip()
        
        # Wait for input or timeout
        waiting = True
        start_time = pg.time.get_ticks()
        timeout = 5000  # 5 seconds
        
        while waiting and pg.time.get_ticks() - start_time < timeout:
            for event in pg.event.get():
                if event.type == pg.QUIT or (event.type == pg.KEYDOWN and event.key == pg.K_ESCAPE):
                    waiting = False
            pg.time.wait(100)
            
    except Exception as e:
        logging.error(f"Error showing game over screen: {e}")

# Main execution
if __name__ == "__main__":
    try:
        logging.info("Starting Bottle Ops game")
        clean_exit = safe_game_loop()
        show_game_over_screen(clean_exit)
        
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
