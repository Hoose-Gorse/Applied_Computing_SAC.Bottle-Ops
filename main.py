import pygame as pg
import random
from sys import exit
import logging
import json
import os
import math

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

def update_screen_dimensions(new_width, new_height):
    """Update all screen-dependent variables when screen size changes"""
    global SCREEN_WIDTH, SCREEN_HEIGHT, WINDOWED_WIDTH, WINDOWED_HEIGHT, screen, font_large, font_medium, font_small
    global is_fullscreen, fade_surface
    
    SCREEN_WIDTH = new_width
    SCREEN_HEIGHT = new_height
    
    # If we're not in fullscreen, also update the windowed dimensions
    if not is_fullscreen:
        WINDOWED_WIDTH = new_width
        WINDOWED_HEIGHT = new_height
    
    # Update the display mode
    if is_fullscreen:
        screen = pg.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), pg.FULLSCREEN)
    else:
        screen = pg.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), pg.RESIZABLE)
    
    # Update fonts for new screen size
    font_large, font_medium, font_small = get_scaled_fonts()
    
    # Update all scaled game values
    get_scaled_values()
    
    # Update fade surface for new screen size
    fade_surface = pg.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
    fade_surface.fill(BLACK)
    
    # Update scrollbar if it exists
    if 'scrollbar' in globals():
        recalculate_scrollbar()
    
    logging.info(f"Screen dimensions updated to: {SCREEN_WIDTH}x{SCREEN_HEIGHT}")

def toggle_fullscreen():
    """Toggle fullscreen mode safely"""
    global is_fullscreen, screen, SCREEN_WIDTH, SCREEN_HEIGHT, WINDOWED_WIDTH, WINDOWED_HEIGHT
    global font_large, font_medium, font_small, fade_surface
    
    try:
        if is_fullscreen:
            # Switch to windowed mode - restore previous windowed size
            is_fullscreen = False
            SCREEN_WIDTH = WINDOWED_WIDTH
            SCREEN_HEIGHT = WINDOWED_HEIGHT
            screen = pg.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), pg.RESIZABLE)
            logging.info(f"Switched to windowed mode: {SCREEN_WIDTH}x{SCREEN_HEIGHT}")
        else:
            # Switch to fullscreen mode - save current windowed size first
            WINDOWED_WIDTH = SCREEN_WIDTH
            WINDOWED_HEIGHT = SCREEN_HEIGHT
            is_fullscreen = True
            SCREEN_WIDTH = FULL_WIDTH
            SCREEN_HEIGHT = FULL_HEIGHT
            screen = pg.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), pg.FULLSCREEN)
            logging.info(f"Switched to fullscreen mode: {SCREEN_WIDTH}x{SCREEN_HEIGHT}")
        
        # Update fonts for new screen size
        font_large, font_medium, font_small = get_scaled_fonts()
        
        # Update all scaled game values
        get_scaled_values()
        
        # Update fade surface for new screen size
        fade_surface = pg.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
        fade_surface.fill(BLACK)
        
        # Update scrollbar if it exists
        if 'scrollbar' in globals():
            recalculate_scrollbar()
            
        return True
        
    except Exception as e:
        logging.error(f"Error toggling fullscreen: {e}")
        # Revert the fullscreen flag if we failed
        is_fullscreen = not is_fullscreen
        return False

# Safe initialization
if not safe_init():
    exit(1)

try:
    clock = pg.time.Clock()
    
    # Get full screen info for reference
    info = pg.display.Info()
    FULL_WIDTH = info.current_w
    FULL_HEIGHT = info.current_h
    
    # Base dimensions (reference resolution for scaling)
    BASE_WIDTH = 960  # Fixed reference width
    BASE_HEIGHT = 540  # Fixed reference height (16:9 aspect ratio)
    
    # Current screen dimensions (will change with window resizing)
    SCREEN_WIDTH = BASE_WIDTH
    SCREEN_HEIGHT = BASE_HEIGHT
    
    # Store the windowed mode dimensions separately from current dimensions
    WINDOWED_WIDTH = BASE_WIDTH
    WINDOWED_HEIGHT = BASE_HEIGHT
    
    # Game settings
    is_fullscreen = True  # Start in fullscreen mode
    
    # Create windowed display (not fullscreen)
    if is_fullscreen:
        screen = pg.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), pg.FULLSCREEN | pg.SCALED)
    else:
        screen = pg.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), pg.RESIZABLE)
    
    pg.display.set_caption("Bottle Ops")
    logging.info(f"Initial display created: {SCREEN_WIDTH}x{SCREEN_HEIGHT}")
    
    # Colors
    WHITE = (255, 255, 255)
    BLACK = (0, 0, 0)
    RED = (200, 0, 0)
    BLUE = (0, 100, 255)
    GREEN = (0, 255, 100)
    GRAY = (128, 128, 128)
    DARK_GRAY = (64, 64, 64)
    YELLOW = (255, 255, 0)
    LIGHT_GRAY = (200, 200, 200)
    ORANGE = (255, 165, 0)
    PURPLE = (128, 0, 128)
    
    # Fade transition variables
    fade_surface = pg.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
    fade_surface.fill(BLACK)
    fade_alpha = 0
    fade_direction = 0  # 0 = no fade, 1 = fade out, -1 = fade in
    fade_speed = 8  # Alpha change per frame
    next_state = None  # State to transition to after fade out
    
    # Base font sizes (for reference resolution)
    base_font_large = 48
    base_font_medium = 32
    base_font_small = 24
    
    # Dynamic font loading function
    def get_scaled_fonts():
        # Calculate scale based on current screen size vs base resolution
        scale_x = SCREEN_WIDTH / BASE_WIDTH
        scale_y = SCREEN_HEIGHT / BASE_HEIGHT
        scale = min(scale_x, scale_y)  # Use minimum to maintain aspect ratio
        
        return (
            load_font(None, max(12, int(base_font_large * scale))),
            load_font(None, max(10, int(base_font_medium * scale))),
            load_font(None, max(8, int(base_font_small * scale)))
        )
    
    # Initialize fonts 
    font_large, font_medium, font_small = get_scaled_fonts()
    
    # Base dimensions and speeds (proportional to BASE_WIDTH/BASE_HEIGHT)
    def get_scaled_values():
        global player_width, player_height, player_x, player_speed, vel_y, gravity, jump_power
        global ground_level, player_base_y, player_y, drunk_width, drunk_height, drunk_x, drunk_speed, drunk_y
        
        # Calculate scale based on current screen size vs base resolution
        scale_x = SCREEN_WIDTH / BASE_WIDTH
        scale_y = SCREEN_HEIGHT / BASE_HEIGHT
        
        # Player constants - scaled proportionally
        player_width = max(10, int(60 * scale_x))
        player_height = max(10, int(75 * scale_y))
        player_x = SCREEN_WIDTH // 2 - player_width // 2
        player_speed = max(1, int(5 * scale_x))
        vel_y = 0
        gravity = 0.5 * scale_y
        jump_power = -12 * scale_y
        
        # Ground and player positioning
        ground_level = SCREEN_HEIGHT - max(10, int(40 * scale_y))
        player_base_y = ground_level - player_height
        player_y = player_base_y
        
        # Drunk guy - scaled proportionally (no movement needed)
        drunk_width = max(8, int(45 * scale_x))
        drunk_height = max(8, int(60 * scale_y))
        drunk_x = SCREEN_WIDTH // 2 - drunk_width // 2  # Center horizontally
        drunk_y = max(10, int(80 * scale_y))
    
    # Initialize scaled values
    get_scaled_values()
    
    # Player depth properties (these remain constant as they're ratios)
    player_z_ground_start = 0.45  # Player z-space when on ground (0.4 to 0.6)
    player_z_ground_end = 0.5
    player_z_air_start = 0.45     # Player z-space when jumping (0.2 to 0.4)
    player_z_air_end = 0.5
    player_collision_depth = 0.1  # Always 0.2 units of depth
    
    is_on_ground = False
    
    # Enhanced scoring system variables
    score = 0
    bottles_dodged = 0
    close_calls = 0
    combo_multiplier = 1.0
    
    # Scoring constants
    BASE_DODGE_SCORE = 10
    CLOSE_CALL_SCORE = 25
    CLOSE_CALL_DISTANCE = 100  # Pixels for close call detection
    COMBO_INCREMENT = 0.2  # How much combo increases per consecutive dodge
    MAX_COMBO = 5.0  # Maximum combo multiplier
    
    # Visual feedback for scoring
    score_popups = []  # List of score popup effects
    
    # Game state
    lives = 9
    start_time = pg.time.get_ticks()
    bottle_spawn_time = 1000  # Starting spawn time for right hand
    left_hand_spawn_time = 1500  # Left hand spawns slower
    last_bottle_time = pg.time.get_ticks()
    last_left_bottle_time = pg.time.get_ticks()
    bottles = []
    
    # Dual hand system
    next_bottle_preview = None  # Right hand preview
    next_bottle_show_time = 0
    next_bottle_throw_delay = 1000
    
    next_left_bottle_preview = None  # Left hand preview
    next_left_bottle_show_time = 0
    next_left_bottle_throw_delay = 1000
    
    current_throwing_hand = "right"  # Track which hand throws next
    
    # Difficulty progression constants
    MIN_SPAWN_TIME = 200  # Minimum time between bottles (0.2 seconds at 60fps)
    MIN_LEFT_SPAWN_TIME = 400  # Left hand minimum spawn time (slower)
    DIFFICULTY_INCREASE_INTERVAL = 500  # Points needed to increase difficulty
    
    # Leaderboard scrolling
    leaderboard_scroll = 0
    max_visible_scores = 8  # How many scores to show at once
    scrollbar_dragging = False
    scroll_drag_offset = 0
    
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

