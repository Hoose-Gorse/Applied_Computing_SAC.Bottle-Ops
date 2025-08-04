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
    GRAY = (128, 128, 128)
    
    # Safe font loading
    font = load_font(None, 48)
    
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
        
        # Add jump indicator
        if is_jumping:
            # Draw a small indicator showing the player is in "dodge mode"
            indicator_rect = pg.Rect(int(x + width//2 - 5), int(y - 10), 10, 5)
            pg.draw.rect(surface, GREEN, indicator_rect)
        
    except Exception as e:
        logging.error(f"Error drawing player with depth: {e}")
        # Fallback to simple rectangle
        player_rect = pg.Rect(int(x), int(y), width, height)
        pg.draw.rect(surface, WHITE, player_rect)

def safe_game_loop():
    """Main game loop with comprehensive error handling"""
    global player_x, player_y, vel_y, is_on_ground, drunk_x, drunk_direction, lives, last_bottle_time, bottles, start_time
    
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
                                            return False
                                        
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
                    life_text = font.render(f"Lives: {lives}", True, GREEN)
                    screen.blit(life_text, (20, 20))
                    
                    # Time survived on top-right
                    time_survived = (current_time - start_time) // 1000
                    minutes = time_survived // 60
                    seconds = time_survived % 60
                    time_text = font.render(f"Time: {minutes:02d}:{seconds:02d}", True, GREEN)
                    time_rect = time_text.get_rect()
                    screen.blit(time_text, (SCREEN_WIDTH - time_rect.width - 20, 20))
                    
                    # Debug info (optional - remove in final version)
                    active_bottles = len([b for b in bottles if b.active])
                    debug_text = font.render(f"Bottles: {active_bottles}", True, WHITE)
                    screen.blit(debug_text, (20, 80))
                    
                    # Jump status indicator
                    if not is_on_ground:
                        jump_text = font.render("DODGING!", True, GREEN)
                        jump_rect = jump_text.get_rect(center=(SCREEN_WIDTH // 2, 100))
                        screen.blit(jump_text, jump_rect)
                        
                except Exception as e:
                    logging.error(f"Error drawing HUD: {e}")
                
                # Event handling
                try:
                    for event in pg.event.get():
                        if event.type == pg.QUIT:
                            logging.info("User quit game")
                            return True
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
        timeout = 5000
        
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
