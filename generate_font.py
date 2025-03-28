#!/usr/bin/env python3

import argparse
import os
import subprocess
from typing import Dict, List, Set, Tuple

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
UNIFONT_PATH = os.path.join(SCRIPT_DIR, "fonts/unifont-16.0.02.otf")
UNIFONT_UPPER_PATH = os.path.join(SCRIPT_DIR, "fonts/unifont_upper-16.0.02.otf")
UNIFONT_JP_PATH = os.path.join(SCRIPT_DIR, "fonts/unifont_jp-16.0.02.otf")
NERD_FONT_PATH = os.path.join(SCRIPT_DIR, "fonts/SymbolsNerdFontMono-Regular.ttf")

# Private Use Area for Nerd Fonts
NERD_FONT_RANGE = "0xE000-0xF8FF"

def split_range(range_str: str) -> Tuple[int, int]:
    start, end = range_str.split("-")
    return (int(start, 16), int(end, 16))

# Unicode ranges for different scripts
UNICODE_RANGES = {
    "latin": "0x20-0x7E",  # Basic Latin
    "latin_extended": "0xA0-0xFF",  # Latin-1 Supplement
    "cyrillic": "0x0400-0x04FF",  # Cyrillic
    "greek": "0x0370-0x03FF",  # Greek
    "japanese": "0x3040-0x309F,0x30A0-0x30FF,0x4E00-0x9FFF",  # Hiragana, Katakana, and common Kanji
    "korean": "0xAC00-0xD7AF",  # Hangul Syllables
    "chinese": "0x4E00-0x9FFF",  # Common Chinese characters
    "devanagari": "0x0900-0x097F",  # Devanagari (Hindi)
    "emoji": (
        "0x2190-0x21FF,"  # Arrows
        "0x2300-0x23FF,"  # Miscellaneous Technical
        "0x2500-0x257F,"  # Box Drawing
        "0x2600-0x26FF,"  # Miscellaneous Symbols
        "0x1F000-0x1F02F,"  # Mahjong Tiles
        "0x1F0A0-0x1F0FF,"  # Playing Cards
        "0x1F100-0x1F1FF,"  # Enclosed Alphanumeric Supplement
        "0x1F200-0x1F2FF,"  # Enclosed Ideographic Supplement
        "0x1F300-0x1F9FF,"  # Miscellaneous Symbols and Pictographs
        "0x1FA00-0x1FA6F,"  # Chess Symbols
        "0x1FA70-0x1FAFF"  # Symbols and Pictographs Extended-A
    ),
}

# Map languages to their required Unicode ranges
LANGUAGE_RANGES = {
    "cs": ["latin", "latin_extended"],  # Czech
    "de_DE": ["latin", "latin_extended"],  # German
    "el": ["latin", "greek"],  # Greek
    "en_GB": ["latin"],  # British English
    "en_US": ["latin"],  # US English
    "en_x_pirate": ["latin"],  # Pirate English
    "es": ["latin", "latin_extended"],  # Spanish
    "fil": ["latin"],  # Filipino
    "fr": ["latin", "latin_extended"],  # French
    "hi": ["latin", "devanagari"],  # Hindi
    "ID": ["latin"],  # Indonesian
    "it_IT": ["latin", "latin_extended"],  # Italian
    "ja": ["latin", "japanese"],  # Japanese
    "ko": ["latin", "korean"],  # Korean
    "nl": ["latin", "latin_extended"],  # Dutch
    "pl": ["latin", "latin_extended"],  # Polish
    "pt_BR": ["latin", "latin_extended"],  # Brazilian Portuguese
    "ru": ["latin", "cyrillic"],  # Russian
    "sv": ["latin", "latin_extended"],  # Swedish
    "tr": ["latin", "latin_extended"],  # Turkish
    "zh_Latn_pinyin": ["latin", "latin_extended"],  # Pinyin
}

def get_unicode_ranges(language: str) -> List[str]:
    """Get the Unicode ranges for a specific language.
    Splits ranges based on the font format requirements, considering:
    - Format 0: Direct 1-byte mapping (0x0000-0x00FF)
    - Format 2: Range-to-range mapping
    - Format 3: Sparse entries with delta encoding
    """
    if language not in LANGUAGE_RANGES:
        raise ValueError(f"Unsupported language: {language}")

    ranges = set()
    # Always include emoji ranges
    ranges.add(UNICODE_RANGES["emoji"])
    for script in LANGUAGE_RANGES[language]:
        ranges.add(UNICODE_RANGES[script])

    # Split ranges into low (unifont) and high (unifont_upper) ranges
    low_ranges = []
    high_ranges = []

    for range_str in ranges:
        for part in range_str.split(","):
            start, end = split_range(part)
            # Use unifont_upper for anything above 0x10000
            if start >= 0x10000:
                high_ranges.append(part)
            else:
                low_ranges.append(part)

    # Sort ranges for better subtable organization
    low_ranges.sort(key=lambda x: split_range(x)[0])
    high_ranges.sort(key=lambda x: split_range(x)[0])

    return [",".join(low_ranges), ",".join(high_ranges)]

def main():
    parser = argparse.ArgumentParser(description="Generate fonts using lv_font_conv")
    parser.add_argument("language", help="Language code (e.g., en_US, fr, ja)")
    parser.add_argument("--output", required=True, help="Output font file path")
    parser.add_argument("--size", type=int, default=16, help="Font size in pixels")
    parser.add_argument("--bpp", type=int, default=1, help="Bits per pixel")

    args = parser.parse_args()

    low_ranges, high_ranges = get_unicode_ranges(args.language)

    # For Japanese, use unifont_jp instead of unifont
    base_font = UNIFONT_JP_PATH if args.language == "ja" else UNIFONT_PATH
    cmd = [
        "lv_font_conv",
        "--font",
        base_font,
        "--autohint-off",
        "-r",
        low_ranges,
    ]

    # Add high ranges with upper font if needed
    if high_ranges:
        cmd.extend(["--font", UNIFONT_UPPER_PATH, "--autohint-off", "-r", high_ranges])

    # Add Nerd Font with private use area
    cmd.extend(["--font", NERD_FONT_PATH, "-r", NERD_FONT_RANGE])

    # Add common arguments
    cmd.extend(
        [
            "--size",
            str(args.size),
            "--format",
            "bin",
            "--bpp",
            str(args.bpp),
            "--no-compress",
            "-o",
            args.output,
        ]
    )

    try:
        print("Running command:")
        print(" ".join(cmd))
        subprocess.run(cmd, check=True)
        print(f"Generated font for {args.language} at {args.output}")
    except subprocess.CalledProcessError as e:
        print(f"Error running lv_font_conv: {e}")
        return 1
    except FileNotFoundError:
        print(
            "Error: lv_font_conv not found. Please install it using: npm install -g lv_font_conv"
        )
        return 1

    return 0

if __name__ == "__main__":
    exit(main())