def get_current_difficulty():
    """Calculate current difficulty based on score"""
    difficulty_level = score // DIFFICULTY_INCREASE_INTERVAL
    # Calculate spawn time: start at 1000ms, decrease by 80ms per level, min 200ms
    current_spawn_time = max(MIN_SPAWN_TIME, 1000 - (difficulty_level * 80))
    # Left hand spawn time (always slower)
    left_spawn_time = max(MIN_LEFT_SPAWN_TIME, 1500 - (difficulty_level * 60))
    return current_spawn_time, left_spawn_time

def start_fade_transition(target_state):
    """Start a fade out transition to a target state"""
    global fade_direction, next_state, fade_alpha
    fade_direction = 1  # Start fade out
    next_state = target_state
    fade_alpha = 0

def update_fade():
    """Update fade transition and return True if transition is complete"""
    global fade_alpha, fade_direction, current_state, next_state
    
    if fade_direction == 0:
        return True  # No fade in progress
    
    if fade_direction == 1:  # Fading out
        fade_alpha += fade_speed
        if fade_alpha >= 255:
            fade_alpha = 255
            # Switch to target state and start fading in
            current_state = next_state
            next_state = None
            fade_direction = -1
    
    elif fade_direction == -1:  # Fading in
        fade_alpha -= fade_speed
        if fade_alpha <= 0:
            fade_alpha = 0
            fade_direction = 0  # Fade complete
            return True
    
    return False

def draw_fade():
    """Draw the fade overlay"""
    if fade_direction != 0 and fade_alpha > 0:
        fade_surface.set_alpha(fade_alpha)
        screen.blit(fade_surface, (0, 0))

class ScorePopup:
    """Visual feedback for scoring events"""
    def __init__(self, x, y, text, color, font):
        self.x = x
        self.y = y
        self.text = text
        self.color = color
        self.font = font
        self.alpha = 255
        self.timer = 0
        self.max_time = 90  # 1.5 seconds at 60 FPS
        self.y_offset = 0
        
    def update(self):
        """Update popup animation"""
        self.timer += 1
        self.y_offset -= 1  # Float upward
        
        # Fade out
        progress = self.timer / self.max_time
        self.alpha = int(255 * (1 - progress))
        
        return self.timer >= self.max_time  # Return True when done
    
    def draw(self, surface):
        """Draw the popup"""
        if self.alpha <= 0:
            return
            
        text_surface = self.font.render(self.text, True, self.color)
        text_surface.set_alpha(self.alpha)
        
        surface.blit(text_surface, (self.x, self.y + self.y_offset))

def add_score_popup(x, y, points, is_close_call=False, combo_mult=1.0):
    """Add a visual score popup"""
    global score_popups
    
    # Determine popup text and color
    if is_close_call:
        text = f"CLOSE CALL! +{points}"
        color = ORANGE
    elif combo_mult > 1.0:
        text = f"+{points} (x{combo_mult:.1f})"
        color = PURPLE
    else:
        text = f"+{points}"
        color = GREEN
    
    popup = ScorePopup(x, y, text, color, font_small)
    score_popups.append(popup)

def update_score_popups():
    """Update all score popups and remove finished ones"""
    global score_popups
    score_popups = [popup for popup in score_popups if not popup.update()]

def draw_score_popups(surface):
    """Draw all active score popups"""
    for popup in score_popups:
        popup.draw(surface)

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
        # No longer limiting to top 10 - keep all scores
        self.save_scores()
    
    def get_all_scores(self):
        """Get all scores"""
        return self.scores
    
    def get_top_scores(self, limit=10):
        """Get top scores"""
        return self.scores[:limit]
    
    def clear_all_scores(self):
        """Clear all scores from leaderboard"""
        self.scores = []
        self.save_scores()

