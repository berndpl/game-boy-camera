"""
Game Boy Camera Color Palettes
Shared palette definitions for all Game Boy Camera processing scripts
"""

# Game Boy color palettes (4 colors each)
# Each palette maps grayscale levels 0-3 to RGB colors
PALETTES = {
    "DMG_Grayscale": [(15, 15, 15), (85, 85, 85), (170, 170, 170), (255, 255, 255)],
    "DMG_Green": [(8, 24, 32), (52, 104, 86), (136, 192, 112), (224, 248, 208)],
    "Pocket_GrayWarm": [(30, 30, 30), (90, 80, 70), (170, 150, 120), (250, 240, 220)],
    "GameBoyColor_Red": [(64, 0, 0), (128, 32, 32), (192, 96, 96), (255, 224, 224)],
    "Peanut_GB": [(26, 28, 32), (84, 94, 74), (166, 172, 134), (246, 255, 210)],
    "BW_Classic": [(8, 24, 32), (64, 64, 64), (144, 144, 144), (224, 248, 208)],
    "Lollipop": [(92, 28, 128), (132, 52, 168), (172, 124, 44), (212, 176, 140)]
}