# Image Configuration for Bottle Ops Game
# Update these URLs to point to your own image repository

# Base URL for your GitHub repository
# Replace 'yourusername' and 'your-repo' with your actual GitHub username and repository name
GITHUB_BASE = "https://raw.githubusercontent.com/yourusername/your-repo/main"

# Image URLs for game assets
IMAGE_URLS = {
    'player': f'{GITHUB_BASE}/player.png',
    'drunk': f'{GITHUB_BASE}/drunk.png',
    'background': f'{GITHUB_BASE}/background.png',
    'button_normal': f'{GITHUB_BASE}/button_normal.png',
    'button_hover': f'{GITHUB_BASE}/button_hover.png',
    'bottles': {
        1: f'{GITHUB_BASE}/bottle_ground.png',
        2: f'{GITHUB_BASE}/bottle_air.png',
        3: f'{GITHUB_BASE}/bottle_boomerang.png',
        4: f'{GITHUB_BASE}/bottle_shatter.png',
        5: f'{GITHUB_BASE}/bottle_molotov.png',
        6: f'{GITHUB_BASE}/bottle_sticky.png',
        7: f'{GITHUB_BASE}/bottle_leaky.png',
        8: f'{GITHUB_BASE}/bottle_pill.png',
        9: f'{GITHUB_BASE}/bottle_ink.png',
        10: f'{GITHUB_BASE}/bottle_hourglass.png',
        11: f'{GITHUB_BASE}/bottle_caffeine.png',
        12: f'{GITHUB_BASE}/bottle_golden.png',
        13: f'{GITHUB_BASE}/bottle_star.png',
        14: f'{GITHUB_BASE}/bottle_ghost.png',
        15: f'{GITHUB_BASE}/bottle_prankster.png'
    }
}

# Alternative: Use local image files instead of URLs
# Set this to True to use local images from an 'images' folder
USE_LOCAL_IMAGES = False

# Local image paths (when USE_LOCAL_IMAGES is True)
LOCAL_IMAGE_PATHS = {
    'player': 'images/player.png',
    'drunk': 'images/drunk.png',
    'background': 'images/background.png',
    'button_normal': 'images/button_normal.png',
    'button_hover': 'images/button_hover.png',
    'bottles': {
        1: 'images/bottle_ground.png',
        2: 'images/bottle_air.png',
        3: 'images/bottle_boomerang.png',
        4: 'images/bottle_shatter.png',
        5: 'images/bottle_molotov.png',
        6: 'images/bottle_sticky.png',
        7: 'images/bottle_leaky.png',
        8: 'images/bottle_pill.png',
        9: 'images/bottle_ink.png',
        10: 'images/bottle_hourglass.png',
        11: 'images/bottle_caffeine.png',
        12: 'images/bottle_golden.png',
        13: 'images/bottle_star.png',
        14: 'images/bottle_ghost.png',
        15: 'images/bottle_prankster.png'
    }
}