class ScrollBar:
    def __init__(self, x, y, width, height, total_items, visible_items):
        self.rect = pg.Rect(x, y, width, height)
        self.total_items = total_items
        self.visible_items = visible_items
        self.scroll_position = 0
        self.dragging = False
        self.drag_offset = 0
        
        # Calculate thumb properties
        self.update_thumb()
    
    def update_thumb(self):
        """Update thumb size and position based on scroll state"""
        if self.total_items <= self.visible_items:
            # No scrolling needed - hide scrollbar
            self.thumb_height = 0
            self.thumb_y = self.rect.y
            self.max_scroll = 0
        else:
            # Calculate thumb size as proportion of visible area
            scroll_ratio = self.visible_items / self.total_items
            self.thumb_height = max(20, int(self.rect.height * scroll_ratio))
            
            # Calculate maximum scroll positions
            self.max_scroll = self.total_items - self.visible_items
            self.max_thumb_y = self.rect.bottom - self.thumb_height
            
            # Calculate thumb position based on scroll
            if self.max_scroll > 0:
                scroll_progress = self.scroll_position / self.max_scroll
                self.thumb_y = self.rect.y + int((self.rect.height - self.thumb_height) * scroll_progress)
            else:
                self.thumb_y = self.rect.y
    
    def get_thumb_rect(self):
        """Get the rectangle for the scroll thumb"""
        return pg.Rect(self.rect.x, self.thumb_y, self.rect.width, self.thumb_height)
    
    def handle_event(self, event):
        """Handle mouse events for scrollbar interaction"""
        if self.thumb_height == 0:  # No scrolling needed
            return False
            
        if event.type == pg.MOUSEBUTTONDOWN:
            if event.button == 1:  # Left click
                mouse_x, mouse_y = event.pos
                thumb_rect = self.get_thumb_rect()
                
                if thumb_rect.collidepoint(mouse_x, mouse_y):
                    # Start dragging thumb
                    self.dragging = True
                    self.drag_offset = mouse_y - self.thumb_y
                    print(f"Started dragging at thumb_y={self.thumb_y}, mouse_y={mouse_y}, offset={self.drag_offset}")
                    return True
                elif self.rect.collidepoint(mouse_x, mouse_y):
                    # Click on track - jump to position
                    relative_y = mouse_y - self.rect.y
                    track_height = self.rect.height - self.thumb_height
                    
                    if track_height > 0:
                        scroll_progress = relative_y / self.rect.height
                        new_scroll = int(scroll_progress * self.total_items)
                        self.scroll_position = max(0, min(self.max_scroll, new_scroll))
                        self.update_thumb()
                        print(f"Track clicked, new scroll position: {self.scroll_position}")
                        return True
        
        elif event.type == pg.MOUSEBUTTONUP:
            if event.button == 1:
                was_dragging = self.dragging
                if was_dragging:
                    print("Stopped dragging")
                self.dragging = False
                return was_dragging
        
        elif event.type == pg.MOUSEMOTION:
            if self.dragging:
                mouse_y = event.pos[1]
                new_thumb_y = mouse_y - self.drag_offset
                
                # Constrain thumb to track
                new_thumb_y = max(self.rect.y, min(self.rect.y + self.rect.height - self.thumb_height, new_thumb_y))
                
                # Calculate scroll position from thumb position
                track_range = self.rect.height - self.thumb_height
                if track_range > 0:
                    scroll_progress = (new_thumb_y - self.rect.y) / track_range
                    old_scroll = self.scroll_position
                    self.scroll_position = int(scroll_progress * self.max_scroll)
                    self.scroll_position = max(0, min(self.max_scroll, self.scroll_position))
                    self.update_thumb()
                    
                    if old_scroll != self.scroll_position:
                        print(f"Dragging: mouse_y={mouse_y}, new_thumb_y={new_thumb_y}, scroll={self.scroll_position}")
                    
                    return True
        
        return False
    
    def set_scroll_position(self, position):
        """Set scroll position directly"""
        self.scroll_position = max(0, min(self.max_scroll, position))
        self.update_thumb()
    
    def draw(self, surface):
        """Draw the scrollbar"""
        if self.thumb_height == 0:  # No scrolling needed
            return
            
        # Draw track
        pg.draw.rect(surface, DARK_GRAY, self.rect)
        pg.draw.rect(surface, GRAY, self.rect, 2)
        
        # Draw thumb
        thumb_rect = self.get_thumb_rect()
        thumb_color = LIGHT_GRAY if not self.dragging else WHITE
        pg.draw.rect(surface, thumb_color, thumb_rect)
        pg.draw.rect(surface, GRAY, thumb_rect, 1)

class Button:
    def __init__(self, x, y, width, height, text, font, color=WHITE, hover_color=BLUE):
        self.rect = pg.Rect(x, y, width, height)
        self.text = text
        self.font = font
        self.color = color
        self.hover_color = hover_color
        self.is_hovered = False
    
    def handle_event(self, event):
        if event.type == pg.MOUSEMOTION:
            self.is_hovered = self.rect.collidepoint(event.pos)
            return False  # Don't consume the event, just update hover state
        elif event.type == pg.MOUSEBUTTONDOWN:
            if self.rect.collidepoint(event.pos):
                return True
        return False
    
    def update_hover(self, mouse_pos):
        """Update hover state based on mouse position"""
        self.is_hovered = self.rect.collidepoint(mouse_pos)
    
    def draw(self, surface):
        color = self.hover_color if self.is_hovered else self.color
        pg.draw.rect(surface, DARK_GRAY, self.rect)
        pg.draw.rect(surface, color, self.rect, 3)
        
        text_surface = self.font.render(self.text, True, color)
        text_rect = text_surface.get_rect(center=self.rect.center)
        surface.blit(text_surface, text_rect)

class Bottle:
    def __init__(self, start_x, start_y, target_x, target_y, bottle_type="ground", hand="right", is_preview_transition=False):
        # Get current scaling factors
        scale_x = SCREEN_WIDTH / BASE_WIDTH
        scale_y = SCREEN_HEIGHT / BASE_HEIGHT
        
        self.start_x = start_x
        self.start_y = start_y
        self.x = start_x
        self.y = start_y
        self.hand = hand  # Which hand threw this bottle
        self.is_preview_transition = is_preview_transition  # New flag for preview bottles
        
        # Bottle type determines target z-plane and color
        self.bottle_type = bottle_type  # "ground" or "air"
        
        # Target positioning based on bottle type
        if bottle_type == "air":
            # Air bottles target the jumping z-plane
            self.target_x = target_x
            self.target_y = target_y - max(30, int(50 * scale_y))  # Higher target for jump bottles
            self.target_z = (player_z_air_start + player_z_air_end) / 2  # Middle of air z-plane
            self.color = BLUE  # Blue for air bottles
        else:
            # Ground bottles target the ground z-plane
            self.target_x = target_x
            self.target_y = target_y
            self.target_z = (player_z_ground_start + player_z_ground_end) / 2  # Middle of ground z-plane
            self.color = RED  # Red for ground bottles
        
        # Z-axis properties for enhanced 3D effect
        if is_preview_transition:
            # Preview bottles start at a small but visible z to maintain visibility
            self.z = 0.05
        else:
            self.z = 0.01  # Start far away
        
        # Hand-specific properties
        if hand == "left":
            self.z_speed = 0.006  # Slower movement for left hand
            # Random curve for left hand bottles
            self.curve_strength = random.uniform(0.3, 0.8)  # How much it curves
            self.curve_direction = random.choice([-1, 1])  # Left or right curve
            self.curve_peak_z = random.uniform(0.3, 0.6)  # Where the curve peaks
        else:
            self.z_speed = 0.008  # Normal speed for right hand
            self.curve_strength = 0  # No curve for right hand
            self.curve_direction = 0
            self.curve_peak_z = 0
        
        # Calculate movement per frame
        self.total_frames = int((self.target_z - self.z) / self.z_speed)
        if self.total_frames > 0:
            self.dx = (self.target_x - self.start_x) / self.total_frames
            self.dy = (self.target_y - self.start_y) / self.total_frames
        else:
            self.dx = self.dy = 0
        
        # Visual properties - scaled dynamically
        self.base_width = max(1, int(5 * scale_x))
        self.base_height = max(1, int(15 * scale_y))
        self.rotation = 0
        self.rotation_speed = random.uniform(3, 8)
        
        # Create bottle surface with appropriate color
        self.original_image = pg.Surface((self.base_width, self.base_height), pg.SRCALPHA)
        self.original_image.fill(self.color)
        
        self.active = True
        self.hit_player = False  # Track if bottle hit player
        self.scored = False  # Track if bottle has been scored for dodging

    def update(self):
        """Update bottle position and state"""
        if not self.active:
            return True
        
        # Move along z-axis (simulating depth)
        self.z += self.z_speed
        
        # Calculate curve offset for left hand bottles
        curve_offset_x = 0
        if self.hand == "left" and self.curve_strength > 0:
            # Create a curved trajectory using sine wave
            progress = self.z / self.target_z
            if progress <= 1.0:
                # Peak curve at curve_peak_z
                curve_progress = min(1.0, progress / self.curve_peak_z) if self.curve_peak_z > 0 else progress
                curve_offset_x = math.sin(curve_progress * math.pi) * self.curve_strength * self.curve_direction * SCREEN_WIDTH * 0.2
        
        # Move towards target position (with curve for left hand)
        self.x += self.dx + (curve_offset_x * self.z_speed * 10)  # Apply curve gradually
        self.y += self.dy
        
        # Update rotation
        self.rotation = (self.rotation + self.rotation_speed) % 360
        
        # Remove bottle if it has gone past the target z
        if self.z >= self.target_z + 0.1:  # Small buffer past target
            return True
        
        # Check if bottle is completely off-screen
        scale_factor = (self.z ** 1.8) * 15  # Adjusted scaling for current screen
        scale_factor = max(scale_factor, 0.1)
        max_size = max(self.base_width, self.base_height) * scale_factor
        
        if (self.x + max_size < -100 or self.x - max_size > SCREEN_WIDTH + 100 or
            self.y + max_size < -100 or self.y - max_size > SCREEN_HEIGHT + 100):
            return True
            
        return False

    def draw(self, surface):
        """Draw bottle with perspective scaling"""
        if not self.active or self.z <= 0:
            return
        
        # Calculate size based on z-position - scaled dynamically
        scale_factor = (self.z ** 1.8) * (15 * min(SCREEN_WIDTH / BASE_WIDTH, SCREEN_HEIGHT / BASE_HEIGHT))
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

    def is_in_player_collision_zone(self, player_is_jumping):
        """Check if bottle is within the player's current depth collision zone"""
        if not self.active:
            return False
        
        # Only check collision if bottle type matches player state
        if self.bottle_type == "air" and not player_is_jumping:
            return False  # Air bottles can't hit grounded player
        elif self.bottle_type == "ground" and player_is_jumping:
            return False  # Ground bottles can't hit jumping player
        
        # Player has different z-positions when jumping vs on ground
        if player_is_jumping and self.bottle_type == "air":
            return (self.z >= player_z_air_start and 
                    self.z <= player_z_air_end)
        elif not player_is_jumping and self.bottle_type == "ground":
            return (self.z >= player_z_ground_start and 
                    self.z <= player_z_ground_end)
        
        return False

    def get_collision_rect(self, player_is_jumping):
        """Get collision rectangle for bottles in the player's depth zone"""
        if not self.active or not self.is_in_player_collision_zone(player_is_jumping):
            return pg.Rect(0, 0, 0, 0)
        
        # Use exact same scaling logic as visual drawing
        scale_factor = (self.z ** 1.8) * (15 * min(SCREEN_WIDTH / BASE_WIDTH, SCREEN_HEIGHT / BASE_HEIGHT))
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

    def get_distance_to_player(self, player_x, player_y, player_width, player_height):
        """Calculate distance between bottle center and player center"""
        player_center_x = player_x + player_width // 2
        player_center_y = player_y + player_height // 2
        
        dx = self.x - player_center_x
        dy = self.y - player_center_y
        
        return (dx * dx + dy * dy) ** 0.5

    def is_close_call(self, player_x, player_y, player_width, player_height, player_is_jumping):
        """Check if this bottle qualifies as a close call based on distance and type matching"""
        # Close calls only count when:
        # 1. The bottle type matches the player's current state
        # 2. The bottle is within close call distance
        # 3. The bottle is in the collision z-zone
        
        # Type matching check
        if self.bottle_type == "air" and not player_is_jumping:
            return False  # Air bottle but player on ground - no close call
        elif self.bottle_type == "ground" and player_is_jumping:
            return False  # Ground bottle but player jumping - no close call
        
        # Check distance
        distance = self.get_distance_to_player(player_x, player_y, player_width, player_height)
        return distance <= CLOSE_CALL_DISTANCE

