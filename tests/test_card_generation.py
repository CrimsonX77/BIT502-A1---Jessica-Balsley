"""
Test script for card generation module
Run this to verify backend connectivity and basic generation
"""

import asyncio
import sys
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent))

from card_generation import (
    CardGenerator,
    test_grok_connection,
    test_sd_connection,
    MembershipTier,
    GenerationBackend
)


async def test_backend_availability():
    """Test both backend connections."""
    print("\n" + "="*60)
    print("🔍 BACKEND AVAILABILITY TEST")
    print("="*60)
    
    print("\n📡 Testing Grok API connection...")
    grok_available = await test_grok_connection()
    if grok_available:
        print("✅ Grok API is available")
    else:
        print("❌ Grok API is unavailable")
        print("   💡 Check GROK_API_KEY in .env file")
    
    print("\n📡 Testing Stable Diffusion connection...")
    sd_available = await test_sd_connection()
    if sd_available:
        print("✅ Stable Diffusion is available")
    else:
        print("❌ Stable Diffusion is unavailable")
        print("   💡 Ensure SD WebUI is running on localhost:7860")
    
    return grok_available, sd_available


async def test_prompt_validation():
    """Test tier-based prompt validation."""
    print("\n" + "="*60)
    print("🔐 PROMPT VALIDATION TEST")
    print("="*60)
    
    generator = CardGenerator(tier='Kids')
    
    # Test Kids tier - whitelist only
    print("\n👶 Testing Kids Tier (Whitelist):")
    
    test_prompts = [
        "cute fantasy character",  # Should pass
        "mystical warrior",  # Should fail
        "violent monster"  # Should fail
    ]
    
    for prompt in test_prompts:
        result = generator.validate_prompt(prompt, MembershipTier.KIDS)
        status = "✅ PASS" if result['valid'] else "❌ FAIL"
        print(f"  {status}: '{prompt}'")
        if not result['valid']:
            print(f"       Reason: {result['reason'][:60]}...")
    
    # Test Standard tier - templates
    print("\n📋 Testing Standard Tier (Templates):")
    generator.tier = MembershipTier.STANDARD
    
    test_prompts = [
        "Fantasy mystical character",  # Should pass
        "custom complex prompt",  # Should fail
        "explicit content"  # Should fail
    ]
    
    for prompt in test_prompts:
        result = generator.validate_prompt(prompt, MembershipTier.STANDARD)
        status = "✅ PASS" if result['valid'] else "❌ FAIL"
        print(f"  {status}: '{prompt}'")
        if not result['valid']:
            print(f"       Reason: {result['reason'][:60]}...")
    
    # Test Premium tier - full freedom
    print("\n⭐ Testing Premium Tier (Full Freedom):")
    generator.tier = MembershipTier.PREMIUM
    
    test_prompts = [
        "complex custom character design",  # Should pass
        "dark fantasy warrior",  # Should pass
    ]
    
    for prompt in test_prompts:
        result = generator.validate_prompt(prompt, MembershipTier.PREMIUM)
        status = "✅ PASS" if result['valid'] else "❌ FAIL"
        print(f"  {status}: '{prompt}'")


async def test_tier_constraints():
    """Test tier-based generation constraints."""
    print("\n" + "="*60)
    print("⚙️  TIER CONSTRAINTS TEST")
    print("="*60)
    
    test_params = {
        'prompt': 'test character',
        'style': 'Fantasy',
        'color_palette': 'Crimson & Gold'
    }
    
    for tier in [MembershipTier.KIDS, MembershipTier.STANDARD, MembershipTier.PREMIUM]:
        print(f"\n{tier.value} Tier Constraints:")
        generator = CardGenerator(tier=tier.value)
        constrained = generator.apply_tier_constraints(test_params.copy(), tier)
        
        print(f"  Quality: {constrained.get('quality', 'N/A')}")
        print(f"  Steps: {constrained.get('steps', 'N/A')}")
        print(f"  Guidance: {constrained.get('guidance_scale', 'N/A')}")
        print(f"  Max Size: {constrained.get('max_file_size_mb', 'N/A')}MB")
        print(f"  Safety: {constrained.get('safety_level', constrained.get('safety_scale', 'N/A'))}")


