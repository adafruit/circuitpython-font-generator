# CircuitPython Font Generator

This tool generates optimized fonts for CircuitPython using the `lv_font_conv` converter. It supports multiple languages and scripts, including Latin, Cyrillic, Greek, Japanese, Korean, Chinese, and more.

## Prerequisites

- Python 3.7 or later
- Node.js and npm (for lv_font_conv)
- lv_font_conv: `npm install -g lv_font_conv`

## Installation

1. Clone this repository:
```bash
git clone https://github.com/adafruit/circuitpython-font-generator.git
cd circuitpython-font-generator
```

2. The required font files are included in the repository:
- unifont-16.0.02.otf (Basic Unicode coverage)
- unifont_upper-16.0.02.otf (Extended Unicode coverage)
- unifont_jp-16.0.02.otf (Japanese-optimized font)
- SymbolsNerdFontMono-Regular.ttf (Icons and symbols)

## Usage

```bash
python3 generate_font.py [language] --output [output_file] [options]
```

### Arguments

- `language`: Language code (e.g., en_US, fr, ja)
- `--output`: Output font file path (required)
- `--size`: Font size in pixels (default: 16)
- `--bpp`: Bits per pixel (default: 1)

### Supported Languages

- cs (Czech)
- de_DE (German)
- el (Greek)
- en_GB (British English)
- en_US (US English)
- en_x_pirate (Pirate English)
- es (Spanish)
- fil (Filipino)
- fr (French)
- hi (Hindi)
- ID (Indonesian)
- it_IT (Italian)
- ja (Japanese)
- ko (Korean)
- nl (Dutch)
- pl (Polish)
- pt_BR (Brazilian Portuguese)
- ru (Russian)
- sv (Swedish)
- tr (Turkish)
- zh_Latn_pinyin (Pinyin)

### Example

Generate a US English font:
```bash
python3 generate_font.py en_US --output en_US.lvfontbin
```

## License

This project is licensed under the MIT License. The included fonts have their own licenses:
- Unifont: GNU GPL v2 or later, with the GNU font embedding exception
- Nerd Fonts: MIT License