def draw_player_with_depth(surface, x, y, width, height, is_jumping):
    """Draw player with visual depth representation based on jumping state"""
    if is_jumping:
        # When jumping, player appears "behind" ground-level bottles
        # Use lighter colors to show they're in the background
        main_color = (200, 200, 200)  # Lighter white
        shadow_color = (100, 100, 100)  # Lighter gray
        shadow_offset = max(1, int(2 * min(SCREEN_WIDTH / BASE_WIDTH, SCREEN_HEIGHT / BASE_HEIGHT)))  # Smaller shadow when in back
    else:
        # When on ground, player appears "in front" 
        main_color = WHITE
        shadow_color = GRAY
        shadow_offset = max(2, int(3 * min(SCREEN_WIDTH / BASE_WIDTH, SCREEN_HEIGHT / BASE_HEIGHT)))
    
    # Main player body
    player_rect = pg.Rect(int(x), int(y), width, height)
    
    # Add depth shadow/outline
    shadow_rect = pg.Rect(int(x + shadow_offset), int(y + shadow_offset), width, height)
    pg.draw.rect(surface, shadow_color, shadow_rect)
    
    # Draw main body on top
    pg.draw.rect(surface, main_color, player_rect)
    
    # Add depth indicator lines
    line_width = max(1, int(2 * min(SCREEN_WIDTH / BASE_WIDTH, SCREEN_HEIGHT / BASE_HEIGHT)))
    pg.draw.line(surface, shadow_color, (int(x), int(y)), (int(x + shadow_offset), int(y + shadow_offset)), line_width)
    pg.draw.line(surface, shadow_color, (int(x + width), int(y)), (int(x + width + shadow_offset), int(y + shadow_offset)), line_width)

def reset_game():
    """Reset all game variables for a new game"""
    global player_x, player_y, vel_y, is_on_ground, drunk_x, lives, start_time, last_bottle_time, bottles
    global next_bottle_preview, next_bottle_show_time, score, bottles_dodged, close_calls, combo_multiplier, score_popups
    global bottle_spawn_time, left_hand_spawn_time, last_left_bottle_time, next_left_bottle_preview, next_left_bottle_show_time
    global current_throwing_hand
    
    # Recalculate scaled values in case screen size changed
    get_scaled_values()
    
    player_x = SCREEN_WIDTH // 2 - player_width // 2
    player_y = player_base_y
    vel_y = 0
    is_on_ground = False
    drunk_x = SCREEN_WIDTH // 2 - drunk_width // 2  # Drunk guy stays centered
    lives = 9
    start_time = pg.time.get_ticks()
    last_bottle_time = pg.time.get_ticks()
    last_left_bottle_time = pg.time.get_ticks()
    bottles = []
    
    # Reset dual hand system
    next_bottle_preview = None
    next_bottle_show_time = 0
    next_left_bottle_preview = None
    next_left_bottle_show_time = 0
    current_throwing_hand = "right"
    
    # Reset scoring system
    score = 0
    bottles_dodged = 0
    close_calls = 0
    combo_multiplier = 1.0  # Remove combo timer - permanent combo system
    score_popups = []
    
    # Reset difficulty
    bottle_spawn_time = 1000  # Start with 1 second spawn time for right hand
    left_hand_spawn_time = 1500  # Start with 1.5 second spawn time for left hand

def calculate_final_score():
    """Calculate final score without time bonus"""
    global final_score
    final_score = score  # No time bonus - just the base score
    logging.info(f"Final score: {final_score}")

