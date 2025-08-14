# Bottle Ops Game

A fun bottle-dodging game built with Pygame featuring dynamic image loading and fallback graphics.

## Features

- **Dynamic Image Loading**: Automatically loads images from GitHub repositories
- **Fallback Graphics**: Gracefully falls back to drawn shapes if images fail to load
- **Click and Drag Scrollbars**: Enhanced scrollbar functionality for bottle configuration
- **Progressive Difficulty**: Game gets harder as you score more points
- **Dual Hand Throwing**: Bottles are thrown from both hands with different timing
- **Multiple Bottle Types**: 15 different bottle types with unique behaviors and scoring

## Image System Setup

The game automatically attempts to load images from a GitHub repository. To use your own images:

1. **Create a GitHub Repository**: Set up a private repository for your game assets
2. **Upload Images**: Add the following images to your repository:
   - `player.png` - Player character
   - `drunk.png` - Drunk person throwing bottles
   - `background.png` - Game background
   - `button_normal.png` - Normal button state
   - `button_hover.png` - Button hover state
   - `bottle_1.png` through `bottle_15.png` - Bottle type images

3. **Update URLs**: Modify the `IMAGE_URLS` dictionary in `main.py` to point to your repository:
   ```python
   IMAGE_URLS = {
       'player': 'https://raw.githubusercontent.com/YOUR_USERNAME/YOUR_REPO/main/player.png',
       # ... update all other URLs
   }
   ```

4. **Make Repository Public**: Ensure the repository is public or use GitHub tokens for private access

## Fallback System

If images fail to load, the game automatically uses drawn shapes:
- Colored rectangles for bottles
- Simple geometric shapes for buttons
- Basic backgrounds

## Installation

1. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

2. Run the game:
   ```bash
   python main.py
   ```

## Controls

- **Arrow Keys/WASD**: Move player
- **Space/W/Up**: Jump
- **Escape**: Return to menu
- **Mouse**: Navigate menus and interact with scrollbars

## Game States

- **Loading**: Shows while assets are being loaded
- **Menu**: Main game menu
- **Playing**: Active gameplay
- **Settings**: Game configuration
- **Bottle Config**: Customize bottle types
- **Leaderboard**: View high scores
- **Username Input**: Enter player name
- **Game Over**: End game screen

## Bottle Types

The game features 15 different bottle types with unique properties:
- **Ground Bottles**: Target players on the ground
- **Air Bottles**: Target jumping players
- **Special Bottles**: Have curve trajectories and unique behaviors

Each bottle type can be customized with:
- Colors (RGB values)
- Dimensions (width/height)
- Curve properties (min/max curve)
- Score values

## Technical Details

- **Image Loading**: Asynchronous loading with threading
- **Fallback System**: Automatic fallback to drawn graphics
- **Responsive Design**: Scales to different screen resolutions
- **Performance**: Optimized rendering with perspective scaling
- **Error Handling**: Comprehensive logging and error recovery

## Troubleshooting

- **Images Not Loading**: Check your GitHub URLs and repository settings
- **Performance Issues**: The game will automatically use fallback graphics
- **Scrollbar Issues**: Ensure you're using the latest version with enhanced scrollbar support

## Contributing

Feel free to contribute improvements, bug fixes, or new features to the game!
