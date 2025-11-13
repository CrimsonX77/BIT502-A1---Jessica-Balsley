#!/usr/bin/env python3
"""
Test script for card generation with Grok API
"""

import asyncio
import sys
from pathlib import Path
from card_generation import CardGenerator

async def test_grok_generation():
    """Test Grok image generation"""
    
    print("🔮 Testing Aurora Card Generation with Grok API\n")
    print("=" * 60)
    
    # Initialize generator
    print("Initializing CardGenerator with Grok backend...")
    generator = CardGenerator(
        backend='grok',
        tier='Premium',
        user_id='test_user'
    )
    
    # Test prompt
    prompt = "A mystical fantasy warrior with flowing silver hair and piercing blue eyes, wearing elegant armor with arcane symbols, surrounded by ethereal purple energy"
    
    print(f"\nPrompt: {prompt}\n")
    print("=" * 60)
    
    # Progress callback
    def on_progress(message: str, percentage: int):
        bar_length = 40
        filled = int(bar_length * percentage / 100)
        bar = '█' * filled + '░' * (bar_length - filled)
        print(f"\r[{bar}] {percentage}% - {message}", end='', flush=True)
    
    try:
        # Generate card
        print("\nGenerating card...\n")
        result = await generator.generate_static_card(
            prompt=prompt,
            style='Fantasy',
            color_palette='azure_silver',
            progress_callback=on_progress
        )
        
        print("\n\n" + "=" * 60)
        
        if result['success']:
            print("✓ Generation successful!\n")
            print(f"📁 Image saved to: {result['path']}")
            print(f"📊 File size: {result['metadata']['file_size_mb']:.2f} MB")
            print(f"⏱️  Generation time: {result['metadata']['generation_time']:.2f}s")
            print(f"🔧 Backend: {result['metadata']['backend']}")
            
            # Check if file exists
            if Path(result['path']).exists():
                print(f"\n✓ File verified: {result['path']}")
                return True
            else:
                print(f"\n❌ File not found: {result['path']}")
                return False
        else:
            print(f"❌ Generation failed: {result['error']}")
            return False
            
    except Exception as e:
        print(f"\n❌ Error: {str(e)}")
        import traceback
        traceback.print_exc()
        return False

async def test_backend_status():
    """Test backend connectivity"""
    
    print("\n" + "=" * 60)
    print("Testing backend connectivity...\n")
    
    generator = CardGenerator(backend='grok', tier='Premium')
    
    try:
        status = await generator.check_backend_status()
        
        print("Backend Status:")
        print(f"  Grok API: {'✓ Connected' if status.get('grok', {}).get('available') else '❌ Not available'}")
        print(f"  Stable Diffusion: {'✓ Connected' if status.get('stable_diffusion', {}).get('available') else '❌ Not available'}")
        
        if status.get('grok', {}).get('available'):
            print(f"\n  Grok Details:")
            print(f"    API URL: {generator.grok_base_url}")
            print(f"    Model: grok-2-image-1212")
        
        return status
        
    except Exception as e:
        print(f"❌ Status check failed: {str(e)}")
        return None

async def main():
    """Main test runner"""
    
    print("\n🌟 Aurora Archive - Card Generation Test\n")
    
    # Test 1: Backend status
    status = await test_backend_status()
    
    # Test 2: Generate test image
    success = await test_grok_generation()
    
    print("\n" + "=" * 60)
    if success:
        print("✓ All tests passed!")
        print("\nYou can now use the member registration app.")
        return 0
    else:
        print("❌ Tests failed. Check configuration.")
        return 1

if __name__ == '__main__':
    exit_code = asyncio.run(main())
    sys.exit(exit_code)