def show_menu():
    """Display the main menu"""
    screen.fill(BLACK)
    
    # Title
    title_text = font_large.render("BOTTLE OPS", True, WHITE)
    title_rect = title_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 4))
    screen.blit(title_text, title_rect)
    
    # Buttons - dynamically scaled
    scale_x = SCREEN_WIDTH / BASE_WIDTH
    scale_y = SCREEN_HEIGHT / BASE_HEIGHT
    
    button_width = max(100, int(200 * scale_x))
    button_height = max(30, int(40 * scale_y))
    button_x = SCREEN_WIDTH // 2 - button_width // 2
    
    spacing = max(40, int(50 * scale_y))
    start_y = SCREEN_HEIGHT // 2 - max(60, int(80 * scale_y))
    
    play_button = Button(button_x, start_y, button_width, button_height, "PLAY", font_medium)
    settings_button = Button(button_x, start_y + spacing, button_width, button_height, "SETTINGS", font_medium)
    leaderboard_button = Button(button_x, start_y + spacing * 2, button_width, button_height, "LEADERBOARD", font_medium)
    exit_button = Button(button_x, start_y + spacing * 3, button_width, button_height, "EXIT", font_medium)
    
    # Update hover states for all buttons
    mouse_pos = pg.mouse.get_pos()
    play_button.update_hover(mouse_pos)
    settings_button.update_hover(mouse_pos)
    leaderboard_button.update_hover(mouse_pos)
    exit_button.update_hover(mouse_pos)
    
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
    
    # Dynamic scaling
    scale_x = SCREEN_WIDTH / BASE_WIDTH
    scale_y = SCREEN_HEIGHT / BASE_HEIGHT
    
    # Fullscreen toggle - scaled proportionally
    fullscreen_text = "Fullscreen: ON" if is_fullscreen else "Fullscreen: OFF"
    fs_button = Button(
        SCREEN_WIDTH // 2 - max(80, int(100 * scale_x)), 
        SCREEN_HEIGHT // 2 - max(20, int(30 * scale_y)), 
        max(160, int(200 * scale_x)), 
        max(30, int(40 * scale_y)), 
        fullscreen_text, 
        font_medium
    )
    
    # Back button - scaled proportionally
    back_button = Button(
        SCREEN_WIDTH // 2 - max(80, int(100 * scale_x)), 
        SCREEN_HEIGHT // 2 + max(20, int(30 * scale_y)), 
        max(160, int(200 * scale_x)), 
        max(30, int(40 * scale_y)), 
        "BACK", 
        font_medium
    )
    
    # Update hover states
    mouse_pos = pg.mouse.get_pos()
    fs_button.update_hover(mouse_pos)
    back_button.update_hover(mouse_pos)
    
    fs_button.draw(screen)
    back_button.draw(screen)    
    return fs_button, back_button

def recalculate_scrollbar():
    """Recalculates the scrollbar dimensions and creates a new instance"""
    global scrollbar

    all_scores = leaderboard.get_all_scores()
    scale_x = SCREEN_WIDTH / BASE_WIDTH
    scale_y = SCREEN_HEIGHT / BASE_HEIGHT

    scores_start_y = int(SCREEN_HEIGHT * 0.25)
    scores_end_y = int(SCREEN_HEIGHT * 0.75)
    scores_area_height = scores_end_y - scores_start_y
    scrollbar_width = max(15, int(20 * scale_x))
    scrollbar_x = SCREEN_WIDTH - max(30, int(40 * scale_x))
    scrollbar_y = scores_start_y
    scrollbar_height = scores_area_height - max(30, int(40 * scale_y))

    scrollbar = ScrollBar(
        scrollbar_x,
        scrollbar_y,
        scrollbar_width,
        scrollbar_height,
        len(all_scores),
        max_visible_scores
    )

def show_leaderboard():
    """Display the leaderboard with visual scrollbar"""
    global leaderboard_scroll, scrollbar
    
    screen.fill(BLACK)
    
    # Title
    title_text = font_large.render("LEADERBOARD", True, WHITE)
    title_rect = title_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 6))
    screen.blit(title_text, title_rect)
    
    # Get all scores
    all_scores = leaderboard.get_all_scores()
    
    # Dynamic scaling
    scale_x = SCREEN_WIDTH / BASE_WIDTH
    scale_y = SCREEN_HEIGHT / BASE_HEIGHT
    line_spacing = max(20, int(30 * scale_y))
    
    # Define scores display area
    scores_start_y = int(SCREEN_HEIGHT * 0.3)  # Start below title
    scores_end_y = int(SCREEN_HEIGHT * 0.8)    # End above buttons
    scores_area_height = scores_end_y - scores_start_y

    # Draw outline around the scores area
    box_margin = max(8, int(10 * scale_y))  # Add some padding around the scores
    box_x = int(SCREEN_WIDTH * 0.3)
    box_width = SCREEN_WIDTH - 2 * box_x
    box_y = scores_start_y - box_margin - 20
    box_height = 40 + scores_area_height + 2 * box_margin

    outline_rect = pg.Rect(box_x, box_y, box_width, box_height)
    pg.draw.rect(screen, GRAY, outline_rect, max(2, int(3 * min(scale_x, scale_y))))
    
    # Calculate how many scores can fit in the grey box
    available_height = box_height - 2 * box_margin
    max_visible_scores = max(1, int(available_height // line_spacing))
    
    # Create scrollbar only if it doesn't exist or needs updating
    scrollbar_width = max(15, int(20 * scale_x))
    scrollbar_x = box_x + box_width + max(5, int(8 * scale_x))
    scrollbar_y = box_y
    scrollbar_height = box_height
    
    # Only create new scrollbar if dimensions changed or doesn't exist
    if ('scrollbar' not in globals() or 
        scrollbar.rect.x != scrollbar_x or 
        scrollbar.rect.y != scrollbar_y or 
        scrollbar.rect.width != scrollbar_width or 
        scrollbar.rect.height != scrollbar_height or
        scrollbar.total_items != len(all_scores) or
        scrollbar.visible_items != max_visible_scores):
        
        old_dragging = False
        old_scroll = 0
        if 'scrollbar' in globals():
            old_dragging = scrollbar.dragging
            old_scroll = scrollbar.scroll_position
            
        scrollbar = ScrollBar(
            scrollbar_x,
            scrollbar_y,
            scrollbar_width,
            scrollbar_height,
            len(all_scores),
            max_visible_scores
        )
        
        # Preserve dragging state and scroll position
        scrollbar.dragging = old_dragging
        scrollbar.set_scroll_position(old_scroll)
    
    # Update scroll position from global variable
    scrollbar.set_scroll_position(leaderboard_scroll)
    
    # Display visible scores within the grey box bounds
    visible_scores = all_scores[leaderboard_scroll:leaderboard_scroll + max_visible_scores]
    
    # Calculate left margin for text alignment (inside the grey box)
    text_left_margin = box_x + max(15, int(20 * scale_x))  # Left edge of box + padding
    
    for i, score_data in enumerate(visible_scores):
        username = score_data['username']
        score = score_data['score']
        
        # Actual rank in full leaderboard
        actual_rank = leaderboard_scroll + i + 1
        rank_text = f"{actual_rank}. {username} - {score:,} pts"
        
        # Highlight top 3 scores
        if username == current_username:
            color = RED
        elif actual_rank == 1:
            color = YELLOW  # Gold for 1st
        elif actual_rank == 2:
            color = (192, 192, 192)  # Silver for 2nd
        elif actual_rank == 3:
            color = (205, 127, 50)   # Bronze for 3rd
        else:
            color = WHITE
        
        score_surface = font_small.render(rank_text, True, color)
        # Left-align the text within the grey box
        score_rect = score_surface.get_rect()
        score_rect.x = text_left_margin
        score_rect.y = box_y + box_margin + i * line_spacing  # Position within grey box bounds
        
        # Only draw if within the grey box bounds
        if (score_rect.y >= box_y + box_margin and 
            score_rect.bottom <= box_y + box_height - box_margin):
            screen.blit(score_surface, score_rect)
    
    # Empty leaderboard message
    if len(all_scores) == 0:
        empty_text = font_medium.render("No scores yet!", True, GRAY)
        empty_rect = empty_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))
        screen.blit(empty_text, empty_rect)
    
    # Draw scrollbar only if needed
    if len(all_scores) > max_visible_scores:
        scrollbar.draw(screen)
    
    # Buttons at bottom - scaled proportionally
    button_width = max(80, int(120 * scale_x))
    button_height = max(30, int(40 * scale_y))
    button_spacing = max(100, int(140 * scale_x))
    
    # Center the buttons
    total_button_width = button_width * 2 + button_spacing
    start_x = (SCREEN_WIDTH - total_button_width) // 2
    button_y = SCREEN_HEIGHT - max(45, int(60 * scale_y))
    
    clear_button = Button(
        start_x,
        button_y,
        button_width,
        button_height,
        "CLEAR",
        font_medium,
        color=YELLOW,
        hover_color=RED
    )
    
    back_button = Button(
        start_x + button_width + button_spacing,
        button_y,
        button_width,
        button_height,
        "BACK",
        font_medium
    )
    
    # Update hover states
    mouse_pos = pg.mouse.get_pos()
    clear_button.update_hover(mouse_pos)
    back_button.update_hover(mouse_pos)
    
    clear_button.draw(screen)
    back_button.draw(screen)
    
    return clear_button, back_button, scrollbar

