import pygame as pg
import random
from sys import exit
import logging
import json
import os
import math
import threading
import time
import urllib.request
from io import BytesIO

# Configure logging for error handling
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('bottle_ops.log'),
        logging.StreamHandler()
    ]
)

# Enhanced Image configuration - now supports all UI elements and animations
IMAGE_URLS = {
    # Player animations
    'player_idle': [
        "https://github.com/Hoose-Gorse/Applied_Computing_SAC.Bottle-Ops/blob/main/graphics/player/cat-left-down.png?raw=true",
        "https://github.com/Hoose-Gorse/Applied_Computing_SAC.Bottle-Ops/blob/main/graphics/player/cat-left-down.png?raw=true"
    ],
    'player_run': [
        "https://github.com/Hoose-Gorse/Applied_Computing_SAC.Bottle-Ops/blob/main/graphics/player/cat-left-mid-jump.png?raw=true",
        "https://github.com/Hoose-Gorse/Applied_Computing_SAC.Bottle-Ops/blob/main/graphics/player/cat-left-start-jump.png?raw=true"
    ],
    'player_jump': [
        "https://github.com/Hoose-Gorse/Applied_Computing_SAC.Bottle-Ops/blob/main/graphics/player/cat-left-start-jump.png?raw=true",
        "https://github.com/Hoose-Gorse/Applied_Computing_SAC.Bottle-Ops/blob/main/graphics/player/cat-left-mid-jump.png?raw=true",
        "https://github.com/Hoose-Gorse/Applied_Computing_SAC.Bottle-Ops/blob/main/graphics/player/cat-left-jumping.png?raw=true"
    ],
    
    # Drunk guy animations
    'drunk_idle': [
        "https://github.com/Hoose-Gorse/Applied_Computing_SAC.Bottle-Ops/blob/main/graphics/drunk/idle.png?raw=true",
        "https://github.com/Hoose-Gorse/Applied_Computing_SAC.Bottle-Ops/blob/main/graphics/drunk/idle.png?raw=true",
        "https://github.com/Hoose-Gorse/Applied_Computing_SAC.Bottle-Ops/blob/main/graphics/drunk/idle.png?raw=true"
    ],
    'drunk_left_throw': [
        "https://github.com/Hoose-Gorse/Applied_Computing_SAC.Bottle-Ops/blob/main/graphics/hand/left.png?raw=true",
        "https://github.com/Hoose-Gorse/Applied_Computing_SAC.Bottle-Ops/blob/main/graphics/hand/left.png?raw=true",
        "https://github.com/Hoose-Gorse/Applied_Computing_SAC.Bottle-Ops/blob/main/graphics/hand/left.png?raw=true"
    ],
    'drunk_right_throw': [
        "https://github.com/Hoose-Gorse/Applied_Computing_SAC.Bottle-Ops/blob/main/graphics/hand/right.png?raw=true",
        "https://github.com/Hoose-Gorse/Applied_Computing_SAC.Bottle-Ops/blob/main/graphics/hand/right.png?raw=true",
        "https://github.com/Hoose-Gorse/Applied_Computing_SAC.Bottle-Ops/blob/main/graphics/hand/right.png?raw=true"
    ],
    
    # Backgrounds for different screens
    'background_menu': "https://github.com/Hoose-Gorse/Applied_Computing_SAC.Bottle-Ops/blob/main/graphics/backgrounds/main-menu-background.png?raw=true",
    'background_game': "https://github.com/Hoose-Gorse/Applied_Computing_SAC.Bottle-Ops/blob/main/graphics/backgrounds/background-main.png?raw=true",
    'background_settings': "https://github.com/Hoose-Gorse/Applied_Computing_SAC.Bottle-Ops/blob/main/graphics/backgrounds/main-menu-background.png?raw=true",
    'background_leaderboard': "https://github.com/Hoose-Gorse/Applied_Computing_SAC.Bottle-Ops/blob/main/graphics/backgrounds/main-menu-background.png?raw=true",
    
    # UI Text Images (optional replacements for rendered text)
    'text_title': "https://github.com/Hoose-Gorse/Applied_Computing_SAC.Bottle-Ops/blob/main/graphics/backgrounds/bottle-ops-white.png?raw=true",
    'text_play': "https://github.com/Hoose-Gorse/Applied_Computing_SAC.Bottle-Ops/blob/main/graphics/buttons/play-button.png?raw=true",
    'text_settings': "https://github.com/Hoose-Gorse/Applied_Computing_SAC.Bottle-Ops/blob/main/graphics/buttons/setting-button.png?raw=true",
    'text_leaderboard': "https://github.com/Hoose-Gorse/Applied_Computing_SAC.Bottle-Ops/blob/main/graphics/buttons/leaderboard-button.png?raw=true",
    'text_quit': "https://github.com/Hoose-Gorse/Applied_Computing_SAC.Bottle-Ops/blob/main/graphics/buttons/quit-button.png?raw=true",
    'text_back': "https://github.com/Hoose-Gorse/Applied_Computing_SAC.Bottle-Ops/blob/main/graphics/buttons/back.png?raw=true",
    'text_game_over': "https://github.com/Hoose-Gorse/Applied_Computing_SAC.Bottle-Ops/blob/main/graphics/ui/game_over.png?raw=true",
    
    # Special effects
    'effect_shatter': [
        "https://github.com/Hoose-Gorse/Applied_Computing_SAC.Bottle-Ops/blob/main/graphics/bottles/shattter-pile.png?raw=true",
        "https://github.com/Hoose-Gorse/Applied_Computing_SAC.Bottle-Ops/blob/main/graphics/bottles/shattter-pile.png?raw=true",
        "https://github.com/Hoose-Gorse/Applied_Computing_SAC.Bottle-Ops/blob/main/graphics/bottles/shattter-pile.png?raw=true"
    ],
    'effect_explosion': [
        "https://github.com/Hoose-Gorse/Applied_Computing_SAC.Bottle-Ops/blob/main/graphics/bottles/explosion.png?raw=true",
        "https://github.com/Hoose-Gorse/Applied_Computing_SAC.Bottle-Ops/blob/main/graphics/bottles/explosion.png?raw=true",
        "https://github.com/Hoose-Gorse/Applied_Computing_SAC.Bottle-Ops/blob/main/graphics/bottles/explosion.png?raw=true",
        "https://github.com/Hoose-Gorse/Applied_Computing_SAC.Bottle-Ops/blob/main/graphics/bottles/explosion.png?raw=true"
    ],
    
    # Button images
    'button_normal': "https://github.com/Hoose-Gorse/Applied_Computing_SAC.Bottle-Ops/blob/main/graphics/buttons/buttons-background.png?raw=true",
    'button_hover': "https://github.com/Hoose-Gorse/Applied_Computing_SAC.Bottle-Ops/blob/main/graphics/buttons/button-background-hover-thing.png?raw=true",
    
    # Bottles (existing)
    'bottles': {
        1: "https://github.com/Hoose-Gorse/Applied_Computing_SAC.Bottle-Ops/blob/main/graphics/bottles/normal-beer-bottle.png?raw=true",
        2: "https://github.com/Hoose-Gorse/Applied_Computing_SAC.Bottle-Ops/blob/main/graphics/bottles/Helium-beer-bottle.png?raw=true",
        3: "https://github.com/Hoose-Gorse/Applied_Computing_SAC.Bottle-Ops/blob/main/graphics/bottles/Boomerang-bottle.png?raw=true",
        4: "https://github.com/Hoose-Gorse/Applied_Computing_SAC.Bottle-Ops/blob/main/graphics/bottles/Glass-bottle.png?raw=true",
        5: "https://github.com/Hoose-Gorse/Applied_Computing_SAC.Bottle-Ops/blob/main/graphics/bottles/Moltov.png?raw=true",
        6: "https://github.com/Hoose-Gorse/Applied_Computing_SAC.Bottle-Ops/blob/main/graphics/bottles/sugarglass-sticlky.png?raw=true",
        7: "https://github.com/Hoose-Gorse/Applied_Computing_SAC.Bottle-Ops/blob/main/graphics/bottles/Leak-bottle.png?raw=true",
        8: "https://github.com/Hoose-Gorse/Applied_Computing_SAC.Bottle-Ops/blob/main/graphics/bottles/pill-bottle.png?raw=true",
        9: "https://github.com/Hoose-Gorse/Applied_Computing_SAC.Bottle-Ops/blob/main/graphics/bottles/INK-bottle.png?raw=true",
        10: "https://github.com/Hoose-Gorse/Applied_Computing_SAC.Bottle-Ops/blob/main/graphics/bottles/hourglass-bottlwe.png?raw=true",
        11: "https://github.com/Hoose-Gorse/Applied_Computing_SAC.Bottle-Ops/blob/main/graphics/bottles/Caffeine.png?raw=true",
        12: "https://github.com/Hoose-Gorse/Applied_Computing_SAC.Bottle-Ops/blob/main/graphics/bottles/Gold-bottle.png?raw=true",
        13: "https://github.com/Hoose-Gorse/Applied_Computing_SAC.Bottle-Ops/blob/main/graphics/bottles/star-bottle.png?raw=true",
        14: "https://github.com/Hoose-Gorse/Applied_Computing_SAC.Bottle-Ops/blob/main/graphics/bottles/ghost.png?raw=true",
        15: "https://github.com/Hoose-Gorse/Applied_Computing_SAC.Bottle-Ops/blob/main/graphics/bottles/prankster.png?raw=true"
    }
}

# Animation configuration
ANIMATION_CONFIG = {
    'player_idle': {'fps': 2, 'loop': True},
    'player_run': {'fps': 8, 'loop': True},
    'player_jump': {'fps': 6, 'loop': False},
    'drunk_idle': {'fps': 3, 'loop': True},
    'drunk_left_throw': {'fps': 12, 'loop': False},
    'drunk_right_throw': {'fps': 12, 'loop': False},
    'effect_shatter': {'fps': 8, 'loop': False},
    'effect_explosion': {'fps': 10, 'loop': False}
}

USE_LOCAL_IMAGES = False
LOCAL_IMAGE_PATHS = {}

# ANIMATION AND VISUAL CLASSES