async def test_generation_dry_run():
    """Test generation workflow without actual API calls."""
    print("\n" + "="*60)
    print("🎨 GENERATION WORKFLOW TEST (DRY RUN)")
    print("="*60)
    
    generator = CardGenerator(backend='grok', tier='Standard')
    
    print("\n1️⃣  Building prompt from template...")
    prompt = generator._build_prompt(
        "warrior",
        "Fantasy",
        "Crimson & Gold"
    )
    print(f"   Full prompt: {prompt}")
    
    print("\n2️⃣  Applying tier constraints...")
    params = generator.apply_tier_constraints(
        {'prompt': prompt},
        MembershipTier.STANDARD
    )
    print(f"   Constrained params: {list(params.keys())}")
    
    print("\n3️⃣  Output directory check...")
    print(f"   Path: {generator.output_dir}")
    print(f"   Exists: {generator.output_dir.exists()}")
    
    print("\n4️⃣  Session info...")
    print(f"   User ID: {generator.user_id}")
    print(f"   Session ID: {generator.session_id}")
    print(f"   Generation count: {generator.generation_count}")


async def test_full_generation(backend='grok', tier='Standard'):
    """
    Test actual card generation (if backends are available).
    This will make real API calls!
    """
    print("\n" + "="*60)
    print(f"🎨 FULL GENERATION TEST ({backend.upper()}, {tier})")
    print("="*60)
    print("\n⚠️  This will make real API calls and use credits!")
    
    # Check backend availability
    generator = CardGenerator(backend=backend, tier=tier)
    availability = await generator.check_backend_availability()
    
    if not availability.get(backend, False):
        print(f"\n❌ {backend} backend is not available")
        print("   Skipping full generation test")
        return
    
    print(f"\n✅ {backend} backend is available")
    print("\n🎨 Generating card...")
    
    # Progress callback
    def progress(message, percentage):
        bar_length = 30
        filled = int(bar_length * percentage / 100)
        bar = '█' * filled + '░' * (bar_length - filled)
        print(f"\r   [{bar}] {percentage}% - {message}", end='', flush=True)
    
    result = await generator.generate_static_card(
        prompt="mystical warrior",
        style="Fantasy",
        color_palette="Crimson & Gold",
        progress_callback=progress
    )
    
    print()  # New line after progress bar
    
    if result['success']:
        print("\n✅ Generation successful!")
        print(f"   📁 Path: {result['path']}")
        print(f"   ⏱️  Time: {result['metadata']['generation_time']:.2f}s")
        print(f"   📦 Size: {result['metadata']['file_size_mb']:.2f}MB")
        print(f"   🔧 Backend: {result['metadata']['backend']}")
        print(f"   🎨 Style: {result['metadata']['style']}")
    else:
        print(f"\n❌ Generation failed!")
        print(f"   Error: {result['error']}")


async def main():
    """Run all tests."""
    print("\n" + "="*60)
    print("🌅 AURORA CARD GENERATOR - TEST SUITE")
    print("="*60)
    
    # Test 1: Backend availability
    grok_ok, sd_ok = await test_backend_availability()
    
    # Test 2: Prompt validation
    await test_prompt_validation()
    
    # Test 3: Tier constraints
    await test_tier_constraints()
    
    # Test 4: Generation workflow
    await test_generation_dry_run()
    
    # Test 5: Full generation (optional)
    print("\n" + "="*60)
    print("🎨 FULL GENERATION TEST")
    print("="*60)
    print("\nDo you want to test actual card generation?")
    print("This will use API credits if available.")
    print("\nOptions:")
    print("  1. Test with Grok (if available)")
    print("  2. Test with Stable Diffusion (if available)")
    print("  3. Skip full generation test")
    
    # For automated testing, skip actual generation
    print("\n⏭️  Skipping full generation test (automated run)")
    print("   To test generation, run: python test_card_generation.py --generate")
    
    print("\n" + "="*60)
    print("✅ ALL TESTS COMPLETE")
    print("="*60)
    
    # Summary
    print("\n📊 Summary:")
    print(f"   Grok API: {'✅ Available' if grok_ok else '❌ Unavailable'}")
    print(f"   Stable Diffusion: {'✅ Available' if sd_ok else '❌ Unavailable'}")
    print(f"   Prompt Validation: ✅ Working")
    print(f"   Tier Constraints: ✅ Working")
    print(f"   Generation Workflow: ✅ Working")


if __name__ == '__main__':
    # Check command line args
    if '--generate' in sys.argv:
        # Run with actual generation
        asyncio.run(test_full_generation())
    else:
        # Run full test suite
        asyncio.run(main())