cursor_timer = 0
cursor_visible = True 

def show_username_input():
    global cursor_timer, cursor_visible
    screen.fill(BLACK)

    # Title
    title_text = font_large.render("ENTER USERNAME", True, WHITE)
    title_rect = title_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 3))
    screen.blit(title_text, title_rect)

    scale_x = SCREEN_WIDTH / BASE_WIDTH
    scale_y = SCREEN_HEIGHT / BASE_HEIGHT

    input_box = pg.Rect(
        SCREEN_WIDTH // 2 - max(100, int(150 * scale_x)),
        SCREEN_HEIGHT // 2 - max(15, int(20 * scale_y)),
        max(200, int(300 * scale_x)),
        max(30, int(40 * scale_y))
    )

    color = WHITE if input_active else GRAY
    pg.draw.rect(screen, color, input_box, max(2, int(3 * min(scale_x, scale_y))))

    # Cursor
    cursor_timer += 1
    if cursor_timer >= 30:
        cursor_timer = 0
        cursor_visible = not cursor_visible

    username_surface = font_medium.render(current_username, True, WHITE)
    text_x = input_box.x + max(8, int(10 * scale_x))
    text_y = input_box.y + max(8, int(10 * scale_y))
    screen.blit(username_surface, (text_x, text_y))

    if input_active and cursor_visible:
        cursor_x = text_x + username_surface.get_width() + 2
        cursor_y = text_y
        cursor_height = font_medium.get_height()
        pg.draw.line(screen, WHITE, (cursor_x, cursor_y), (cursor_x, cursor_y + cursor_height), max(1, int(2 * min(scale_x, scale_y))))

    # Instruction text
    inst_text = font_small.render("Press ENTER to continue", True, GRAY)
    inst_rect = inst_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + max(30, int(40 * scale_y))))
    screen.blit(inst_text, inst_rect)

    button_width = max(80, int(100 * scale_x))
    button_height = max(30, int(40 * scale_y))
    button_x = SCREEN_WIDTH - button_width - max(15, int(20 * scale_x))
    button_y = SCREEN_HEIGHT - button_height - max(15, int(20 * scale_y))

    back_button = Button(
        button_x,
        button_y,
        button_width,
        button_height,
        "BACK",
        font_small
    )
    
    # Update hover state
    mouse_pos = pg.mouse.get_pos()
    back_button.update_hover(mouse_pos)
    
    back_button.draw(screen)
    return input_box, back_button

