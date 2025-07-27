"""
Font downloader utility for Certificate Generator
Downloads Great Vibes font from Google Fonts
"""

import os
import requests
from pathlib import Path

def download_great_vibes_font():
    """Download Great Vibes font from Google Fonts GitHub repository"""
    font_url = "https://github.com/google/fonts/raw/main/ofl/greatvibes/GreatVibes-Regular.ttf"
    font_path = "CERTIFICATE GENERATOR/fonts/GreatVibes-Regular.ttf"
    
    # Create fonts directory if it doesn't exist
    font_dir = os.path.dirname(font_path)
    os.makedirs(font_dir, exist_ok=True)
    
    print("📥 Downloading Great Vibes font...")
    
    try:
        response = requests.get(font_url, timeout=30)
        response.raise_for_status()
        
        with open(font_path, 'wb') as f:
            f.write(response.content)
        
        print(f"✅ Font downloaded successfully to {font_path}")
        print(f"📊 Font size: {len(response.content)} bytes")
        return True
        
    except requests.exceptions.RequestException as e:
        print(f"❌ Error downloading font: {e}")
        print("💡 You can manually download the font from:")
        print("   https://fonts.google.com/specimen/Great+Vibes")
        return False

if __name__ == "__main__":
    download_great_vibes_font()
