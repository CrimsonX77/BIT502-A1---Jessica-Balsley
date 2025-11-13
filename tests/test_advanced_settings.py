#!/usr/bin/env python3
"""
Test Stable Diffusion with advanced settings:
- High-res fix
- Custom sampler
- Clip skip
- Model override
"""

import asyncio
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent))

from card_generation import CardGenerator


async def test_advanced_settings():
    """Test SD generation with all advanced settings"""
    
    print("\n" + "=" * 70)
    print("🎨 TESTING ADVANCED SD SETTINGS")
    print("=" * 70)
    
    # Test with Standard tier (30 steps, HR fix enabled)
    generator = CardGenerator(
        backend='stable_diffusion',
        tier='Standard',
        user_id='test_advanced'
    )
    
    print(f"\n✓ Generator initialized")
    print(f"  Model: {generator.sd_model}")
    print(f"  Sampler: {generator.sd_sampler}")
    print(f"  Clip Skip: {generator.sd_clip_skip}")
    print(f"  HR Fix: {generator.sd_enable_hr}")
    print(f"  HR Upscaler: {generator.sd_hr_upscaler}")
    print(f"  HR Scale: {generator.sd_hr_scale}x")
    
    # Get tier settings
    tier_settings = generator._get_tier_sd_settings()
    print(f"\n📊 Standard Tier Settings:")
    print(f"  Steps: {tier_settings['steps']}")
    print(f"  HR Steps: {tier_settings['hr_steps']}")
    print(f"  Denoising: {tier_settings['denoising']}")
    
    print("\n" + "-" * 70)
    print("Generating test card...")
    print("-" * 70)
    
    def progress(msg, pct):
        bar_len = 40
        filled = int(bar_len * pct / 100)
        bar = '█' * filled + '░' * (bar_len - filled)
        print(f"\r[{bar}] {pct}% - {msg}", end='', flush=True)
    
    result = await generator.generate_static_card(
        prompt="Fantasy mystical Sexy warrior Girls",
        style="Fantasy",
        color_palette="Silver And Azure",
        progress_callback=progress
    )
    
    print()  # New line after progress
    
    if result['success']:
        metadata = result['metadata']
        print(f"\n✅ Generation successful!")
        print(f"   📁 Path: {result['path']}")
        print(f"   ⏱️  Time: {metadata['generation_time']:.2f}s")
        print(f"   📦 Size: {metadata['file_size_mb']:.2f} MB")
        print(f"   🎨 Backend: {metadata['backend']}")
        print(f"   📝 Full Prompt: {metadata['prompt'][:80]}...")
        
        # Check file exists and read dimensions
        try:
            from PIL import Image
            img = Image.open(result['path'])
            width, height = img.size
            print(f"   📐 Dimensions: {width}x{height}px")
            
            # Calculate expected dimensions with HR fix
            expected_w = int(512 * generator.sd_hr_scale)
            expected_h = int(768 * generator.sd_hr_scale)
            if width == expected_w and height == expected_h:
                print(f"   ✅ HR Fix applied correctly! ({expected_w}x{expected_h})")
            else:
                print(f"   ⚠️  Unexpected size (expected {expected_w}x{expected_h})")
        except ImportError:
            print(f"   ℹ️  Install Pillow to check image dimensions: pip install Pillow")
        except Exception as e:
            print(f"   ⚠️  Could not read image: {e}")
        
        return True
    else:
        print(f"\n❌ Generation failed!")
        print(f"   Error: {result['error']}")
        return False


async def test_all_tiers():
    """Test generation for all tiers"""
    
    print("\n" + "=" * 70)
    print("🎯 TESTING ALL TIERS WITH NEW SETTINGS")
    print("=" * 70)
    
    results = {}
    
    for tier in ['Kids', 'Standard', 'Premium']:
        print(f"\n{'─' * 70}")
        print(f"Testing {tier} Tier")
        print('─' * 70)
        
        generator = CardGenerator(
            backend='stable_diffusion',
            tier=tier,
            user_id=f'test_{tier.lower()}'
        )
        
        settings = generator._get_tier_sd_settings()
        print(f"Settings: {settings['steps']} steps, "
              f"{settings['hr_steps']} HR steps, "
              f"{settings['denoising']} denoising")
        
        # Use appropriate prompt for tier
        if tier == 'Kids':
            prompt = "cute fantasy character"
        elif tier == 'Standard':
            prompt = "Fantasy brave knight"
        else:
            prompt = "epic fantasy warrior with glowing armor"
        
        result = await generator.generate_static_card(
            prompt=prompt,
            style="Fantasy",
            color_palette="Azure & Silver",
            progress_callback=lambda m, p: None  # Silent
        )
        
        results[tier] = result['success']
        
        if result['success']:
            print(f"✅ {tier}: Generated in {result['metadata']['generation_time']:.1f}s")
            print(f"   Path: {result['path']}")
        else:
            print(f"❌ {tier}: Failed - {result['error']}")
    
    # Summary
    print("\n" + "=" * 70)
    print("📊 SUMMARY")
    print("=" * 70)
    
    for tier, success in results.items():
        status = "✅" if success else "❌"
        print(f"{status} {tier} Tier")
    
    total = len(results)
    passed = sum(results.values())
    print(f"\n🎯 Success Rate: {passed}/{total} ({passed/total*100:.0f}%)")


async def main():
    """Run all tests"""
    
    print("\n" + "🌅" * 35)
    print("AURORA ARCHIVE - ADVANCED SD SETTINGS TEST")
    print("🌅" * 35)
    
    try:
        # Test 1: Advanced settings with current setup
        success = await test_advanced_settings()
        
        if success:
            # Test 2: All tiers if first test passed
            await test_all_tiers()
        
        print("\n" + "=" * 70)
        print("✅ All tests complete!")
        print("=" * 70 + "\n")
        
    except Exception as e:
        print(f"\n❌ Test failed with error: {e}")
        import traceback
        traceback.print_exc()


if __name__ == '__main__':
    asyncio.run(main())