def show_game_over_screen():
    """Display game over screen with simplified scoring and multiple options"""
    global start_time
    screen.fill(BLACK)
    
    # Game Over text
    go_text = font_large.render("GAME OVER", True, RED)
    go_rect = go_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 5))
    screen.blit(go_text, go_rect)
    
    # Final score (no breakdown needed since no time bonus)
    scale_y = SCREEN_HEIGHT / BASE_HEIGHT
    line_height = max(25, int(35 * scale_y))
    start_y = SCREEN_HEIGHT // 3
    
    # Final score
    final_text = font_large.render(f"FINAL SCORE: {final_score:,}", True, YELLOW)
    final_rect = final_text.get_rect(center=(SCREEN_WIDTH // 2, start_y))
    screen.blit(final_text, final_rect)
    
    # Time survived
    current_time = pg.time.get_ticks()
    survival_time_seconds = (current_time - start_time) // 1000
    minutes = survival_time_seconds // 60
    seconds = survival_time_seconds % 60
    time_text = font_medium.render(f"Time Survived: {minutes:02d}:{seconds:02d}", True, GREEN)
    time_rect = time_text.get_rect(center=(SCREEN_WIDTH // 2, start_y + line_height))
    screen.blit(time_text, time_rect)
    
    # Buttons - scaled proportionally
    scale_x = SCREEN_WIDTH / BASE_WIDTH
    button_width = max(80, int(140 * scale_x))
    button_height = max(30, int(40 * scale_y))
    button_spacing_x = max(10, int(20 * scale_x))
    button_spacing_y = max(10, int(15 * scale_y))
    
    # Calculate button positions in a 2x2 grid
    total_width = button_width * 2 + button_spacing_x
    start_x = (SCREEN_WIDTH - total_width) // 2
    buttons_start_y = start_y + line_height * 3
    
    # First row
    play_again_button = Button(
        start_x,
        buttons_start_y,
        button_width,
        button_height,
        "PLAY AGAIN",
        font_small,
        color=GREEN,
        hover_color=WHITE
    )
    
    leaderboard_button = Button(
        start_x + button_width + button_spacing_x,
        buttons_start_y,
        button_width,
        button_height,
        "LEADERBOARD",
        font_small
    )
    
    # Second row
    menu_button = Button(
        start_x,
        buttons_start_y + button_height + button_spacing_y,
        button_width,
        button_height,
        "MAIN MENU",
        font_small
    )
    
    quit_button = Button(
        start_x + button_width + button_spacing_x,
        buttons_start_y + button_height + button_spacing_y,
        button_width,
        button_height,
        "QUIT",
        font_small,
        color=RED,
        hover_color=ORANGE
    )
    
    # Update hover states
    mouse_pos = pg.mouse.get_pos()
    play_again_button.update_hover(mouse_pos)
    leaderboard_button.update_hover(mouse_pos)
    menu_button.update_hover(mouse_pos)
    quit_button.update_hover(mouse_pos)
    
    play_again_button.draw(screen)
    leaderboard_button.draw(screen)
    menu_button.draw(screen)
    quit_button.draw(screen)
    
    return play_again_button, leaderboard_button, menu_button, quit_button

def safe_game_loop():
    """Main game loop with enhanced scoring system, progressive difficulty, and dual hand throwing"""
    global player_x, player_y, vel_y, is_on_ground, drunk_x, lives, last_bottle_time, bottles, start_time, screen
    global next_bottle_preview, next_bottle_show_time, score, bottles_dodged, close_calls, combo_multiplier, combo_timer
    global bottle_spawn_time, left_hand_spawn_time, last_left_bottle_time, next_left_bottle_preview, next_left_bottle_show_time
    global current_throwing_hand
    
    running = True
    frame_count = 0
    
    while running:
        frame_count += 1
        current_time = pg.time.get_ticks()
        
        # Update difficulty based on score
        bottle_spawn_time, left_hand_spawn_time = get_current_difficulty()
        
        screen.fill(BLACK)
        keys = pg.key.get_pressed()
        
        # Player movement - no error handling needed for basic movement
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
        
        # Drunk guy (stationary) - just draw it
        drunk_rect = pg.Rect(int(drunk_x), drunk_y, drunk_width, drunk_height)
        pg.draw.rect(screen, YELLOW, drunk_rect)
        
        # Calculate hand positions for preview bottles
        scale_x = SCREEN_WIDTH / BASE_WIDTH
        scale_y = SCREEN_HEIGHT / BASE_HEIGHT
        
        # Right hand position (right side of drunk guy)
        right_hand_x = drunk_x + drunk_width + max(10, int(15 * scale_x))
        right_hand_y = drunk_y + drunk_height // 3  # Upper part for right hand
        
        # Left hand position (left side of drunk guy)
        left_hand_x = drunk_x - max(15, int(20 * scale_x))
        left_hand_y = drunk_y + drunk_height // 3  # Upper part for left hand
        
        # RIGHT HAND: Bottle preview and spawning system
        if next_bottle_preview is None:
            # Time to show a new preview bottle from right hand
            if current_time - last_bottle_time > bottle_spawn_time:
                # 2/3 chance for ground, 1/3 chance for air (twice as likely for ground)
                bottle_type = random.choices(["ground", "air"], weights=[2, 1])[0]
                
                # Create preview bottle (not thrown yet)
                next_bottle_preview = {
                    'type': bottle_type,
                    'color': RED if bottle_type == "ground" else BLUE
                }
                next_bottle_show_time = current_time
        
        # LEFT HAND: Bottle preview and spawning system
        if next_left_bottle_preview is None:
            # Time to show a new preview bottle from left hand
            if current_time - last_left_bottle_time > left_hand_spawn_time:
                # Same distribution as right hand
                bottle_type = random.choices(["ground", "air"], weights=[2, 1])[0]
                
                # Create preview bottle (not thrown yet)
                next_left_bottle_preview = {
                    'type': bottle_type,
                    'color': RED if bottle_type == "ground" else BLUE
                }
                next_left_bottle_show_time = current_time
        
        # Draw RIGHT HAND preview bottle
        if next_bottle_preview is not None:
            preview_size = max(8, int(12 * min(scale_x, scale_y)))
            preview_rect = pg.Rect(right_hand_x, right_hand_y, preview_size, preview_size)
            pg.draw.rect(screen, next_bottle_preview['color'], preview_rect)
            
            # Check if it's time to throw the bottle from right hand
            if current_time - next_bottle_show_time >= next_bottle_throw_delay:
                # Create transition bottle that starts visible
                new_bottle = Bottle(
                    right_hand_x + preview_size // 2,  # Start from preview position
                    right_hand_y + preview_size // 2,
                    player_x + player_width // 2,
                    player_base_y + player_height // 2,
                    next_bottle_preview['type'],
                    "right",
                    is_preview_transition=True  # Start at visible z
                )
                bottles.append(new_bottle)
                
                # Reset for next bottle
                next_bottle_preview = None
                last_bottle_time = current_time
        
        # Draw LEFT HAND preview bottle
        if next_left_bottle_preview is not None:
            preview_size = max(8, int(12 * min(scale_x, scale_y)))
            preview_rect = pg.Rect(left_hand_x, left_hand_y, preview_size, preview_size)
            pg.draw.rect(screen, next_left_bottle_preview['color'], preview_rect)
            
            # Check if it's time to throw the bottle from left hand
            if current_time - next_left_bottle_show_time >= next_left_bottle_throw_delay:
                # Create transition bottle that starts visible
                new_bottle = Bottle(
                    left_hand_x + preview_size // 2,  # Start from preview position
                    left_hand_y + preview_size // 2,
                    player_x + player_width // 2,
                    player_base_y + player_height // 2,
                    next_left_bottle_preview['type'],
                    "left",
                    is_preview_transition=True  # Start at visible z
                )
                bottles.append(new_bottle)
                
                # Reset for next bottle
                next_left_bottle_preview = None
                last_left_bottle_time = current_time
        
        # Update bottles and separate by layer
        bottles_to_remove = []
        bottles_behind = []
        bottles_in_front = []
        
        for i, bottle in enumerate(bottles):
            if bottle.update():
                # Bottle has moved past the target - check if it should be scored as dodged
                if not bottle.hit_player and not bottle.scored:
                    # Check if this was a close call using the improved detection
                    is_close_call = bottle.is_close_call(player_x, player_y, player_width, player_height, not is_on_ground)
                    
                    # Calculate score with permanent combo system
                    base_points = CLOSE_CALL_SCORE if is_close_call else BASE_DODGE_SCORE
                    points = int(base_points * combo_multiplier)
                    
                    # Add to score
                    score += points
                    bottles_dodged += 1
                    if is_close_call:
                        close_calls += 1
                    
                    # Update combo system (no timer limit)
                    combo_multiplier = min(MAX_COMBO, combo_multiplier + COMBO_INCREMENT)
                    
                    # Add visual feedback
                    add_score_popup(
                        bottle.x, bottle.y - 30, 
                        points, is_close_call, combo_multiplier
                    )
                    
                    bottle.scored = True
                    logging.info(f"Bottle dodged! Points: {points} (base: {base_points}, combo: x{combo_multiplier:.1f}) Close call: {is_close_call}")
                
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
                    bottles_behind.append(bottle)  # Draw in front for visibility
                
                # Collision detection with proper height/type matching
                if bottle.is_in_player_collision_zone(not is_on_ground):
                    player_rect = pg.Rect(int(player_x), int(player_y), player_width, player_height)
                    bottle_collision_rect = bottle.get_collision_rect(not is_on_ground)
                    
                    if (bottle_collision_rect.width > 0 and bottle_collision_rect.height > 0 and
                        player_rect.colliderect(bottle_collision_rect)):
                        lives -= 1
                        bottle.hit_player = True  # Mark for removal
                        bottles_to_remove.append(i)
                        
                        # Reset combo when hit
                        combo_multiplier = 1.0
                        
                        # Enhanced logging with bottle type and hand
                        jump_status = "jumping" if not is_on_ground else "on ground"
                        player_z = f"{current_player_z_start:.1f}-{current_player_z_end:.1f}"
                        logging.info(f"Player hit while {jump_status} by {bottle.hand} hand {bottle.bottle_type} bottle (z={bottle.z:.3f}, player_z={player_z})! Lives remaining: {lives}")
                        
                        if lives <= 0:
                            logging.info("Game over - no lives remaining")
                            calculate_final_score()
                            return current_time - start_time  # Return survival time
        
        # Remove bottles safely (reverse order to maintain indices)
        for i in reversed(sorted(set(bottles_to_remove))):
            if 0 <= i < len(bottles):
                bottles.pop(i)
        
        # Update score popups
        update_score_popups()
        
        # Draw bottles behind player
        for bottle in bottles_behind:
            bottle.draw(screen)
        
        draw_player_with_depth(screen, player_x, player_y, player_width, player_height, not is_on_ground)
        
        # Draw bottles in front of player
        for bottle in bottles_in_front:
            bottle.draw(screen)
        
        # Draw score popups on top
        draw_score_popups(screen)
        
        # Simplified HUD - scaled proportionally
        scale_x = SCREEN_WIDTH / BASE_WIDTH
        scale_y = SCREEN_HEIGHT / BASE_HEIGHT
        
        # Lives on top-left with color coding
        lives_color = GREEN if lives > 6 else ORANGE if lives > 3 else RED
        life_text = font_small.render(f"Lives: {lives}", True, lives_color)
        screen.blit(life_text, (max(10, int(15 * scale_x)), max(10, int(15 * scale_y))))
        
        # Score on top-center
        score_text = font_medium.render(f"Score: {score:,}", True, WHITE)
        score_rect = score_text.get_rect(center=(SCREEN_WIDTH // 2, max(20, int(25 * scale_y))))
        screen.blit(score_text, score_rect)
        
        # Combo multiplier (always show since no timer limit)
        if combo_multiplier > 1.0:
            combo_text = font_small.render(f"COMBO x{combo_multiplier:.1f}", True, PURPLE)
            combo_rect = combo_text.get_rect(center=(SCREEN_WIDTH // 2, max(45, int(55 * scale_y))))
            screen.blit(combo_text, combo_rect)
        
        # Time survived on top-right
        time_survived = (current_time - start_time) // 1000
        minutes = time_survived // 60
        seconds = time_survived % 60
        time_text = font_small.render(f"Time: {minutes:02d}:{seconds:02d}", True, GREEN)
        time_rect = time_text.get_rect()
        screen.blit(time_text, (SCREEN_WIDTH - time_rect.width - max(10, int(15 * scale_x)), max(10, int(15 * scale_y))))
        
        # Back button
        button_width = max(80, int(100 * scale_x))
        button_height = max(30, int(40 * scale_y))
        button_x = SCREEN_WIDTH - button_width - max(15, int(20 * scale_x))
        button_y = SCREEN_HEIGHT - button_height - max(15, int(20 * scale_y))

        back_button = Button(
            button_x,
            button_y,
            button_width,
            button_height,
            "BACK",
            font_small
        )
        
        # Update hover state for back button
        mouse_pos = pg.mouse.get_pos()
        back_button.update_hover(mouse_pos)
        
        back_button.draw(screen)
        
        # Event handling
        for event in pg.event.get():
            if event.type == pg.QUIT:
                logging.info("User quit game")
                return -1
            elif event.type == pg.KEYDOWN:
                if event.key == pg.K_ESCAPE:
                    logging.info("User pressed escape")
                    return -1
            elif event.type == pg.MOUSEBUTTONDOWN:
                if back_button.handle_event(event):
                    logging.info("Back button clicked during gameplay")
                    return -1
            elif event.type == pg.VIDEORESIZE:
                # Handle window resize
                new_width, new_height = event.w, event.h
                update_screen_dimensions(new_width, new_height)
                # Reset game elements to new screen size
                reset_game()
        
        # Update display
        pg.display.flip()
        clock.tick(60)

current_username = ""

def main():
    """Main game function with menu system"""
    global current_state, current_username, input_active, final_score, is_fullscreen, screen, leaderboard, leaderboard_scroll
    global SCREEN_WIDTH, SCREEN_HEIGHT, font_large, font_medium, font_small, fade_direction, next_state

    leaderboard = LeaderboardManager()
    
    try:
        while True:
            # Update fade transition
            update_fade()
            
            # Handle global resize events for all states
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    return
                elif event.type == pg.VIDEORESIZE and not is_fullscreen:
                    # Handle window resize
                    new_width, new_height = event.w, event.h
                    update_screen_dimensions(new_width, new_height)
                    
                # Re-queue the event for state-specific handling
                pg.event.post(event)
            
            # Only process input if not in the middle of a fade transition
            if fade_direction == 0:
                if current_state == MENU:
                    play_btn, settings_btn, leaderboard_btn, exit_btn = show_menu()
                    
                    for event in pg.event.get():
                        if event.type == pg.QUIT:
                            return
                        elif event.type == pg.KEYDOWN:
                            if event.key == pg.K_ESCAPE:
                                return
                        
                        # Handle button clicks with fade transitions
                        if play_btn.handle_event(event):
                            start_fade_transition(USERNAME_INPUT)
                            input_active = True
                        elif settings_btn.handle_event(event):
                            start_fade_transition(SETTINGS)
                        elif leaderboard_btn.handle_event(event):
                            start_fade_transition(LEADERBOARD)
                        elif exit_btn.handle_event(event):
                            return
                
                elif current_state == USERNAME_INPUT:
                    input_box, back_button = show_username_input()
                    
                    for event in pg.event.get():
                        if event.type == pg.QUIT:
                            return
                        elif event.type == pg.KEYDOWN:
                            if event.key == pg.K_ESCAPE:
                                start_fade_transition(MENU)
                            elif event.key == pg.K_RETURN:
                                if current_username.strip():
                                    reset_game()
                                    start_fade_transition(PLAYING)
                            elif event.key == pg.K_BACKSPACE:
                                mods = pg.key.get_mods()
                                if mods & pg.KMOD_CTRL:
                                    current_username = ""
                                else:
                                    current_username = current_username[:-1]
                            else:
                                if len(current_username) < 10 and event.unicode.isprintable():
                                    current_username += event.unicode
                        elif event.type == pg.MOUSEBUTTONDOWN:
                            input_active = input_box.collidepoint(event.pos)
                            if back_button.handle_event(event):
                                start_fade_transition(MENU)

                elif current_state == PLAYING:
                    survival_time = safe_game_loop()
                    if survival_time == -1:  # User quit or escaped
                        start_fade_transition(MENU)
                    else:
                        # final_score already calculated in safe_game_loop
                        leaderboard.add_score(current_username, final_score)
                        start_fade_transition(GAME_OVER)
                
                elif current_state == SETTINGS:
                    fs_btn, back_btn = show_settings()  
                    
                    for event in pg.event.get():
                        if event.type == pg.QUIT:
                            return
                        elif event.type == pg.KEYDOWN:
                            if event.key == pg.K_ESCAPE:
                                start_fade_transition(MENU)
                        
                        if fs_btn.handle_event(event):
                            # Toggle fullscreen using the new safe method
                            if not toggle_fullscreen():
                                logging.warning("Failed to toggle fullscreen mode")
                        elif back_btn.handle_event(event):
                            start_fade_transition(MENU)
                
                elif current_state == LEADERBOARD:
                    clear_btn, back_btn, scrollbar = show_leaderboard()
                    
                    for event in pg.event.get():
                        if event.type == pg.QUIT:
                            return
                        elif event.type == pg.KEYDOWN:
                            if event.key == pg.K_ESCAPE:
                                start_fade_transition(MENU)
                        
                        # Handle scrollbar events first (all event types)
                        if scrollbar.handle_event(event):
                            leaderboard_scroll = scrollbar.scroll_position
                        # Handle button events
                        elif clear_btn.handle_event(event):
                            if len(leaderboard.get_all_scores()) > 0:
                                leaderboard.clear_all_scores()
                                leaderboard_scroll = 0
                                logging.info("Leaderboard cleared by user")
                        elif back_btn.handle_event(event):
                            leaderboard_scroll = 0
                            start_fade_transition(MENU)
        
                elif current_state == GAME_OVER:
                    play_again_btn, leaderboard_btn, menu_btn, quit_btn = show_game_over_screen()
                    
                    for event in pg.event.get():
                        if event.type == pg.QUIT:
                            return
                        elif event.type == pg.KEYDOWN:
                            if event.key == pg.K_ESCAPE:
                                start_fade_transition(MENU)
                            elif event.key == pg.K_RETURN:
                                # Enter key for quick play again
                                reset_game()
                                start_fade_transition(PLAYING)
                        
                        # Handle button clicks
                        if play_again_btn.handle_event(event):
                            reset_game()
                            start_fade_transition(PLAYING)
                        elif leaderboard_btn.handle_event(event):
                            start_fade_transition(LEADERBOARD)
                        elif menu_btn.handle_event(event):
                            start_fade_transition(MENU)
                        elif quit_btn.handle_event(event):
                            return
            
            else:
                # During fade transition, still render the current state but don't process input
                if current_state == MENU:
                    show_menu()
                elif current_state == USERNAME_INPUT:
                    show_username_input()
                elif current_state == SETTINGS:
                    show_settings()
                elif current_state == LEADERBOARD:
                    show_leaderboard()
                elif current_state == GAME_OVER:
                    show_game_over_screen()
                
                # Clear event queue during transitions to prevent input buildup
                pg.event.clear()
            
            # Draw fade overlay last (on top of everything)
            draw_fade()
            
            pg.display.flip()
            clock.tick(60)
            
    except Exception as e:
        logging.error(f"Error in main loop: {e}")
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
        
    finally:
        try:
            pg.quit()
        except:
            pass
        exit(0)
