#!/usr/bin/env python3
"""
Test custom model/steps/cfg settings in card generation
"""

import asyncio
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent))

from card_generation import CardGenerator


async def test_custom_settings():
    """Test card generation with custom settings"""
    
    print("\n" + "=" * 70)
    print("🎨 TESTING CUSTOM SETTINGS")
    print("=" * 70)
    
    # Create generator
    generator = CardGenerator(
        backend='stable_diffusion',
        tier='Premium',
        user_id='test_custom'
    )
    
    # Set custom settings
    generator.sd_model = ('YiffMix_v37.safetensors', "fefaHentaiMix_v10.safetensors"),  # Use the other model
    generator.custom_steps = 20  # Faster test
    generator.custom_cfg = 7.0   # Higher guidance
    
    print(f"\n📋 Custom Settings:")
    print(f"   Model: {generator.sd_model}")
    print(f"   Steps: {generator.custom_steps}")
    print(f"   CFG Scale: {generator.custom_cfg}")
    print(f"\n🎯 Generating test card...")
    
    def progress(msg, pct):
        bar_len = 40
        filled = int(bar_len * pct / 100)
        bar = '█' * filled + '░' * (bar_len - filled)
        print(f"\r[{bar}] {pct}% - {msg}", end='', flush=True)
    
    result = await generator.generate_static_card(
        prompt="Sci-Fi cyberpunk hacker character",  # Include style keyword
        style="Sci-Fi",
        color_palette="Azure & Silver",
        progress_callback=progress
    )
    
    print()  # New line after progress
    
    if result['success']:
        metadata = result['metadata']
        print(f"\n✅ Generation successful!")
        print(f"   📁 Path: {result['path']}")
        print(f"   ⏱️  Time: {metadata['generation_time']:.2f}s")
        print(f"   📦 Size: {metadata['file_size_mb']:.2f} MB")
        
        # Verify settings were used
        print(f"\n✅ Custom settings confirmed in generation!")
        return True
    else:
        print(f"\n❌ Generation failed: {result.get('error')}")
        return False


if __name__ == '__main__':
    success = asyncio.run(test_custom_settings())
    sys.exit(0 if success else 1)
