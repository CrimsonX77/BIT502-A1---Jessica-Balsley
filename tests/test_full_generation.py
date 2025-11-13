#!/usr/bin/env python3
"""
Test card_generation.py with Stable Diffusion backend
"""

import asyncio
import sys
from pathlib import Path

# Add current directory to path
sys.path.insert(0, str(Path(__file__).parent))

from card_generation import CardGenerator, MembershipTier


def progress_callback(message: str, percentage: int):
    """Print progress updates"""
    bar_length = 30
    filled = int(bar_length * percentage / 100)
    bar = '█' * filled + '░' * (bar_length - filled)
    print(f"\r[{bar}] {percentage}% - {message}", end='', flush=True)


async def test_standard_tier():
    """Test Standard tier with Stable Diffusion"""
    
    print("\n" + "=" * 70)
    print("🎨 TESTING CARD GENERATION - STANDARD TIER (STABLE DIFFUSION)")
    print("=" * 70 + "\n")
    
    # Initialize with SD backend
    generator = CardGenerator(
        backend='stable_diffusion',
        tier='Standard',
        user_id='test_user_sd'
    )
    
    print(f"✓ Generator initialized")
    print(f"  Backend: Stable Diffusion")
    print(f"  Tier: Standard")
    print(f"  User: test_user_sd\n")
    
    # Test 1: Template-based prompt for Standard tier
    # For Standard tier, just provide character description
    # The style parameter triggers template usage
    print("📝 Test 1: Generating card with 'warrior' character...")
    print("-" * 70)
    
    result = await generator.generate_static_card(
        prompt="Fantasy warrior",  # Must include style keyword for validation
        style="Fantasy",
        color_palette="Crimson & Gold",
        progress_callback=progress_callback
    )
    
    print()  # New line after progress bar
    
    if result['success']:
        print(f"✅ Generation successful!")
        print(f"   📁 Path: {result['path']}")
        print(f"   ⏱️  Time: {result['metadata']['generation_time']:.2f}s")
        print(f"   📦 Size: {result['metadata']['file_size_mb']:.2f} MB")
        print(f"   🎨 Style: {result['metadata']['style']}")
    else:
        print(f"❌ Generation failed: {result['error']}")
    
    return result


async def test_kids_tier():
    """Test Kids tier with whitelisted prompt"""
    
    print("\n" + "=" * 70)
    print("👶 TESTING CARD GENERATION - KIDS TIER (STABLE DIFFUSION)")
    print("=" * 70 + "\n")
    
    generator = CardGenerator(
        backend='stable_diffusion',
        tier='Kids',
        user_id='test_kid_sd'
    )
    
    print(f"✓ Generator initialized")
    print(f"  Backend: Stable Diffusion")
    print(f"  Tier: Kids")
    print(f"  User: test_kid_sd\n")
    
    # Use a whitelisted prompt
    print("📝 Generating 'cute fantasy character' card...")
    print("-" * 70)
    
    result = await generator.generate_static_card(
        prompt="cute fantasy character",
        style="Fantasy",
        color_palette="Azure & Silver",
        progress_callback=progress_callback
    )
    
    print()  # New line after progress bar
    
    if result['success']:
        print(f"✅ Generation successful!")
        print(f"   📁 Path: {result['path']}")
        print(f"   ⏱️  Time: {result['metadata']['generation_time']:.2f}s")
        print(f"   📦 Size: {result['metadata']['file_size_mb']:.2f} MB")
    else:
        print(f"❌ Generation failed: {result['error']}")
    
    return result


async def test_premium_tier():
    """Test Premium tier with custom prompt"""
    
    print("\n" + "=" * 70)
    print("⭐ TESTING CARD GENERATION - PREMIUM TIER (STABLE DIFFUSION)")
    print("=" * 70 + "\n")
    
    generator = CardGenerator(
        backend='stable_diffusion',
        tier='Premium',
        user_id='test_premium_sd'
    )
    
    print(f"✓ Generator initialized")
    print(f"  Backend: Stable Diffusion")
    print(f"  Tier: Premium")
    print(f"  User: test_premium_sd\n")
    
    # Custom detailed prompt
    print("📝 Generating custom card with detailed prompt...")
    print("-" * 70)
    
    result = await generator.generate_static_card(
        prompt="cyberpunk samurai with neon katana, futuristic cityscape background, ((NSFW:1.5)), ((Yuri:1.4)), ((Loli:1.2)), ((Fantasy:1.3)), ((Sci-Fi:1.1)), ((Intense details)), ((High resolution)), ((Lesbian_Sex:1.5)), ((Females:1.2)), ((Furry:1.4)), ((Yiff:1.5)), ((Explicit:1.3))",
        style="Sci-Fi",
        color_palette="Violet & White",
        progress_callback=progress_callback
    )
    
    print()  # New line after progress bar
    
    if result['success']:
        print(f"✅ Generation successful!")
        print(f"   📁 Path: {result['path']}")
        print(f"   ⏱️  Time: {result['metadata']['generation_time']:.2f}s")
        print(f"   📦 Size: {result['metadata']['file_size_mb']:.2f} MB")
    else:
        print(f"❌ Generation failed: {result['error']}")
    
    return result


async def test_backend_availability():
    """Test which backends are available"""
    
    print("\n" + "=" * 70)
    print("🔍 TESTING BACKEND AVAILABILITY")
    print("=" * 70 + "\n")
    
    generator = CardGenerator()
    availability = await generator.check_backend_availability()
    
    print(f"Grok API: {'✅ Available' if availability['grok'] else '❌ Unavailable'}")
    print(f"Stable Diffusion: {'✅ Available' if availability['stable_diffusion'] else '❌ Unavailable'}")
    
    return availability


async def main():
    """Run all tests"""
    
    print("\n" + "🌅" * 35)
    print("AURORA ARCHIVE - CARD GENERATION MODULE TEST")
    print("Testing with Stable Diffusion Backend")
    print("🌅" * 35)
    
    # Check backend availability first
    availability = await test_backend_availability()
    
    if not availability['stable_diffusion']:
        print("\n❌ Stable Diffusion is not available!")
        print("💡 Make sure SD WebUI is running: http://localhost:7860")
        return
    
    # Run generation tests
    results = []
    
    # Test 1: Kids tier
    result1 = await test_kids_tier()
    results.append(('Kids Tier', result1))
    
    # Test 2: Standard tier
    result2 = await test_standard_tier()
    results.append(('Standard Tier', result2))
    
    # Test 3: Premium tier
    result3 = await test_premium_tier()
    results.append(('Premium Tier', result3))
    
    # Summary
    print("\n" + "=" * 70)
    print("📊 TEST SUMMARY")
    print("=" * 70)
    
    successful = sum(1 for _, r in results if r['success'])
    total = len(results)
    
    for name, result in results:
        status = "✅" if result['success'] else "❌"
        print(f"{status} {name}")
        if result['success']:
            print(f"   📁 {result['path']}")
    
    print(f"\n🎯 Success Rate: {successful}/{total} ({successful/total*100:.0f}%)")
    
    if successful == total:
        print("\n🎉 All tests passed! Stable Diffusion backend is working perfectly!")
    else:
        print(f"\n⚠️  {total - successful} test(s) failed")
    
    print("\n" + "=" * 70 + "\n")


if __name__ == '__main__':
    asyncio.run(main())