class Animation:
    """Handles sprite animation with configurable FPS and looping"""
    
    def __init__(self, frames, fps=8, loop=True):
        self.frames = frames if frames else []
        self.fps = fps
        self.loop = loop
        self.frame_duration = max(1, 60 // fps) if fps > 0 else 1  # Convert FPS to frame ticks at 60fps
        
        self.current_frame = 0
        self.frame_timer = 0
        self.finished = False
        self.playing = True
    
    def update(self):
        """Update animation frame"""
        if not self.playing or not self.frames or self.finished:
            return
        
        self.frame_timer += 1
        
        if self.frame_timer >= self.frame_duration:
            self.frame_timer = 0
            
            if self.current_frame < len(self.frames) - 1:
                self.current_frame += 1
            else:
                # Reached the end
                if self.loop:
                    self.current_frame = 0  # Loop back to start
                else:
                    self.finished = True  # Mark as finished
    
    def get_current_frame(self):
        """Get current animation frame"""
        if not self.frames or self.current_frame >= len(self.frames):
            return None
        return self.frames[self.current_frame]
    
    def reset(self):
        """Reset animation to beginning"""
        self.current_frame = 0
        self.frame_timer = 0
        self.finished = False
        self.playing = True
    
    def play(self):
        """Start/resume animation"""
        self.playing = True
    
    def pause(self):
        """Pause animation"""
        self.playing = False
    
    def is_finished(self):
        """Check if animation is finished (only relevant for non-looping animations)"""
        return self.finished
    
    def set_frame(self, frame_index):
        """Set specific frame"""
        if 0 <= frame_index < len(self.frames):
            self.current_frame = frame_index
            self.frame_timer = 0

class ImageManager:
    """Enhanced image manager with animation support"""
    
    def __init__(self):
        self.images = {}
        self.animations = {}
        self.loading_threads = {}
        self.loading_complete = False
        self.fallback_mode = False
        
        # Loading progress tracking
        self.total_assets = 0
        self.loaded_assets = 0
        self.loading_progress = 0.0
        
        # Start loading images in background
        self.start_image_loading()
    
    def start_image_loading(self):
        """Start background thread to load all images and create animations"""
        def load_all_images():
            try:
                # Calculate total assets to load
                self.total_assets = 0
                
                # Count single images
                single_images = ['background_menu', 'background_game', 'background_settings', 
                               'background_leaderboard', 'text_title', 'text_play', 'text_settings',
                               'text_leaderboard', 'text_quit', 'text_back', 'text_game_over',
                               'button_normal', 'button_hover']
                
                for key in single_images:
                    if key in IMAGE_URLS and IMAGE_URLS[key]:
                        self.total_assets += 1
                
                # Count animation frames
                animation_sequences = ['player_idle', 'player_run', 'player_jump', 
                                     'drunk_idle', 'drunk_left_throw', 'drunk_right_throw',
                                     'effect_shatter', 'effect_explosion']
                
                for seq_key in animation_sequences:
                    if seq_key in IMAGE_URLS:
                        self.total_assets += len(IMAGE_URLS[seq_key])
                
                # Count bottle images
                for bottle_id, url in IMAGE_URLS['bottles'].items():
                    if url:
                        self.total_assets += 1
                
                logging.info(f"Total assets to load: {self.total_assets}")
                
                # Load single images
                for key in single_images:
                    if key in IMAGE_URLS and IMAGE_URLS[key]:
                        self.load_image(key, IMAGE_URLS[key])
                        self.loaded_assets += 1
                        self.loading_progress = self.loaded_assets / self.total_assets
                
                # Load animation sequences
                for seq_key in animation_sequences:
                    if seq_key in IMAGE_URLS:
                        frames = []
                        for i, url in enumerate(IMAGE_URLS[seq_key]):
                            frame_key = f"{seq_key}_frame_{i}"
                            self.load_image(frame_key, url)
                            self.loaded_assets += 1
                            self.loading_progress = self.loaded_assets / self.total_assets
                            if frame_key in self.images and self.images[frame_key]:
                                frames.append(self.images[frame_key])
                        
                        # Create animation with proper config
                        if frames and seq_key in ANIMATION_CONFIG:
                            config = ANIMATION_CONFIG[seq_key]
                            self.animations[seq_key] = Animation(
                                frames, 
                                fps=config['fps'], 
                                loop=config['loop']
                            )
                
                # Load bottle images
                for bottle_id, url in IMAGE_URLS['bottles'].items():
                    if url:
                        self.load_image(f'bottle_{bottle_id}', url)
                        self.loaded_assets += 1
                        self.loading_progress = self.loaded_assets / self.total_assets
                
                self.loading_complete = True
                self.loading_progress = 1.0
                logging.info("All images and animations loaded successfully")
                
            except Exception as e:
                logging.error(f"Error loading images: {e}")
                self.fallback_mode = True
                self.loading_complete = True
        
        thread = threading.Thread(target=load_all_images, daemon=True)
        thread.start()
    
    def load_image_from_url(self, url):
        """Load image from raw URL using urllib"""
        try:
            req = urllib.request.Request(url, headers={
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
            })
            
            with urllib.request.urlopen(req, timeout=10) as response:
                image_data = response.read()
            
            image = pg.image.load(BytesIO(image_data))
            if image.get_alpha() is None:
                image = image.convert()
            else:
                image = image.convert_alpha()
            return image
            
        except Exception as e:
            logging.warning(f"Failed to load image from URL: {e}")
            return None
    
    def load_image_from_data_url(self, data_url):
        """Load image from data URL"""
        try:
            import base64
            
            header, data = data_url.split(',', 1)
            image_data = base64.b64decode(data)
            
            image = pg.image.load(BytesIO(image_data))
            if image.get_alpha() is None:
                image = image.convert()
            else:
                image = image.convert_alpha()
            return image
            
        except Exception as e:
            logging.warning(f"Failed to load image from data URL: {e}")
            return None
    
    def load_image(self, key, url):
        """Load a single image from URL, data URL, or local file"""
        try:
            # Try local image first if enabled
            if USE_LOCAL_IMAGES and key in LOCAL_IMAGE_PATHS:
                local_path = LOCAL_IMAGE_PATHS[key]
                if os.path.exists(local_path):
                    image = pg.image.load(local_path)
                    if image.get_alpha() is None:
                        image = image.convert()
                    else:
                        image = image.convert_alpha()
                    self.images[key] = image
                    logging.info(f"Loaded local image: {key}")
                    return
            
            # Skip if no URL provided
            if not url:
                logging.info(f"No URL provided for {key}")
                self.images[key] = None
                return
            
            # Handle different URL types
            if url.startswith('data:'):
                image = self.load_image_from_data_url(url)
                if image:
                    self.images[key] = image
                    logging.info(f"Loaded image from data URL: {key}")
                    return
                else:
                    logging.warning(f"Failed to load data URL for {key}")
                    self.images[key] = None
                    return
            
            elif url.startswith(('http://', 'https://')):
                image = self.load_image_from_url(url)
                if image:
                    self.images[key] = image
                    logging.info(f"Loaded image from web URL: {key}")
                    return
                else:
                    logging.warning(f"Failed to load web URL for {key}")
                    self.images[key] = None
                    return
            
            elif os.path.exists(url):
                image = pg.image.load(url)
                if image.get_alpha() is None:
                    image = image.convert()
                else:
                    image = image.convert_alpha()
                self.images[key] = image
                logging.info(f"Loaded image from file path: {key}")
                return
            
            logging.warning(f"Could not load image {key} from URL: {url}")
            self.images[key] = None
            
        except Exception as e:
            logging.warning(f"Failed to load image {key}: {e}")
            self.images[key] = None
    
    def get_image(self, key, fallback_surface=None):
        """Get an image, return fallback surface if image not available"""
        if key in self.images and self.images[key] is not None:
            return self.images[key]
        return fallback_surface
    
    def get_animation(self, key):
        """Get an animation object"""
        return self.animations.get(key)
    
    def update_animations(self):
        """Update all animations"""
        for animation in self.animations.values():
            animation.update()
    
    def is_loading(self):
        """Check if images are still loading"""
        return not self.loading_complete
    
    def get_loading_progress(self):
        """Get current loading progress as a percentage (0.0 to 1.0)"""
        return self.loading_progress
    
    def get_loading_percentage(self):
        """Get current loading progress as a percentage string"""
        return f"{int(self.loading_progress * 100)}%"
    
    def use_fallbacks(self):
        """Check if we should use fallback shapes"""
        return self.fallback_mode or not self.loading_complete

class VisualEffect:
    """Handles visual effects like explosions and shattering"""
    
    def __init__(self, x, y, effect_type, image_manager):
        self.x = x
        self.y = y
        self.effect_type = effect_type
        self.image_manager = image_manager
        self.animation = image_manager.get_animation(f'effect_{effect_type}')
        
        if self.animation:
            self.animation.reset()
        
        self.active = True
        self.scale_factor = random.uniform(0.8, 1.2)  # Random size variation
    
    def update(self):
        """Update effect animation"""
        if not self.active:
            return True
        
        if self.animation:
            self.animation.update()
            if self.animation.is_finished():
                self.active = False
                return True
        else:
            # Fallback timer for effects without animations
            self.active = False
            return True
        
        return False
    
    def draw(self, surface):
        """Draw the visual effect"""
        if not self.active:
            return
        
        if self.animation:
            frame = self.animation.get_current_frame()
            if frame:
                # Scale the effect
                scale_x = SCREEN_WIDTH / BASE_WIDTH
                scale_y = SCREEN_HEIGHT / BASE_HEIGHT
                base_size = max(20, int(40 * min(scale_x, scale_y)))
                size = int(base_size * self.scale_factor)
                
                scaled_frame = pg.transform.scale(frame, (size, size))
                rect = scaled_frame.get_rect(center=(int(self.x), int(self.y)))
                surface.blit(scaled_frame, rect.topleft)
        else:
            # Fallback visual for effects without animations
            scale_x = SCREEN_WIDTH / BASE_WIDTH
            scale_y = SCREEN_HEIGHT / BASE_HEIGHT
            size = max(10, int(20 * min(scale_x, scale_y)))
            
            if self.effect_type == 'shatter':
                # Draw simple shatter pattern
                pg.draw.circle(surface, (200, 200, 200), (int(self.x), int(self.y)), size)
                for i in range(8):
                    angle = i * math.pi / 4
                    end_x = self.x + math.cos(angle) * size
                    end_y = self.y + math.sin(angle) * size
                    pg.draw.line(surface, (255, 255, 255), (int(self.x), int(self.y)), (int(end_x), int(end_y)), 2)
            
            elif self.effect_type == 'explosion':
                # Draw simple explosion
                pg.draw.circle(surface, (255, 100, 0), (int(self.x), int(self.y)), size)
                pg.draw.circle(surface, (255, 200, 0), (int(self.x), int(self.y)), size // 2)

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

# BOTTLE CONFIGURATION SYSTEM

class BottleTypeConfig:
    def __init__(self):
        # Default bottle configurations
        self.bottle_types = {
            1: {
                'name': 'Ground bottle',
                'color': (200, 0, 0),  # RED
                'width': 5,
                'height': 15,
                'min_curve': 0.0,
                'max_curve': 0.0,
                'score_gain': 10,
                'behavior': 'ground'
            },
            2: {
                'name': 'Air bottle',
                'color': (0, 100, 255),  # BLUE
                'width': 5,
                'height': 15,
                'min_curve': 0.0,
                'max_curve': 0.0,
                'score_gain': 15,
                'behavior': 'air'
            },
            3: {
                'name': 'Curved bottle',
                'color': (255, 165, 0),  # ORANGE
                'width': 6,
                'height': 18,
                'min_curve': 0.3,
                'max_curve': 0.8,
                'score_gain': 25,
                'behavior': 'ground'
            },
            4: {
                'name': 'Glass bottle',
                'color': (200, 255, 200),  # LIGHT GREEN
                'width': 4,
                'height': 12,
                'min_curve': 0.0,
                'max_curve': 0.2,
                'score_gain': 5,
                'behavior': 'ground',
                'special_effect': 'shatter'
            },
            5: {
                'name': 'Molotov',
                'color': (255, 0, 255),  # MAGENTA
                'width': 7,
                'height': 20,
                'min_curve': 0.1,
                'max_curve': 0.4,
                'score_gain': 50,
                'behavior': 'ground',
                'special_effect': 'explosion'
            },
            6: {
                'name': 'Sugar glass bottle',
                'color': (255, 255, 0),  # YELLOW
                'width': 5,
                'height': 15,
                'min_curve': 0.0,
                'max_curve': 0.1,
                'score_gain': 8,
                'behavior': 'ground'
            },
            7: {
                'name': 'Leak bottle',
                'color': (0, 255, 255),  # CYAN
                'width': 6,
                'height': 16,
                'min_curve': 0.2,
                'max_curve': 0.6,
                'score_gain': 20,
                'behavior': 'air'
            },
            8: {
                'name': 'Pill bottle',
                'color': (255, 255, 255),  # WHITE
                'width': 4,
                'height': 10,
                'min_curve': 0.0,
                'max_curve': 0.3,
                'score_gain': 12,
                'behavior': 'ground'
            },
            9: {
                'name': 'Ink bottle',
                'color': (0, 0, 0),  # BLACK
                'width': 5,
                'height': 14,
                'min_curve': 0.1,
                'max_curve': 0.5,
                'score_gain': 18,
                'behavior': 'air'
            },
            10: {
                'name': 'Hourglass bottle',
                'color': (139, 69, 19),  # BROWN
                'width': 6,
                'height': 18,
                'min_curve': 0.0,
                'max_curve': 0.4,
                'score_gain': 22,
                'behavior': 'ground'
            },
            11: {
                'name': 'Caffeine',
                'color': (128, 0, 128),  # PURPLE
                'width': 4,
                'height': 12,
                'min_curve': 0.2,
                'max_curve': 0.7,
                'score_gain': 30,
                'behavior': 'air'
            },
            12: {
                'name': 'Gold bottle',
                'color': (255, 215, 0),  # GOLD
                'width': 7,
                'height': 21,
                'min_curve': 0.1,
                'max_curve': 0.3,
                'score_gain': 100,
                'behavior': 'ground'
            },
            13: {
                'name': 'Star bottle',
                'color': (255, 20, 147),  # DEEP PINK
                'width': 8,
                'height': 24,
                'min_curve': 0.5,
                'max_curve': 1.2,
                'score_gain': 75,
                'behavior': 'air'
            },
            14: {
                'name': 'Ghost',
                'color': (192, 192, 192),  # SILVER
                'width': 6,
                'height': 16,
                'min_curve': 0.3,
                'max_curve': 0.9,
                'score_gain': 40,
                'behavior': 'air'
            },
            15: {
                'name': 'Prankster',
                'color': (255, 105, 180),  # HOT PINK
                'width': 5,
                'height': 17,
                'min_curve': 0.4,
                'max_curve': 1.0,
                'score_gain': 35,
                'behavior': 'ground'
            }
        }
        
        # Spawn weights for random bottle selection
        self.spawn_weights = {
            1: 30,   # Ground bottle - common
            2: 25,   # Air bottle - common
            3: 15,   # Curved bottle - uncommon
            4: 10,   # Glass bottle - uncommon
            5: 2,    # Molotov - rare
            6: 12,   # Sugar glass - uncommon
            7: 8,    # Leak bottle - uncommon
            8: 15,   # Pill bottle - uncommon
            9: 8,    # Ink bottle - uncommon
            10: 6,   # Hourglass bottle - uncommon
            11: 5,   # Caffeine - uncommon
            12: 1,   # Gold bottle - very rare
            13: 2,   # Star bottle - rare
            14: 3,   # Ghost - rare
            15: 4    # Prankster - rare
        }
        
        self.config_file = "bottle_config.json"
        self.load_config()
    
    def get_bottle_config(self, bottle_id):
        """Get configuration for a specific bottle type"""
        return self.bottle_types.get(bottle_id, self.bottle_types[1])
    
    def get_random_bottle_type(self):
        """Get random bottle type based on spawn weights"""
        bottle_ids = list(self.spawn_weights.keys())
        weights = list(self.spawn_weights.values())
        return random.choices(bottle_ids, weights=weights, k=1)[0]
    
    def save_config(self):
        """Save bottle configuration to file"""
        try:
            with open(self.config_file, 'w') as f:
                json.dump({
                    'bottle_types': self.bottle_types,
                    'spawn_weights': self.spawn_weights
                }, f, indent=2)
            logging.info("Bottle configuration saved")
        except Exception as e:
            logging.error(f"Failed to save bottle config: {e}")
    
    def load_config(self):
        """Load bottle configuration from file"""
        try:
            if os.path.exists(self.config_file):
                with open(self.config_file, 'r') as f:
                    data = json.load(f)
                    if 'bottle_types' in data:
                        # Update existing types with saved data
                        for bottle_id, config in data['bottle_types'].items():
                            if int(bottle_id) in self.bottle_types:
                                self.bottle_types[int(bottle_id)].update(config)
                    if 'spawn_weights' in data:
                        self.spawn_weights.update({int(k): v for k, v in data['spawn_weights'].items()})
                logging.info("Bottle configuration loaded")
        except Exception as e:
            logging.error(f"Failed to load bottle config: {e}")

# GAME MANAGEMENT CLASSES

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
    
    def add_default_scores(self):
        """Add default scores for testing"""
        default_scores = [
            {"username": "Player1", "score": 15000},
            {"username": "Player2", "score": 12500},
            {"username": "Player3", "score": 11000},
            {"username": "Player4", "score": 9500},
            {"username": "Player5", "score": 8200},
            {"username": "Player6", "score": 7800},
            {"username": "Player7", "score": 6500},
            {"username": "Player8", "score": 5900},
            {"username": "Player9", "score": 5200},
            {"username": "Player10", "score": 4800},
            {"username": "Player11", "score": 4200},
            {"username": "Player12", "score": 3800},
            {"username": "Player13", "score": 3400},
            {"username": "Player14", "score": 3100},
            {"username": "Player15", "score": 2800},
            {"username": "Player16", "score": 2500},
            {"username": "Player17", "score": 2200},
            {"username": "Player18", "score": 1900},
            {"username": "Player19", "score": 1600},
            {"username": "Player20", "score": 1300}
        ]
        
        # Only add if no scores exist
        if len(self.scores) == 0:
            self.scores = default_scores
            self.scores.sort(key=lambda x: x['score'], reverse=True)
            self.save_scores()
            logging.info("Added 20 default scores to leaderboard")

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
                    return True
                elif self.rect.collidepoint(mouse_x, mouse_y):
                    # Clicked on the track -> jump thumb toward click
                    track_range = self.rect.height - self.thumb_height
                    if track_range > 0:
                        # Calculate click position relative to track
                        click_y = mouse_y - self.rect.y
                        scroll_progress = click_y / self.rect.height
                        new_scroll = int(scroll_progress * self.max_scroll)
                        self.scroll_position = max(0, min(self.max_scroll, new_scroll))
                        self.update_thumb()
                        return True
            elif event.button == 4:  # Mouse wheel up
                self.scroll_position = max(0, self.scroll_position - 1)
                self.update_thumb()
                return True
            elif event.button == 5:  # Mouse wheel down
                self.scroll_position = min(self.max_scroll, self.scroll_position + 1)
                self.update_thumb()
                return True

        elif event.type == pg.MOUSEBUTTONUP:
            if event.button == 1:
                was_dragging = self.dragging
                self.dragging = False
                return was_dragging

        elif event.type == pg.MOUSEMOTION:
            if self.dragging:
                mouse_y = event.pos[1]
                # Move thumb with mouse, respecting drag offset
                new_thumb_y = mouse_y - self.drag_offset
                # Constrain thumb to track
                track_range = self.rect.height - self.thumb_height
                new_thumb_y = max(self.rect.y, min(self.rect.y + track_range, new_thumb_y))
                # Map thumb position -> scroll position
                if track_range > 0:
                    scroll_progress = (new_thumb_y - self.rect.y) / track_range
                    self.scroll_position = int(scroll_progress * self.max_scroll)
                    self.scroll_position = max(0, min(self.max_scroll, self.scroll_position))
                    self.update_thumb()
                return True

        elif event.type == pg.MOUSEWHEEL:
            # Handle mouse wheel scrolling (pygame 2.0+)
            if event.y > 0:  # Scroll up
                self.scroll_position = max(0, self.scroll_position - 1)
                self.update_thumb()
                return True
            elif event.y < 0:  # Scroll down
                self.scroll_position = min(self.max_scroll, self.scroll_position + 1)
                self.update_thumb()
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
        
        # Draw scroll indicators (arrows) if there's room
        if self.rect.height > 40:
            # Up arrow
            up_arrow_y = self.rect.y + 5
            up_arrow_points = [
                (self.rect.centerx, up_arrow_y),
                (self.rect.centerx - 4, up_arrow_y + 6),
                (self.rect.centerx + 4, up_arrow_y + 6)
            ]
            pg.draw.polygon(surface, GRAY, up_arrow_points)
            
            # Down arrow
            down_arrow_y = self.rect.bottom - 11
            down_arrow_points = [
                (self.rect.centerx, down_arrow_y + 6),
                (self.rect.centerx - 4, down_arrow_y),
                (self.rect.centerx + 4, down_arrow_y)
            ]
            pg.draw.polygon(surface, GRAY, down_arrow_points)

class Button:
    def __init__(self, x, y, width, height, text, font, color=None, hover_color=None, text_key=None):
        self.rect = pg.Rect(x, y, width, height)
        self.text = text
        self.text_key = text_key  # Optional image key for text replacement
        self.font = font
        self.color = color or WHITE
        self.hover_color = hover_color or BLUE
        self.is_hovered = False
        
        # Image manager reference (will be set globally)
        self.image_manager = None
    
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
        # Try to use images if available
        if (self.image_manager and 
            not self.image_manager.use_fallbacks()):
            
            # Get appropriate button image
            if self.is_hovered:
                button_img = self.image_manager.get_image('button_hover')
            else:
                button_img = self.image_manager.get_image('button_normal')
            
            if button_img:
                # Scale image to button size
                scaled_img = pg.transform.scale(button_img, (self.rect.width, self.rect.height))
                surface.blit(scaled_img, self.rect.topleft)
            else:
                # Fallback to drawn button
                self._draw_fallback(surface)
        else:
            # Use fallback drawn button
            self._draw_fallback(surface)
        
        # Draw text (try image first, then rendered text)
        if self.text_key:
            # Try to use text image
            text_img = self.image_manager.get_image(self.text_key) if self.image_manager else None
            if text_img:
                # Scale text image to fit button
                scale = min((self.rect.width - 20) / text_img.get_width(), 
                           (self.rect.height - 10) / text_img.get_height())
                new_width = int(text_img.get_width() * scale)
                new_height = int(text_img.get_height() * scale)
                scaled_text = pg.transform.scale(text_img, (new_width, new_height))
                text_rect = scaled_text.get_rect(center=self.rect.center)
                surface.blit(scaled_text, text_rect)
                return
        
        # Fallback to rendered text
        text_color = self.hover_color if self.is_hovered else self.color
        text_surface = self.font.render(self.text, True, text_color)
        text_rect = text_surface.get_rect(center=self.rect.center)
        surface.blit(text_surface, text_rect)
    
    def _draw_fallback(self, surface):
        """Draw fallback button when images aren't available"""
        color = self.hover_color if self.is_hovered else self.color
        pg.draw.rect(surface, DARK_GRAY, self.rect)
        pg.draw.rect(surface, color, self.rect, 3)

# GAME OBJECTS

class Bottle:
    def __init__(self, start_x, start_y, target_x, target_y, bottle_type_id=1, hand="right", is_preview_transition=False):
        # Get current scaling factors
        scale_x = SCREEN_WIDTH / BASE_WIDTH
        scale_y = SCREEN_HEIGHT / BASE_HEIGHT
        
        self.start_x = start_x
        self.start_y = start_y
        self.x = start_x
        self.y = start_y
        self.hand = hand  # Which hand threw this bottle
        self.is_preview_transition = is_preview_transition  # New flag for preview bottles
        
        # Get bottle configuration
        self.bottle_type_id = bottle_type_id
        self.config = bottle_config.get_bottle_config(bottle_type_id)
        self.bottle_type = self.config['behavior']  # "ground" or "air"
        self.name = self.config['name']
        
        # Target positioning based on bottle type
        if self.bottle_type == "air":
            # Air bottles target the jumping z-plane - ensure they pass through player's Y position
            self.target_x = target_x
            self.target_y = target_y  # Keep original target Y to ensure bottles pass through player
            self.target_z = 2.5  # Much higher target to ensure bottles travel far past player
        else:
            # Ground bottles target the ground z-plane
            self.target_x = target_x
            self.target_y = target_y
            self.target_z = 2.0  # Much higher target to ensure bottles travel far past player
        
        # Z-axis properties for enhanced 3D effect
        if is_preview_transition:
            # Preview bottles start at a small but visible z to maintain visibility
            self.z = 0.05
        else:
            self.z = 0.2  # Start closer to prevent instant teleporting
        
        # Hand-specific properties with bottle-specific curve values
        if hand == "left":
            self.z_speed = 0.015  # Faster movement for left hand
            # Use bottle-specific curve values
            if self.config['max_curve'] > 0:
                self.curve_strength = random.uniform(self.config['min_curve'], self.config['max_curve'])
                self.curve_direction = random.choice([-1, 1])  # Left or right curve
                self.curve_peak_z = random.uniform(0.4, 0.8)  # Where the curve peaks
            else:
                self.curve_strength = 0
                self.curve_direction = 0
                self.curve_peak_z = 0
        else:
            self.z_speed = 0.02  # Faster speed for right hand
            # Right hand can also have curves now based on bottle config
            if self.config['max_curve'] > 0:
                self.curve_strength = random.uniform(self.config['min_curve'], self.config['max_curve'])
                self.curve_direction = random.choice([-1, 1])
                self.curve_peak_z = random.uniform(0.4, 0.8)
            else:
                self.curve_strength = 0
                self.curve_direction = 0
                self.curve_peak_z = 0
        
        # Calculate movement per frame - ensure smooth movement
        # Account for the 3x speed multiplier used in update()
        actual_z_speed = self.z_speed * 3
        self.total_frames = max(30, int((self.target_z - self.z) / actual_z_speed))  # Faster movement
        if self.total_frames > 0:
            self.dx = (self.target_x - self.start_x) / self.total_frames
            self.dy = (self.target_y - self.start_y) / self.total_frames
        else:
            self.dx = self.dy = 0
        
        # Visual properties - scaled dynamically using bottle config
        self.base_width = max(1, int(self.config['width'] * scale_x))
        self.base_height = max(1, int(self.config['height'] * scale_y))
        self.rotation = 0
        self.rotation_speed = random.uniform(7, 10)
        
        # Create bottle surface with bottle-specific color
        self.original_image = pg.Surface((self.base_width, self.base_height), pg.SRCALPHA)
        self.original_image.fill(self.config['color'])
        
        # Image manager reference (will be set globally)
        self.image_manager = None
        
        self.active = True
        self.hit_player = False  # Track if bottle hit player
        self.scored = False  # Track if bottle has been scored for dodging
        self.frame_count = 0  # Track frames for smooth movement

    def update(self):
        """Update bottle position and state"""
        if not self.active:
            return True
        
        self.frame_count += 1
        
        # Move along z-axis (simulating depth) - faster movement
        self.z += self.z_speed * 3  # Triple the z-speed for faster movement
        
        # Calculate curve offset for bottles with curve properties
        curve_offset_x = 0
        if self.curve_strength > 0:
            # Create a curved trajectory using sine wave
            progress = self.z / self.target_z
            if progress <= 1.0:
                # Peak curve at curve_peak_z
                curve_progress = min(1.0, progress / self.curve_peak_z) if self.curve_peak_z > 0 else progress
                curve_offset_x = math.sin(curve_progress * math.pi) * self.curve_strength * self.curve_direction * SCREEN_WIDTH * 0.1
        
        # Move towards target position (with curve if applicable)
        self.x += self.dx + (curve_offset_x * 0.05)  # Apply curve more smoothly
        self.y += self.dy
        
        # Update rotation
        self.rotation = (self.rotation + self.rotation_speed) % 360
        
        # Remove bottle if it has gone past the target z
        if self.z >= self.target_z + 0.05:  # Smaller buffer past target
            return True
        
        # Check if bottle is completely off-screen with better scaling (50% smaller)
        scale_factor = (self.z ** 1.2) * (4 * min(SCREEN_WIDTH / BASE_WIDTH, SCREEN_HEIGHT / BASE_HEIGHT))  # Reduced from 8 to 4 (50% smaller)
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
        
        # Calculate size based on z-position - scaled dynamically with better scaling
        # Make bottles 50% smaller by reducing the scaling factor
        scale_factor = (self.z ** 1.2) * (4 * min(SCREEN_WIDTH / BASE_WIDTH, SCREEN_HEIGHT / BASE_HEIGHT))  # Reduced from 8 to 4 (50% smaller)
        scale_factor = max(scale_factor, 0.1)
        
        current_width = max(int(self.base_width * scale_factor), 1)
        current_height = max(int(self.base_height * scale_factor), 1)
        
        # Try to use bottle image if available
        if (self.image_manager and 
            not self.image_manager.use_fallbacks()):
            
            bottle_img = self.image_manager.get_image(f'bottle_{self.bottle_type_id}')
            if bottle_img:
                # Scale and rotate the bottle image
                scaled_image = pg.transform.scale(bottle_img, (current_width, current_height))
                rotated_image = pg.transform.rotate(scaled_image, self.rotation)
            else:
                # Fallback to colored rectangle
                scaled_image = pg.transform.scale(self.original_image, (current_width, current_height))
                rotated_image = pg.transform.rotate(scaled_image, self.rotation)
        else:
            # Use fallback colored rectangle
            scaled_image = pg.transform.scale(self.original_image, (current_width, current_height))
            rotated_image = pg.transform.rotate(scaled_image, self.rotation)
        
        # Position the bottle
        rect = rotated_image.get_rect(center=(int(self.x), int(self.y)))
        
        # Only draw if on screen and bottle is visible
        if (rect.right > 0 and rect.left < SCREEN_WIDTH and 
            rect.bottom > 0 and rect.top < SCREEN_HEIGHT and
            current_width > 0 and current_height > 0):
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
            return (self.z >= 1.4 and self.z <= 1.8)  # Expanded air collision zone
        elif not player_is_jumping and self.bottle_type == "ground":
            return (self.z >= 1.4 and self.z <= 1.8)  # Expanded ground collision zone
        
        return False

    def get_collision_rect(self, player_is_jumping):
        """Get collision rectangle for bottles in the player's depth zone"""
        if not self.active or not self.is_in_player_collision_zone(player_is_jumping):
            return pg.Rect(0, 0, 0, 0)
        
        # Use exact same scaling logic as visual drawing (50% smaller)
        scale_factor = (self.z ** 1.2) * (4 * min(SCREEN_WIDTH / BASE_WIDTH, SCREEN_HEIGHT / BASE_HEIGHT))  # Reduced from 8 to 4 (50% smaller)
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
    
    def create_impact_effect(self):
        """Create visual effect when bottle impacts"""
        special_effect = self.config.get('special_effect')
        if special_effect in ['shatter', 'explosion']:
            effect = VisualEffect(self.x, self.y, special_effect, self.image_manager)
            return effect
        return None

# UTILITY FUNCTIONS

def set_image_urls(urls_dict):
    """Set image URLs from external source"""
    global IMAGE_URLS
    
    # Update single images
    single_keys = ['background_menu', 'background_game', 'background_settings', 
                   'background_leaderboard', 'text_title', 'text_play', 'text_settings',
                   'text_leaderboard', 'text_quit', 'text_back', 'text_game_over',
                   'button_normal', 'button_hover']
    
    for key in single_keys:
        if key in urls_dict:
            IMAGE_URLS[key] = urls_dict[key]
    
    # Update animation sequences
    animation_keys = ['player_idle', 'player_run', 'player_jump', 
                     'drunk_idle', 'drunk_left_throw', 'drunk_right_throw',
                     'effect_shatter', 'effect_explosion']
    
    for key in animation_keys:
        if key in urls_dict and isinstance(urls_dict[key], list):
            IMAGE_URLS[key] = urls_dict[key]
    
    # Update bottles
    if 'bottles' in urls_dict:
        for bottle_id, url in urls_dict['bottles'].items():
            if bottle_id in IMAGE_URLS['bottles']:
                IMAGE_URLS['bottles'][bottle_id] = url

def create_fallback_surface(width, height, color, shape='rect'):
    """Create a fallback surface when images fail to load"""
    surface = pg.Surface((width, height), pg.SRCALPHA)
    
    if shape == 'rect':
        pg.draw.rect(surface, color, (0, 0, width, height))
        pg.draw.rect(surface, (max(0, color[0] - 50), max(0, color[1] - 50), max(0, color[2] - 50)), 
                    (0, 0, width, height), 2)
    elif shape == 'circle':
        pg.draw.circle(surface, color, (width//2, height//2), min(width, height)//2)
        pg.draw.circle(surface, (max(0, color[0] - 50), max(0, color[1] - 50), max(0, color[2] - 50)), 
                      (width//2, height//2), min(width, height)//2, 2)
    
    return surface

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

def toggle_fullscreen():
    """Toggle fullscreen mode safely"""
    global is_fullscreen, screen, SCREEN_WIDTH, SCREEN_HEIGHT
    
    try:
        if is_fullscreen:
            # Switch to windowed mode
            screen = pg.display.set_mode((BASE_WIDTH, BASE_HEIGHT), pg.RESIZABLE)
            is_fullscreen = False
            logging.info("Switched to windowed mode")
        else:
            # Switch to fullscreen mode
            screen = pg.display.set_mode((0, 0), pg.FULLSCREEN)
            is_fullscreen = True
            logging.info("Switched to fullscreen mode")
        
        # Update screen dimensions after mode change
        SCREEN_WIDTH = screen.get_width()
        SCREEN_HEIGHT = screen.get_height()
        update_screen_dimensions(SCREEN_WIDTH, SCREEN_HEIGHT)
        
        # Recreate fade surface with new dimensions
        global fade_surface
        fade_surface = pg.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
        fade_surface.fill((0, 0, 0))
        
        return True
        
    except Exception as e:
        logging.error(f"Failed to toggle fullscreen: {e}")
        return False

def update_screen_dimensions(width, height):
    """Update screen dimensions and related variables"""
    global SCREEN_WIDTH, SCREEN_HEIGHT, fade_surface
    
    SCREEN_WIDTH = width
    SCREEN_HEIGHT = height
    
    # Recreate fade surface
    fade_surface = pg.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
    fade_surface.fill((0, 0, 0))
    
    # Update scaled values
    get_scaled_values()
    
    logging.info(f"Screen dimensions updated to {SCREEN_WIDTH}x{SCREEN_HEIGHT}")

def get_scaled_values():
    """Calculate scaled values based on current screen size"""
    global player_width, player_height, player_base_y, drunk_width, drunk_height, drunk_y
    global player_speed, jump_power, gravity
    
    scale_x = SCREEN_WIDTH / BASE_WIDTH
    scale_y = SCREEN_HEIGHT / BASE_HEIGHT
    
    # Player dimensions - scaled
    player_width = max(60, int(120 * scale_x))
    player_height = max(40, int(80 * scale_y))
    player_base_y = SCREEN_HEIGHT - max(100, int(150 * scale_y))
    
    # Drunk guy dimensions - scaled
    drunk_width = max(125, int(200 * scale_x))
    drunk_height = max(120, int(240 * scale_y))
    drunk_y = max(100, int(200 * scale_y))
    
    # Physics - scaled to maintain consistent gameplay feel
    player_speed = max(3, int(5 * scale_x))
    jump_power = max(-16, int(-12 * scale_y / BASE_HEIGHT * 600))  # Negative because up is negative
    gravity = max(0.3, 0.5 * scale_y / BASE_HEIGHT * 600)

def get_current_difficulty():
    """Calculate current difficulty based on score"""
    difficulty_level = score // DIFFICULTY_INCREASE_INTERVAL
    # Calculate spawn time: start at 1000ms, decrease by 80ms per level, min 200ms
    current_spawn_time = max(MIN_SPAWN_TIME, 1000 - (difficulty_level * 80))
    # Left hand spawn time (always slower)
    left_spawn_time = max(MIN_LEFT_SPAWN_TIME, 1500 - (difficulty_level * 60))
    return current_spawn_time, left_spawn_time

def add_score_popup(x, y, points, is_close_call=False, combo_mult=1.0, bottle_name=""):
    """Add a visual score popup"""
    global score_popups
    
    # Determine popup text and color
    if is_close_call:
        text = f"CLOSE CALL! +{points}"
        color = RED
    elif combo_mult > 1.0:
        text = f"{bottle_name} +{points} (x{combo_mult:.1f})"
        color = BLUE
    else:
        text = f"{bottle_name} +{points}"
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

def reset_game():
    """Reset all game variables for a new game"""
    global player_x, player_y, vel_y, is_on_ground, drunk_x, lives, start_time, last_bottle_time, bottles
    global score, bottles_dodged, close_calls, combo_multiplier, score_popups
    global bottle_spawn_time, left_hand_spawn_time, last_left_bottle_time
    global visual_effects, player_jumping, drunk_current_animation
    global left_hand_preview, right_hand_preview, left_hand_preview_time, right_hand_preview_time
    global player_facing_right, player_last_direction
    
    # Recalculate scaled values in case screen size changed
    get_scaled_values()
    
    player_x = SCREEN_WIDTH // 2 - player_width // 2
    player_y = player_base_y
    vel_y = 0
    is_on_ground = False
    drunk_x = SCREEN_WIDTH // 2 - drunk_width // 2  # Drunk guy stays centered
    lives = 9
    last_bottle_time = pg.time.get_ticks()
    last_left_bottle_time = pg.time.get_ticks()
    bottles = []
    
    # Reset hand preview system
    left_hand_preview = None
    right_hand_preview = None
    left_hand_preview_time = 0
    right_hand_preview_time = 0
    
    # Reset player direction
    player_facing_right = True
    player_last_direction = "right"
    
    # Reset scoring system
    score = 0
    bottles_dodged = 0
    close_calls = 0
    combo_multiplier = 1.0
    score_popups = []
    
    # Reset difficulty
    bottle_spawn_time = 1000  # Start with 1 second spawn time for right hand
    left_hand_spawn_time = 1500  # Start with 1.5 second spawn time for left hand
    
    # Reset visual effects and animations
    visual_effects = []
    player_jumping = False
    drunk_current_animation = 'drunk_idle'
    
    # Reset animations
    if image_manager:
        for anim_key in ['player_idle', 'player_run', 'player_jump', 'drunk_idle']:
            anim = image_manager.get_animation(anim_key)
            if anim:
                anim.reset()

def calculate_final_score():
    """Calculate final score without time bonus"""
    global final_score
    final_score = score  # No time bonus - just the base score
    logging.info(f"Final score: {final_score}")

# DRAWING AND UI FUNCTIONS

def draw_background(surface, bg_type='menu'):
    """Draw background image or fallback"""
    bg_key = f'background_{bg_type}'
    bg_img = image_manager.get_image(bg_key)
    
    if bg_img:
        # Scale background to screen size
        scaled_bg = pg.transform.scale(bg_img, (SCREEN_WIDTH, SCREEN_HEIGHT))
        surface.blit(scaled_bg, (0, 0))
    else:
        # Fallback to solid color
        if bg_type == 'menu':
            surface.fill((20, 20, 40))  # Dark blue
        elif bg_type == 'game':
            surface.fill(BLACK)
        elif bg_type == 'settings':
            surface.fill((40, 20, 20))  # Dark red
        elif bg_type == 'leaderboard':
            surface.fill((20, 40, 20))  # Dark green
        else:
            surface.fill(BLACK)

def draw_text_or_image(surface, text_key, fallback_text, font, color, pos, center=True):
    """Draw text image if available, otherwise render text"""
    text_img = image_manager.get_image(text_key)
    
    if text_img:
        # Scale text image appropriately
        scale = min(SCREEN_WIDTH / BASE_WIDTH, SCREEN_HEIGHT / BASE_HEIGHT)
        img_width = int(text_img.get_width() * scale * 0.8)  # Slightly smaller than full scale
        img_height = int(text_img.get_height() * scale * 0.8)
        scaled_img = pg.transform.scale(text_img, (img_width, img_height))
        
        if center:
            rect = scaled_img.get_rect(center=pos)
        else:
            rect = scaled_img.get_rect(topleft=pos)
        
        surface.blit(scaled_img, rect)
        return rect
    else:
        # Fallback to rendered text
        text_surface = font.render(fallback_text, True, color)
        if center:
            rect = text_surface.get_rect(center=pos)
        else:
            rect = text_surface.get_rect(topleft=pos)
        
        surface.blit(text_surface, rect)
        return rect

def draw_player_with_depth(surface, x, y, width, height, is_jumping, image_manager=None):
    """Draw player with visual depth representation based on jumping state (fallback)"""
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

def update_player_animation_state():
    """Update player animation state based on movement"""
    global player_moving, player_jumping, player_on_ground_last_frame
    
    keys = pg.key.get_pressed()
    player_moving = keys[pg.K_LEFT] or keys[pg.K_a] or keys[pg.K_RIGHT] or keys[pg.K_d]
    
    # Detect jump start
    if is_on_ground and not player_on_ground_last_frame:
        # Just landed - could trigger landing animation
        pass
    elif not is_on_ground and player_on_ground_last_frame:
        # Just started jumping
        player_jumping = True
        # Reset jump animation
        player_jump_anim = image_manager.get_animation('player_jump')
        if player_jump_anim:
            player_jump_anim.reset()
    
    player_on_ground_last_frame = is_on_ground

def draw_animated_player(surface, x, y, width, height):
    """Draw player with proper animations and direction"""
    global player_jumping, player_facing_right
    
    # Determine which animation to use
    current_frame = None
    
    if not is_on_ground:
        # Jumping animation
        jump_anim = image_manager.get_animation('player_jump')
        if jump_anim:
            current_frame = jump_anim.get_current_frame()
            # Reset jumping flag when animation finishes
            if jump_anim.is_finished():
                player_jumping = False
    
    elif player_moving:
        # Running animation
        run_anim = image_manager.get_animation('player_run')
        if run_anim:
            current_frame = run_anim.get_current_frame()
    
    else:
        # Idle animation
        idle_anim = image_manager.get_animation('player_idle')
        if idle_anim:
            current_frame = idle_anim.get_current_frame()
    
    if current_frame:
        # Scale the frame
        scaled_frame = pg.transform.scale(current_frame, (width, height))
        
        # Apply depth effect when jumping
        if not is_on_ground:
            scaled_frame.set_alpha(180)
        
        # Flip the frame based on direction
        if not player_facing_right:
            scaled_frame = pg.transform.flip(scaled_frame, True, False)
        
        rect = scaled_frame.get_rect(center=(int(x + width//2), int(y + height//2)))
        surface.blit(scaled_frame, rect.topleft)
    else:
        # Fallback to old drawing method
        draw_player_with_depth(surface, x, y, width, height, not is_on_ground, image_manager)

def update_drunk_animation():
    """Update drunk guy animation state"""
    global drunk_current_animation, drunk_throwing_timer
    
    # Handle throwing animations
    if drunk_current_animation in ['drunk_left_throw', 'drunk_right_throw']:
        drunk_throwing_timer -= 1
        if drunk_throwing_timer <= 0:
            drunk_current_animation = 'drunk_idle'
            # Reset idle animation
            idle_anim = image_manager.get_animation('drunk_idle')
            if idle_anim:
                idle_anim.reset()

def trigger_drunk_throw(hand):
    """Trigger drunk guy throwing animation"""
    global drunk_current_animation, drunk_throwing_timer
    
    if hand == "left":
        drunk_current_animation = 'drunk_left_throw'
        # Reset left throw animation
        left_throw_anim = image_manager.get_animation('drunk_left_throw')
        if left_throw_anim:
            left_throw_anim.reset()
    else:
        drunk_current_animation = 'drunk_right_throw'
        # Reset right throw animation
        right_throw_anim = image_manager.get_animation('drunk_right_throw')
        if right_throw_anim:
            right_throw_anim.reset()
    
    drunk_throwing_timer = drunk_throw_duration

def draw_animated_drunk(surface, x, y, width, height):
    """Draw drunk guy with proper animations and separated hands"""
    # Always use idle animation for the main drunk guy
    idle_anim = image_manager.get_animation('drunk_idle')
    
    if idle_anim:
        frame = idle_anim.get_current_frame()
        if frame:
            scaled_frame = pg.transform.scale(frame, (width, height))
            rect = scaled_frame.get_rect(center=(int(x + width//2), int(y + height//2)))
            surface.blit(scaled_frame, rect.topleft)
        else:
            # Fallback to colored rectangle
            drunk_rect = pg.Rect(int(x), y, width, height)
            pg.draw.rect(surface, YELLOW, drunk_rect)
    else:
        # Fallback to colored rectangle
        drunk_rect = pg.Rect(int(x), y, width, height)
        pg.draw.rect(surface, YELLOW, drunk_rect)
    
    # Draw hand previews separately
    draw_hand_previews(surface, x, y, width, height)

def draw_hand_previews(surface, drunk_x, drunk_y, drunk_width, drunk_height):
    """Draw hand previews for bottle throws"""
    global left_hand_preview, right_hand_preview, left_hand_preview_time, right_hand_preview_time
    
    scale_x = SCREEN_WIDTH / BASE_WIDTH
    scale_y = SCREEN_HEIGHT / BASE_HEIGHT
    
    # Right hand position (right side of drunk guy)
    right_hand_x = drunk_x + drunk_width + max(10, int(15 * scale_x))
    right_hand_y = drunk_y + drunk_height // 3  # Upper part for right hand
    
    # Left hand position (left side of drunk guy)
    left_hand_x = drunk_x - max(15, int(20 * scale_x))
    left_hand_y = drunk_y + drunk_height // 3  # Upper part for left hand
    
    # Draw right hand preview
    if right_hand_preview is not None:
        preview_size = max(8, int(12 * min(scale_x, scale_y)))
        preview_rect = pg.Rect(right_hand_x, right_hand_y, preview_size, preview_size)
        
        # Try to use bottle image if available
        if (image_manager and not image_manager.use_fallbacks()):
            bottle_img = image_manager.get_image(f'bottle_{right_hand_preview["type_id"]}')
            if bottle_img:
                scaled_img = pg.transform.scale(bottle_img, (preview_size, preview_size))
                surface.blit(scaled_img, preview_rect.topleft)
            else:
                pg.draw.rect(surface, right_hand_preview['color'], preview_rect)
        else:
            pg.draw.rect(surface, right_hand_preview['color'], preview_rect)
    
    # Draw left hand preview
    if left_hand_preview is not None:
        preview_size = max(8, int(12 * min(scale_x, scale_y)))
        preview_rect = pg.Rect(left_hand_x, left_hand_y, preview_size, preview_size)
        
        # Try to use bottle image if available
        if (image_manager and not image_manager.use_fallbacks()):
            bottle_img = image_manager.get_image(f'bottle_{left_hand_preview["type_id"]}')
            if bottle_img:
                scaled_img = pg.transform.scale(bottle_img, (preview_size, preview_size))
                surface.blit(scaled_img, preview_rect.topleft)
            else:
                pg.draw.rect(surface, left_hand_preview['color'], preview_rect)
        else:
            pg.draw.rect(surface, left_hand_preview['color'], preview_rect)

def show_loading_screen():
    """Show animated loading screen while images are being loaded"""
    global loading_progress, loading_animation_timer
    
    screen.fill((0, 0, 0))
    
    # Try to use background image
    bg_img = image_manager.get_image('background_menu')
    if bg_img:
        scaled_bg = pg.transform.scale(bg_img, (SCREEN_WIDTH, SCREEN_HEIGHT))
        screen.blit(scaled_bg, (0, 0))
    
    # Title
    title_img = image_manager.get_image('text_title')
    if title_img:
        # Scale title image to appropriate size
        scale = min(SCREEN_WIDTH / BASE_WIDTH, SCREEN_HEIGHT / BASE_HEIGHT)
        title_width = int(title_img.get_width() * scale)
        title_height = int(title_img.get_height() * scale)
        scaled_title = pg.transform.scale(title_img, (title_width, title_height))
        title_rect = scaled_title.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 3))
        screen.blit(scaled_title, title_rect)
    else:
        # Fallback text
        title_text = font_large.render("BOTTLE OPS", True, (255, 255, 255))
        title_rect = title_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 3))
        screen.blit(title_text, title_rect)
    
    # Loading text
    loading_text = font_medium.render("Loading assets...", True, (0, 100, 255))
    loading_rect = loading_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))
    screen.blit(loading_text, loading_rect)
    
    # Animated progress bar
    progress_bar_width = int(SCREEN_WIDTH * 0.6)
    progress_bar_height = max(20, int(30 * SCREEN_HEIGHT / BASE_HEIGHT))
    progress_bar_x = (SCREEN_WIDTH - progress_bar_width) // 2
    progress_bar_y = SCREEN_HEIGHT // 2 + 50
    
    # Progress bar background
    pg.draw.rect(screen, (50, 50, 50), (progress_bar_x, progress_bar_y, progress_bar_width, progress_bar_height))
    pg.draw.rect(screen, (100, 100, 100), (progress_bar_x, progress_bar_y, progress_bar_width, progress_bar_height), 2)
    
    # Animated progress
    if image_manager.is_loading():
        # Get actual loading progress
        actual_progress = image_manager.get_loading_progress()
        
        # Draw actual progress bar
        progress_width = int(progress_bar_width * actual_progress)
        pg.draw.rect(screen, (0, 150, 255), (progress_bar_x, progress_bar_y, progress_width, progress_bar_height))
        
        # Show percentage text
        percentage_text = image_manager.get_loading_percentage()
        progress_text = font_small.render(f"Loading... {percentage_text}", True, (128, 128, 128))
        
        # Show spacebar skip option
        skip_text = font_small.render("Press SPACEBAR to skip loading", True, (255, 165, 0))  # Orange color
        skip_rect = skip_text.get_rect(center=(SCREEN_WIDTH // 2, progress_bar_y + progress_bar_height + 60))
        screen.blit(skip_text, skip_rect)
    else:
        # Show full progress bar when done
        pg.draw.rect(screen, (0, 255, 100), (progress_bar_x, progress_bar_y, progress_bar_width, progress_bar_height))
        progress_text = font_small.render("Press any key to continue", True, (0, 255, 100))
    
    progress_rect = progress_text.get_rect(center=(SCREEN_WIDTH // 2, progress_bar_y + progress_bar_height + 30))
    screen.blit(progress_text, progress_rect)
    
    pg.display.flip()

def show_menu():
    """Display the main menu with enhanced visuals"""
    draw_background(screen, 'menu')
    
    # Title with image support
    draw_text_or_image(screen, 'text_title', "BOTTLE OPS", font_large, WHITE, 
                      (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 4))
    
    # Buttons - dynamically scaled
    scale_x = SCREEN_WIDTH / BASE_WIDTH
    scale_y = SCREEN_HEIGHT / BASE_HEIGHT
    
    button_width = max(100, int(200 * scale_x))
    button_height = max(30, int(40 * scale_y))
    button_x = SCREEN_WIDTH // 2 - button_width // 2
    
    spacing = max(40, int(50 * scale_y))
    start_y = SCREEN_HEIGHT // 2 - max(80, int(100 * scale_y))
    
    play_button = Button(button_x, start_y, button_width, button_height, "PLAY", font_medium, hover_color=GREEN, text_key='text_play')
    settings_button = Button(button_x, start_y + spacing, button_width, button_height, "SETTINGS", font_medium, text_key='text_settings')
    bottle_config_button = Button(button_x, start_y + spacing * 2, button_width, button_height, "BOTTLE CONFIG", font_medium, hover_color=PURPLE)
    leaderboard_button = Button(button_x, start_y + spacing * 3, button_width, button_height, "LEADERBOARD", font_medium, hover_color=YELLOW, text_key='text_leaderboard')
    exit_button = Button(button_x, start_y + spacing * 4, button_width, button_height, "QUIT", font_medium, hover_color=RED, text_key='text_quit')
    
    # Set image manager for all buttons
    for button in [play_button, settings_button, bottle_config_button, leaderboard_button, exit_button]:
        button.image_manager = image_manager
    
    # Update hover states for all buttons
    mouse_pos = pg.mouse.get_pos()
    play_button.update_hover(mouse_pos)
    settings_button.update_hover(mouse_pos)
    bottle_config_button.update_hover(mouse_pos)
    leaderboard_button.update_hover(mouse_pos)
    exit_button.update_hover(mouse_pos)
    
    play_button.draw(screen)
    settings_button.draw(screen)
    bottle_config_button.draw(screen)
    leaderboard_button.draw(screen)
    exit_button.draw(screen)
    
    return play_button, settings_button, bottle_config_button, leaderboard_button, exit_button

def show_settings():
    """Display the settings menu with enhanced visuals"""
    draw_background(screen, 'settings')
    
    # Title with image support
    draw_text_or_image(screen, None, "SETTINGS", font_large, WHITE, 
                      (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 4))
    
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
        font_medium,
        hover_color=ORANGE,
        text_key='text_back'
    )
    
    # Update hover states
    mouse_pos = pg.mouse.get_pos()
    fs_button.update_hover(mouse_pos)
    back_button.update_hover(mouse_pos)
    
    # Set image manager for buttons
    fs_button.image_manager = image_manager
    back_button.image_manager = image_manager
    
    fs_button.draw(screen)
    back_button.draw(screen)    
    return fs_button, back_button

def show_bottle_config():
    """Display bottle configuration menu with scrollable list and enhanced visuals"""
    global bottle_config_scroll, bottle_config_scrollbar
    
    draw_background(screen, 'settings')
    
    # Title with image support
    draw_text_or_image(screen, None, "BOTTLE CONFIGURATION", font_large, WHITE,
                      (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 8))
    
    # Dynamic scaling
    scale_x = SCREEN_WIDTH / BASE_WIDTH
    scale_y = SCREEN_HEIGHT / BASE_HEIGHT
    
    # Define bottle list display area
    list_start_y = int(SCREEN_HEIGHT * 0.2)
    list_end_y = int(SCREEN_HEIGHT * 0.75)
    list_area_height = list_end_y - list_start_y
    line_spacing = max(25, int(35 * scale_y))
    
    # Calculate visible bottles
    max_visible_bottles = max(1, int(list_area_height // line_spacing))
    
    # Ensure bottle_config_scroll is initialized
    if bottle_config_scroll is None:
        bottle_config_scroll = 0
    
    # Create scrollbar for bottle list
    scrollbar_width = max(15, int(20 * scale_x))
    scrollbar_x = SCREEN_WIDTH - max(40, int(50 * scale_x))
    scrollbar_height = list_area_height
    
    # Always create a new scrollbar to avoid crashes
    bottle_config_scrollbar = ScrollBar(
        scrollbar_x,
        list_start_y,
        scrollbar_width,
        scrollbar_height,
        15,  # Total bottle types
        max_visible_bottles
    )
    bottle_config_scrollbar.set_scroll_position(bottle_config_scroll)
    
    # Draw bottle list
    visible_bottles = range(bottle_config_scroll + 1, min(16, bottle_config_scroll + max_visible_bottles + 1))
    
    for i, bottle_id in enumerate(visible_bottles):
        config = bottle_config.get_bottle_config(bottle_id)
        y_pos = list_start_y + i * line_spacing
        
        # Draw bottle preview (small colored rectangle or image)
        preview_size = max(8, int(12 * min(scale_x, scale_y)))
        preview_rect = pg.Rect(max(20, int(30 * scale_x)), y_pos, preview_size, preview_size)
        
        # Try to use bottle image if available
        if (image_manager and 
            not image_manager.use_fallbacks()):
            
            bottle_img = image_manager.get_image(f'bottle_{bottle_id}')
            if bottle_img:
                # Scale image to preview size
                scaled_img = pg.transform.scale(bottle_img, (preview_size, preview_size))
                screen.blit(scaled_img, preview_rect.topleft)
            else:
                # Fallback to colored rectangle
                pg.draw.rect(screen, config['color'], preview_rect)
        else:
            # Use fallback colored rectangle
            pg.draw.rect(screen, config['color'], preview_rect)
        
        # Draw bottle info
        text_x = preview_rect.right + max(10, int(15 * scale_x))
        bottle_text = f"{bottle_id}. {config['name']} - Score: {config['score_gain']} - Min curve: {config['min_curve']} - Max curve: {config['max_curve']} - H{config['height']} W{config['width']}"
        
        # Highlight if it has curve properties
        color = WHITE
        
        bottle_surface = font_small.render(bottle_text, True, color)
        screen.blit(bottle_surface, (text_x, y_pos))
    
    # Draw scrollbar
    if 15 > max_visible_bottles:
        bottle_config_scrollbar.draw(screen)
    
    # Instructions
    inst_text = font_small.render("Click on a bottle to customize it", True, GRAY)
    inst_rect = inst_text.get_rect(center=(SCREEN_WIDTH // 2, list_end_y + max(20, int(30 * scale_y))))
    screen.blit(inst_text, inst_rect)
    
    # Scroll instructions
    scroll_inst_text = font_small.render("Use arrow keys, mouse wheel, or drag scrollbar to navigate", True, GRAY)
    scroll_inst_rect = scroll_inst_text.get_rect(center=(SCREEN_WIDTH // 2, list_end_y + max(40, int(50 * scale_y))))
    screen.blit(scroll_inst_text, scroll_inst_rect)
    
    # Back button
    button_width = max(80, int(120 * scale_x))
    button_height = max(30, int(40 * scale_y))
    back_button = Button(
        SCREEN_WIDTH // 2 - button_width // 2,
        SCREEN_HEIGHT - max(60, int(80 * scale_y)),
        button_width,
        button_height,
        "BACK",
        font_medium,
        hover_color=ORANGE,
        text_key='text_back'
    )
    
    # Set image manager for button
    back_button.image_manager = image_manager
    
    # Update hover state
    mouse_pos = pg.mouse.get_pos()
    back_button.update_hover(mouse_pos)
    back_button.draw(screen)
    
    return back_button, bottle_config_scrollbar, visible_bottles, list_start_y, line_spacing

def recalculate_scrollbar():
    global scrollbar
    if 'leaderboard' not in globals() or leaderboard is None:
        return  # Can't build scrollbar yet
    
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
    """Display the leaderboard with visual scrollbar and enhanced visuals"""
    global leaderboard_scroll, scrollbar
    
    draw_background(screen, 'leaderboard')
    
    # Title with image support
    draw_text_or_image(screen, 'text_leaderboard', "LEADERBOARD", font_large, WHITE,
                      (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 6))
    
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
    pg.draw.rect(screen, WHITE, outline_rect, max(2, int(3 * min(scale_x, scale_y))))
    pg.draw.rect(screen, BLACK, outline_rect, 0)
    
    # Calculate how many scores can fit in the grey box
    available_height = box_height - 2 * box_margin
    max_visible_scores = max(1, int(available_height // line_spacing))
    
    # Ensure leaderboard_scroll is initialized
    if leaderboard_scroll is None:
        leaderboard_scroll = 0
    
    # Create scrollbar
    scrollbar_width = max(15, int(20 * scale_x))
    scrollbar_x = box_x + box_width + max(5, int(8 * scale_x))
    scrollbar_y = box_y
    scrollbar_height = box_height
    
    # Always create a new scrollbar to avoid crashes
    scrollbar = ScrollBar(
        scrollbar_x,
        scrollbar_y,
        scrollbar_width,
        scrollbar_height,
        len(all_scores),
        max_visible_scores
    )
    
    # Set scroll position
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
    else:
        # Scroll instructions for leaderboard
        scroll_inst_text = font_small.render("Use arrow keys, mouse wheel, or drag scrollbar to navigate", True, GRAY)
        scroll_inst_rect = scroll_inst_text.get_rect(center=(SCREEN_WIDTH // 2, box_y + box_height + max(20, int(30 * scale_y))))
        screen.blit(scroll_inst_text, scroll_inst_rect)
    
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
        font_medium,
        hover_color=ORANGE,
        text_key='text_back'
    )
    
    # Set image manager for buttons
    clear_button.image_manager = image_manager
    back_button.image_manager = image_manager
    
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
    draw_background(screen, 'menu')

    # Title with image support
    draw_text_or_image(screen, None, "ENTER USERNAME", font_large, WHITE,
                      (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 3))

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
    if current_username.strip():
        inst_text = font_small.render("Press ENTER to continue", True, GREEN)
    else:
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
        font_small,
        hover_color=ORANGE,
        text_key='text_back'
    )
    
    # Set image manager for button
    back_button.image_manager = image_manager
    
    # Update hover state
    mouse_pos = pg.mouse.get_pos()
    back_button.update_hover(mouse_pos)
    
    back_button.draw(screen)
    return input_box, back_button

def show_game_over_screen():
    """Display game over screen with enhanced visuals and multiple options"""
    global start_time
    draw_background(screen, 'menu')
    
    # Game Over text with image support
    draw_text_or_image(screen, 'text_game_over', "GAME OVER", font_large, RED,
                      (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 5))
    
    # Final score (no breakdown needed since no time bonus)
    scale_y = SCREEN_HEIGHT / BASE_HEIGHT
    line_height = max(25, int(35 * scale_y))
    start_y = SCREEN_HEIGHT // 3
    
    # Final score
    final_text = font_large.render(f"FINAL SCORE: {final_score:,}", True, YELLOW)
    final_rect = final_text.get_rect(center=(SCREEN_WIDTH // 2, start_y))
    screen.blit(final_text, final_rect)
    
    # Time survived
    minutes = survival_time_seconds_final // 60
    seconds = survival_time_seconds_final % 60
    time_text = font_medium.render(f"Time Survived: {minutes:02d}:{seconds:02d}", True, GREEN)
    time_rect = time_text.get_rect(center=(SCREEN_WIDTH // 2, start_y + line_height))
    screen.blit(time_text, time_rect)
    
    # Buttons - stacked vertically in the center
    scale_x = SCREEN_WIDTH / BASE_WIDTH
    scale_y = SCREEN_HEIGHT / BASE_HEIGHT
    button_width = max(80, int(200 * scale_x))
    button_height = max(30, int(50 * scale_y))
    button_spacing_y = max(15, int(20 * scale_y))

    # Starting Y so the stack is centered vertically under the text
    total_height = button_height * 4 + button_spacing_y * 3
    start_x = (SCREEN_WIDTH - button_width) // 2
    buttons_start_y = start_y + line_height * 2  # put it under the score/time text

    # Create buttons stacked vertically
    play_again_button = Button(
        start_x,
        buttons_start_y,
        button_width,
        button_height,
        "PLAY AGAIN",
        font_small,
        hover_color=GREEN,
        text_key='text_play'
    )

    leaderboard_button = Button(
        start_x,
        buttons_start_y + (button_height + button_spacing_y) * 1,
        button_width,
        button_height,
        "LEADERBOARD",
        font_small,
        hover_color=YELLOW,
        text_key='text_leaderboard'
    )

    menu_button = Button(
        start_x,
        buttons_start_y + (button_height + button_spacing_y) * 2,
        button_width,
        button_height,
        "MAIN MENU",
        font_small
    )

    quit_button = Button(
        start_x,
        buttons_start_y + (button_height + button_spacing_y) * 3,
        button_width,
        button_height,
        "QUIT",
        font_small,
        hover_color=RED,
        text_key='text_quit'
    )

    
    # Set image manager for all buttons
    for button in [play_again_button, leaderboard_button, menu_button, quit_button]:
        button.image_manager = image_manager
    
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

# BOTTLE EDITING FUNCTIONS

# Bottle editing variables and functions
selected_bottle_id = 1
edit_field = 0  # 0=color_r, 1=color_g, 2=color_b, 3=width, 4=height, 5=min_curve, 6=max_curve, 7=score_gain
edit_fields = ['color_r', 'color_g', 'color_b', 'width', 'height', 'min_curve', 'max_curve', 'score_gain']
temp_bottle_config = {}

def show_bottle_edit():
    """Display bottle editing interface with enhanced visuals"""
    global temp_bottle_config, edit_field
    
    draw_background(screen, 'settings')
    
    # Get current bottle config
    config = bottle_config.get_bottle_config(selected_bottle_id)
    
    # Initialize temp config if not exists
    if not temp_bottle_config or temp_bottle_config.get('id') != selected_bottle_id:
        temp_bottle_config = {
            'id': selected_bottle_id,
            'color_r': config['color'][0],
            'color_g': config['color'][1],
            'color_b': config['color'][2],
            'width': config['width'],
            'height': config['height'],
            'min_curve': config['min_curve'],
            'max_curve': config['max_curve'],
            'score_gain': config['score_gain']
        }
    
    # Title
    title_text = font_medium.render(f"Editing: {config['name']}", True, WHITE)
    title_rect = title_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 8))
    screen.blit(title_text, title_rect)
    
    # Dynamic scaling
    scale_x = SCREEN_WIDTH / BASE_WIDTH
    scale_y = SCREEN_HEIGHT / BASE_HEIGHT
    
    # Preview bottle
    preview_size = max(20, int(40 * min(scale_x, scale_y)))
    preview_x = SCREEN_WIDTH // 4
    preview_y = SCREEN_HEIGHT // 4
    preview_color = (temp_bottle_config['color_r'], temp_bottle_config['color_g'], temp_bottle_config['color_b'])
    preview_rect = pg.Rect(preview_x, preview_y, preview_size, preview_size)
    
    # Try to use bottle image if available
    if (image_manager and 
        not image_manager.use_fallbacks()):
        
        bottle_img = image_manager.get_image(f'bottle_{selected_bottle_id}')
        if bottle_img:
            # Scale image to preview size
            scaled_img = pg.transform.scale(bottle_img, (preview_size, preview_size))
            screen.blit(scaled_img, preview_rect.topleft)
        else:
            # Fallback to colored rectangle
            pg.draw.rect(screen, preview_color, preview_rect)
    else:
        # Use fallback colored rectangle
        pg.draw.rect(screen, preview_color, preview_rect)
    
    # Edit fields
    field_start_y = SCREEN_HEIGHT // 3
    field_spacing = max(25, int(35 * scale_y))
    field_x = SCREEN_WIDTH // 2
    
    for i, field_name in enumerate(edit_fields):
        y_pos = field_start_y + i * field_spacing
        
        # Highlight current field
        color = BLUE if i == edit_field else WHITE
        
        # Get current value
        current_value = temp_bottle_config[field_name]
        if field_name.startswith('color_'):
            display_text = f"{field_name.upper()}: {current_value} (0-255)"
        elif field_name in ['min_curve', 'max_curve']:
            display_text = f"{field_name.upper()}: {current_value:.2f}"
        else:
            display_text = f"{field_name.upper()}: {current_value}"
        
        field_surface = font_small.render(display_text, True, color)
        field_rect = field_surface.get_rect(center=(field_x, y_pos))
        screen.blit(field_surface, field_rect)
    
    # Instructions
    inst_text = font_small.render("Use UP/DOWN to select field, LEFT/RIGHT to adjust value", True, GRAY)
    inst_rect = inst_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT - max(80, int(100 * scale_y))))
    screen.blit(inst_text, inst_rect)
    
    # Save and Back buttons
    button_width = max(80, int(100 * scale_x))
    button_height = max(30, int(40 * scale_y))
    button_spacing = max(20, int(30 * scale_x))
    
    save_button = Button(
        SCREEN_WIDTH // 2 - button_width - button_spacing // 2,
        SCREEN_HEIGHT - max(45, int(60 * scale_y)),
        button_width,
        button_height,
        "SAVE",
        font_small,
        hover_color=GREEN
    )
    
    back_button = Button(
        SCREEN_WIDTH // 2 + button_spacing // 2,
        SCREEN_HEIGHT - max(45, int(60 * scale_y)),
        button_width,
        button_height,
        "BACK",
        font_small,
        hover_color=ORANGE,
        text_key='text_back'
    )
    
    # Set image manager for buttons
    save_button.image_manager = image_manager
    back_button.image_manager = image_manager
    
    # Update hover states
    mouse_pos = pg.mouse.get_pos()
    save_button.update_hover(mouse_pos)
    back_button.update_hover(mouse_pos)
    
    save_button.draw(screen)
    back_button.draw(screen)
    
    return save_button, back_button

def handle_bottle_edit_events(event):
    """Handle events for bottle editing"""
    global edit_field, temp_bottle_config
    
    if event.type == pg.KEYDOWN:
        # Navigate fields
        if event.key == pg.K_UP:
            edit_field = (edit_field - 1) % len(edit_fields)
        elif event.key == pg.K_DOWN:
            edit_field = (edit_field + 1) % len(edit_fields)
        
        # Adjust values
        elif event.key == pg.K_LEFT:
            adjust_bottle_value(-1)
        elif event.key == pg.K_RIGHT:
            adjust_bottle_value(1)

def adjust_bottle_value(direction):
    """Adjust the current bottle field value"""
    global temp_bottle_config
    
    field_name = edit_fields[edit_field]
    current_value = temp_bottle_config[field_name]
    
    if field_name.startswith('color_'):
        # Color values: 0-255
        new_value = max(0, min(255, current_value + direction * 5))
    elif field_name in ['width', 'height']:
        # Size values: 1-20
        new_value = max(1, min(20, current_value + direction))
    elif field_name in ['min_curve', 'max_curve']:
        # Curve values: 0.0-2.0
        new_value = max(0.0, min(2.0, current_value + direction * 0.1))
        new_value = round(new_value, 2)
    elif field_name == 'score_gain':
        # Score values: 1-100
        new_value = max(1, min(100, current_value + direction * 5))
    else:
        return
    
    temp_bottle_config[field_name] = new_value
    
    # Ensure min_curve <= max_curve
    if field_name == 'min_curve' and temp_bottle_config['min_curve'] > temp_bottle_config['max_curve']:
        temp_bottle_config['max_curve'] = temp_bottle_config['min_curve']
    elif field_name == 'max_curve' and temp_bottle_config['max_curve'] < temp_bottle_config['min_curve']:
        temp_bottle_config['min_curve'] = temp_bottle_config['max_curve']

def save_bottle_config():
    """Save the temporary bottle configuration"""
    global temp_bottle_config
    
    # Update the bottle config
    config = bottle_config.bottle_types[selected_bottle_id]
    config['color'] = (temp_bottle_config['color_r'], temp_bottle_config['color_g'], temp_bottle_config['color_b'])
    config['width'] = temp_bottle_config['width']
    config['height'] = temp_bottle_config['height']
    config['min_curve'] = temp_bottle_config['min_curve']
    config['max_curve'] = temp_bottle_config['max_curve']
    config['score_gain'] = temp_bottle_config['score_gain']
    
    # Save to file
    bottle_config.save_config()
    logging.info(f"Saved configuration for {config['name']}")

# FADE TRANSITION FUNCTIONS

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

# GAME LOOP FUNCTION

def safe_game_loop():
    """Enhanced main game loop with animations and visual effects"""
    global player_x, player_y, vel_y, is_on_ground, drunk_x, lives, last_bottle_time, bottles, start_time, screen
    global score, bottles_dodged, close_calls, combo_multiplier
    global bottle_spawn_time, left_hand_spawn_time, last_left_bottle_time
    global image_manager, visual_effects
    global left_hand_preview, right_hand_preview, left_hand_preview_time, right_hand_preview_time
    
    running = True
    frame_count = 0
    
    while running:
        frame_count += 1
        current_time = pg.time.get_ticks()
        
        # Update all animations
        image_manager.update_animations()
        
        # Update difficulty based on score
        bottle_spawn_time, left_hand_spawn_time = get_current_difficulty()
        
        # Draw background
        draw_background(screen, 'game')
        
        keys = pg.key.get_pressed()
        
        # Update player animation state
        update_player_animation_state()
        
        # Update drunk animation state
        update_drunk_animation()
        
        # Player movement
        if keys[pg.K_LEFT] or keys[pg.K_a]:
            player_x = max(0, player_x - player_speed)
            player_facing_right = False
            player_last_direction = "left"
        if keys[pg.K_RIGHT] or keys[pg.K_d]:
            player_x = min(SCREEN_WIDTH - player_width, player_x + player_speed)
            player_facing_right = True
            player_last_direction = "right"
        
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
        
        # Draw animated drunk guy
        draw_animated_drunk(screen, drunk_x, drunk_y, drunk_width, drunk_height)
        
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
        if right_hand_preview is None:
            # Time to show a new preview bottle from right hand
            if current_time - last_bottle_time > bottle_spawn_time:
                # Get random bottle type based on spawn weights
                bottle_type_id = bottle_config.get_random_bottle_type()
                bottle_config_data = bottle_config.get_bottle_config(bottle_type_id)
                
                # Create preview bottle (not thrown yet)
                right_hand_preview = {
                    'type_id': bottle_type_id,
                    'config': bottle_config_data,
                    'color': bottle_config_data['color']
                }
                right_hand_preview_time = current_time
        
        # LEFT HAND: Bottle preview and spawning system
        if left_hand_preview is None:
            # Time to show a new preview bottle from left hand
            if current_time - last_left_bottle_time > left_hand_spawn_time:
                # Get random bottle type based on spawn weights
                bottle_type_id = bottle_config.get_random_bottle_type()
                bottle_config_data = bottle_config.get_bottle_config(bottle_type_id)
                
                # Create preview bottle (not thrown yet)
                left_hand_preview = {
                    'type_id': bottle_type_id,
                    'config': bottle_config_data,
                    'color': bottle_config_data['color']
                }
                left_hand_preview_time = current_time
        
        # Check if it's time to throw bottles from hands
        # RIGHT HAND throwing
        if right_hand_preview is not None and current_time - right_hand_preview_time >= next_bottle_throw_delay:
            # Trigger right hand throwing animation
            trigger_drunk_throw("right")
            
            # Create bottle from right hand
            scale_x = SCREEN_WIDTH / BASE_WIDTH
            scale_y = SCREEN_HEIGHT / BASE_HEIGHT
            right_hand_x = drunk_x + drunk_width + max(10, int(15 * scale_x))
            right_hand_y = drunk_y + drunk_height // 3
            preview_size = max(8, int(12 * min(scale_x, scale_y)))
            
            new_bottle = Bottle(
                right_hand_x + preview_size // 2,
                right_hand_y + preview_size // 2,
                player_x + player_width // 2,
                player_base_y + player_height + 30,  # Target below the player
                right_hand_preview['type_id'],
                "right",
                is_preview_transition=True
            )
            new_bottle.image_manager = image_manager
            bottles.append(new_bottle)
            
            # Reset for next bottle
            right_hand_preview = None
            last_bottle_time = current_time
        
        # LEFT HAND throwing
        if left_hand_preview is not None and current_time - left_hand_preview_time >= next_left_bottle_throw_delay:
            # Trigger left hand throwing animation
            trigger_drunk_throw("left")
            
            # Create bottle from left hand
            scale_x = SCREEN_WIDTH / BASE_WIDTH
            scale_y = SCREEN_HEIGHT / BASE_HEIGHT
            left_hand_x = drunk_x - max(15, int(20 * scale_x))
            left_hand_y = drunk_y + drunk_height // 3
            preview_size = max(8, int(12 * min(scale_x, scale_y)))
            
            new_bottle = Bottle(
                left_hand_x + preview_size // 2,
                left_hand_y + preview_size // 2,
                player_x + player_width // 2,
                player_base_y + player_height + 30,  # Target below the player
                left_hand_preview['type_id'],
                "left",
                is_preview_transition=True
            )
            new_bottle.image_manager = image_manager
            bottles.append(new_bottle)
            
            # Reset for next bottle
            left_hand_preview = None
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
                    
                    # Calculate score using bottle-specific score gain
                    base_points = bottle.config['score_gain']
                    if is_close_call:
                        base_points = int(base_points * 2.5)  # Close calls get 2.5x multiplier
                    if bottle.bottle_type == "air":
                        base_points = int(base_points * 1.5)  # Air bottles get additional 1.5x multiplier
                    
                    points = int(base_points * combo_multiplier)
                    
                    # Add to score
                    score += points
                    bottles_dodged += 1
                    if is_close_call:
                        close_calls += 1
                    
                    # Update combo system (no timer limit)
                    combo_multiplier = min(MAX_COMBO, combo_multiplier + COMBO_INCREMENT)
                    
                    # Add visual feedback with bottle name
                    add_score_popup(
                        bottle.x, bottle.y - 30, 
                        points, is_close_call, combo_multiplier, bottle.name
                    )
                    
                    bottle.scored = True
                    logging.info(f"{bottle.name} dodged! Points: {points} (base: {base_points}, combo: x{combo_multiplier:.1f}) Close call: {is_close_call}")
                
                bottles_to_remove.append(i)
            elif bottle.hit_player:
                # Remove bottles that have hit the player
                bottles_to_remove.append(i)
            else:
                # Determine current player z-range based on jumping state
                if is_on_ground:
                    current_player_z_start = 0.2
                    current_player_z_end = 1.0
                else:
                    current_player_z_start = 0.2
                    current_player_z_end = 1.0
                
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
                        
                        # Create impact effect for special bottles
                        effect = bottle.create_impact_effect()
                        if effect:
                            visual_effects.append(effect)
                        
                        # Reset combo when hit
                        combo_multiplier = 1.0
                        
                        # Enhanced logging with bottle type and hand
                        jump_status = "jumping" if not is_on_ground else "on ground"
                        player_z = f"{current_player_z_start:.1f}-{current_player_z_end:.1f}"
                        logging.info(f"Player hit while {jump_status} by {bottle.hand} hand {bottle.name} (z={bottle.z:.3f}, player_z={player_z})! Lives remaining: {lives}")
                        
                        if lives <= 0:
                            logging.info("Game over - no lives remaining")
                            calculate_final_score()
                            global survival_time_seconds_final
                            survival_time_seconds_final = (current_time - start_time) // 1000
                            return survival_time_seconds_final  # Return frozen survival time

        # Remove bottles safely (reverse order to maintain indices)
        for i in reversed(sorted(set(bottles_to_remove))):
            if 0 <= i < len(bottles):
                bottles.pop(i)
        
        # Update visual effects
        effects_to_remove = []
        for i, effect in enumerate(visual_effects):
            if effect.update():
                effects_to_remove.append(i)
        
        # Remove finished effects
        for i in reversed(effects_to_remove):
            visual_effects.pop(i)
        
        # Update score popups
        update_score_popups()
        
        # Draw bottles behind player
        for bottle in bottles_behind:
            bottle.draw(screen)
        
        # Draw animated player
        draw_animated_player(screen, player_x, player_y, player_width, player_height)
        
        # Draw bottles in front of player
        for bottle in bottles_in_front:
            bottle.draw(screen)
        
        # Draw visual effects on top
        for effect in visual_effects:
            effect.draw(screen)
        
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
            combo_text = font_small.render(f"COMBO x{combo_multiplier:.1f}", True, BLUE)
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
            font_small,
            hover_color=ORANGE,
            text_key='text_back'
        )
        
        # Set image manager for button
        back_button.image_manager = image_manager
        
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

# MAIN FUNCTION AND GAME LOOP

def main():
    """Enhanced main game function with animations and visual effects"""
    global current_state, current_username, input_active, final_score, is_fullscreen, screen, leaderboard, leaderboard_scroll
    global SCREEN_WIDTH, SCREEN_HEIGHT, font_large, font_medium, font_small, fade_direction, next_state
    global bottle_config_scroll, image_manager, bottle_config_scrollbar, scrollbar

    leaderboard = LeaderboardManager()
    
    # Add default scores for testing
    leaderboard.add_default_scores()
    
    # Initialize scroll positions
    bottle_config_scroll = 0
    leaderboard_scroll = 0
    
    # Initialize scrollbars
    bottle_config_scrollbar = None
    scrollbar = None
    
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
                    SCREEN_WIDTH = new_width
                    SCREEN_HEIGHT = new_height
                    update_screen_dimensions(new_width, new_height)
                    
                    # Recreate fade surface with new dimensions
                    global fade_surface
                    fade_surface = pg.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
                    fade_surface.fill((0, 0, 0))
                    
                # Re-queue the event for state-specific handling
                pg.event.post(event)
            
            # Only process input if not in the middle of a fade transition
            if fade_direction == 0:
                if current_state == LOADING:
                    show_loading_screen()
                    
                    for event in pg.event.get():
                        if event.type == pg.QUIT:
                            return
                        elif event.type == pg.KEYDOWN:
                            if event.key == pg.K_SPACE:
                                # Skip loading screen with spacebar (optional)
                                start_fade_transition(MENU)
                            elif not image_manager.is_loading():
                                # Any other key or mouse click only works when loading is complete
                                start_fade_transition(MENU)
                        elif event.type == pg.MOUSEBUTTONDOWN:
                            if not image_manager.is_loading():
                                start_fade_transition(MENU)
                
                elif current_state == MENU:
                    play_btn, settings_btn, bottle_config_btn, leaderboard_btn, exit_btn = show_menu()
                    
                    for event in pg.event.get():
                        if event.type == pg.QUIT:
                            return
                        elif event.type == pg.KEYDOWN:
                            if event.key == pg.K_ESCAPE:
                                start_fade_transition(MENU)
                                return
                        
                        # Handle button clicks with fade transitions
                        if play_btn.handle_event(event):
                            start_fade_transition(USERNAME_INPUT)
                            input_active = True
                        elif settings_btn.handle_event(event):
                            start_fade_transition(SETTINGS)
                        elif bottle_config_btn.handle_event(event):
                            start_fade_transition(BOTTLE_CONFIG)
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
                    global start_time
                    start_time = pg.time.get_ticks()
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
                
                elif current_state == BOTTLE_CONFIG:
                    back_btn, config_scrollbar, visible_bottles, list_start_y, line_spacing = show_bottle_config()
                    
                    for event in pg.event.get():
                        if event.type == pg.QUIT:
                            return
                        elif event.type == pg.KEYDOWN:
                            if event.key == pg.K_ESCAPE:
                                start_fade_transition(MENU)
                            elif event.key == pg.K_UP:
                                bottle_config_scroll = max(0, bottle_config_scroll - 1)
                                if config_scrollbar:
                                    config_scrollbar.set_scroll_position(bottle_config_scroll)
                            elif event.key == pg.K_DOWN:
                                bottle_config_scroll = min(14, bottle_config_scroll + 1)
                                if config_scrollbar:
                                    config_scrollbar.set_scroll_position(bottle_config_scroll)
                            elif event.key == pg.K_PAGEUP:
                                # Page up - scroll by multiple items
                                bottle_config_scroll = max(0, bottle_config_scroll - 5)
                                if config_scrollbar:
                                    config_scrollbar.set_scroll_position(bottle_config_scroll)
                            elif event.key == pg.K_PAGEDOWN:
                                # Page down - scroll by multiple items
                                bottle_config_scroll = min(14, bottle_config_scroll + 5)
                                if config_scrollbar:
                                    config_scrollbar.set_scroll_position(bottle_config_scroll)
                            elif event.key == pg.K_HOME:
                                # Home - go to top
                                bottle_config_scroll = 0
                                if config_scrollbar:
                                    config_scrollbar.set_scroll_position(bottle_config_scroll)
                            elif event.key == pg.K_END:
                                # End - go to bottom
                                bottle_config_scroll = 14
                                if config_scrollbar:
                                    config_scrollbar.set_scroll_position(bottle_config_scroll)
                        elif event.type == pg.MOUSEBUTTONDOWN:
                            # Handle scrollbar first
                            if config_scrollbar and config_scrollbar.handle_event(event):
                                bottle_config_scroll = config_scrollbar.scroll_position
                            # Handle bottle selection clicks
                            elif event.button == 1:  # Left click
                                mouse_x, mouse_y = event.pos
                                # Check if click is on a bottle in the list
                                for i, bottle_id in enumerate(visible_bottles):
                                    y_pos = list_start_y + i * line_spacing
                                    click_area = pg.Rect(0, y_pos, SCREEN_WIDTH - max(60, int(80 * SCREEN_WIDTH / BASE_WIDTH)), line_spacing)
                                    if click_area.collidepoint(mouse_x, mouse_y):
                                        # Open bottle customization for this bottle
                                        global selected_bottle_id
                                        selected_bottle_id = bottle_id
                                        start_fade_transition(BOTTLE_EDIT)
                                        break
                            # Handle back button
                            if back_btn.handle_event(event):
                                start_fade_transition(MENU)
                        elif event.type == pg.MOUSEMOTION:
                            if config_scrollbar and config_scrollbar.handle_event(event):
                                # Update the scroll position during dragging
                                bottle_config_scroll = config_scrollbar.scroll_position
                        elif event.type == pg.MOUSEBUTTONUP:
                            if config_scrollbar and config_scrollbar.handle_event(event):
                                # Update the scroll position when dragging ends
                                bottle_config_scroll = config_scrollbar.scroll_position
                        elif event.type == pg.MOUSEWHEEL:
                            # Handle mouse wheel scrolling
                            if event.y > 0:  # Scroll up
                                bottle_config_scroll = max(0, bottle_config_scroll - 1)
                                if config_scrollbar:
                                    config_scrollbar.set_scroll_position(bottle_config_scroll)
                            elif event.y < 0:  # Scroll down
                                bottle_config_scroll = min(14, bottle_config_scroll + 1)
                                if config_scrollbar:
                                    config_scrollbar.set_scroll_position(bottle_config_scroll)
                
                elif current_state == BOTTLE_EDIT:
                    save_btn, back_btn = show_bottle_edit()
                    
                    for event in pg.event.get():
                        if event.type == pg.QUIT:
                            return
                        elif event.type == pg.KEYDOWN:
                            if event.key == pg.K_ESCAPE:
                                start_fade_transition(BOTTLE_CONFIG)
                        elif event.type == pg.MOUSEBUTTONDOWN:
                            if save_btn.handle_event(event):
                                save_bottle_config()
                                start_fade_transition(BOTTLE_CONFIG)
                            elif back_btn.handle_event(event):
                                start_fade_transition(BOTTLE_CONFIG)
                        
                        # Handle bottle editing keyboard events
                        handle_bottle_edit_events(event)
                
                elif current_state == LEADERBOARD:
                    clear_btn, back_btn, scrollbar = show_leaderboard()
                    
                    for event in pg.event.get():
                        if event.type == pg.QUIT:
                            return
                        elif event.type == pg.KEYDOWN:
                            if event.key == pg.K_ESCAPE:
                                start_fade_transition(MENU)
                            elif event.key == pg.K_UP:
                                leaderboard_scroll = max(0, leaderboard_scroll - 1)
                                if scrollbar:
                                    scrollbar.set_scroll_position(leaderboard_scroll)
                            elif event.key == pg.K_DOWN:
                                all_scores = leaderboard.get_all_scores()
                                leaderboard_scroll = min(len(all_scores) - max_visible_scores, leaderboard_scroll + 1)
                                if scrollbar:
                                    scrollbar.set_scroll_position(leaderboard_scroll)
                            elif event.key == pg.K_PAGEUP:
                                # Page up - scroll by multiple items
                                leaderboard_scroll = max(0, leaderboard_scroll - 5)
                                if scrollbar:
                                    scrollbar.set_scroll_position(leaderboard_scroll)
                            elif event.key == pg.K_PAGEDOWN:
                                # Page down - scroll by multiple items
                                all_scores = leaderboard.get_all_scores()
                                leaderboard_scroll = min(len(all_scores) - max_visible_scores, leaderboard_scroll + 5)
                                if scrollbar:
                                    scrollbar.set_scroll_position(leaderboard_scroll)
                            elif event.key == pg.K_HOME:
                                # Home - go to top
                                leaderboard_scroll = 0
                                if scrollbar:
                                    scrollbar.set_scroll_position(leaderboard_scroll)
                            elif event.key == pg.K_END:
                                # End - go to bottom
                                all_scores = leaderboard.get_all_scores()
                                leaderboard_scroll = max(0, len(all_scores) - max_visible_scores)
                                if scrollbar:
                                    scrollbar.set_scroll_position(leaderboard_scroll)

                        # Handle scrollbar events first (all event types)
                        if scrollbar and scrollbar.handle_event(event):
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
                        elif event.type == pg.MOUSEWHEEL:
                            # Handle mouse wheel scrolling
                            all_scores = leaderboard.get_all_scores()
                            if event.y > 0:  # Scroll up
                                leaderboard_scroll = max(0, leaderboard_scroll - 1)
                                if scrollbar:
                                    scrollbar.set_scroll_position(leaderboard_scroll)
                            elif event.y < 0:  # Scroll down
                                leaderboard_scroll = min(len(all_scores) - max_visible_scores, leaderboard_scroll + 1)
                                if scrollbar:
                                    scrollbar.set_scroll_position(leaderboard_scroll)
        
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
                if current_state == LOADING:
                    show_loading_screen()
                elif current_state == MENU:
                    show_menu()
                elif current_state == USERNAME_INPUT:
                    show_username_input()
                elif current_state == SETTINGS:
                    show_settings()
                elif current_state == BOTTLE_CONFIG:
                    show_bottle_config()
                elif current_state == BOTTLE_EDIT:
                    show_bottle_edit()
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
        exit(0)

# CONSTANTS AND GLOBAL VARIABLES

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
ORANGE = (255, 165, 0)
PURPLE = (128, 0, 128)
GRAY = (128, 128, 128)
DARK_GRAY = (64, 64, 64)
LIGHT_GRAY = (192, 192, 192)

# Game states
LOADING = 0
MENU = 1
USERNAME_INPUT = 2
PLAYING = 3
SETTINGS = 4
BOTTLE_CONFIG = 5
LEADERBOARD = 6
GAME_OVER = 7
BOTTLE_EDIT = 8

# Initialize pygame and check for errors
if not safe_init():
    exit(1)

# Screen settings
BASE_WIDTH = 800
BASE_HEIGHT = 600
is_fullscreen = False

# Try to create display
try:
    screen = create_display(BASE_WIDTH, BASE_HEIGHT, "Bottle Ops - Enhanced Edition")
    SCREEN_WIDTH = screen.get_width()
    SCREEN_HEIGHT = screen.get_height()
except Exception as e:
    logging.error(f"Failed to create display: {e}")
    exit(1)

# Initialize clock
clock = pg.time.Clock()

# Load fonts safely
try:
    font_large = load_font('Arial', max(24, int(36 * min(SCREEN_WIDTH/BASE_WIDTH, SCREEN_HEIGHT/BASE_HEIGHT))))
    font_medium = load_font('Arial', max(16, int(24 * min(SCREEN_WIDTH/BASE_WIDTH, SCREEN_HEIGHT/BASE_HEIGHT))))
    font_small = load_font('Arial', max(12, int(18 * min(SCREEN_WIDTH/BASE_WIDTH, SCREEN_HEIGHT/BASE_HEIGHT))))
except Exception as e:
    logging.error(f"Failed to load fonts: {e}")
    exit(1)

# Initialize image manager
image_manager = ImageManager()

# Initialize bottle configuration
bottle_config = BottleTypeConfig()

# Game state
current_state = LOADING
current_username = "NEW USER"
input_active = True

# Player direction tracking
player_facing_right = True
player_last_direction = "right"

# Loading screen variables
loading_progress = 0
loading_animation_timer = 0
loading_animation_speed = 2

# Fade transition variables
fade_alpha = 0
fade_direction = 0  # 0=no fade, 1=fade out, -1=fade in
next_state = None
fade_speed = 10
fade_surface = pg.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
fade_surface.fill((0, 0, 0))

# Game variables (will be calculated dynamically)
player_width = 90
player_height = 90
player_base_y = SCREEN_HEIGHT - 75
player_x = SCREEN_WIDTH // 2 - player_width // 2
player_y = player_base_y
vel_y = 0
is_on_ground = True
player_speed = 5
jump_power = -24000000
gravity = 0.1

# Drunk guy variables
drunk_width = 40
drunk_height = 60
drunk_x = SCREEN_WIDTH // 2 - drunk_width // 2
drunk_y = 50

# Animation state variables
player_moving = False
player_jumping = False
player_on_ground_last_frame = True
drunk_current_animation = 'drunk_idle'
drunk_throwing_timer = 0
drunk_throw_duration = 30  # frames

# 3D depth zones for collision detection
player_z_ground_start = -100.0
player_z_ground_end = 100.0
player_z_air_start = -100.0
player_z_air_end = 100.0

# Game state variables
lives = 9
score = 0
bottles_dodged = 0
close_calls = 0
final_score = 0
survival_time_seconds_final = 0
start_time = pg.time.get_ticks()
bottles = []
visual_effects = []
score_popups = []

# Bottle spawning variables
last_bottle_time = pg.time.get_ticks()
last_left_bottle_time = pg.time.get_ticks()
bottle_spawn_time = 1000  # milliseconds
left_hand_spawn_time = 1500  # milliseconds
next_bottle_preview = None
next_bottle_show_time = 0
next_left_bottle_preview = None
next_left_bottle_show_time = 0
next_bottle_throw_delay = 500  # milliseconds between preview and throw
next_left_bottle_throw_delay = 500
current_throwing_hand = "right"

# Difficulty system
DIFFICULTY_INCREASE_INTERVAL = 500  # Points needed to increase difficulty
MIN_SPAWN_TIME = 200  # Minimum spawn time in milliseconds
MIN_LEFT_SPAWN_TIME = 300  # Minimum left hand spawn time

# Scoring system
CLOSE_CALL_DISTANCE = 80  # pixels
combo_multiplier = 1.0
COMBO_INCREMENT = 0.1
MAX_COMBO = 10.0

# Leaderboard
leaderboard = None
leaderboard_scroll = 0
max_visible_scores = 10

# Scrollbars
scrollbar = None
bottle_config_scroll = 0
bottle_config_scrollbar = None

# Hand preview system
left_hand_preview = None
right_hand_preview = None
left_hand_preview_time = 0
right_hand_preview_time = 0

# Bottle spawning variables (legacy - kept for compatibility)
next_bottle_preview = None
next_bottle_show_time = 0
next_left_bottle_preview = None
next_left_bottle_show_time = 0
current_throwing_hand = "right"

# Calculate initial scaled values
get_scaled_values()

# Main execution
if __name__ == "__main__":
    try:
        logging.info("Starting Enhanced Bottle Ops game with animations")
        main() 
    except Exception as e:
        logging.error(f"Fatal error: {e}")
        
    finally:
        try:
            pg.quit()
        except:
            pass
        exit(0)
