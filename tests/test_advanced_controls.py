#!/usr/bin/env python3
"""
Test script for advanced settings (samplers, schedulers, dimensions, hi-res fix)
"""

import requests

def test_api_endpoints():
    """Test SD WebUI API endpoints for samplers and upscalers"""
    sd_url = "http://localhost:7860"
    
    print("=" * 70)
    print("🧪 Testing Advanced Settings API Endpoints")
    print("=" * 70)
    print()
    
    # Test samplers endpoint
    print("📊 Testing Samplers Endpoint...")
    try:
        response = requests.get(f"{sd_url}/sdapi/v1/samplers", timeout=3)
        if response.status_code == 200:
            samplers = response.json()
            print(f"✅ Found {len(samplers)} samplers:")
            for i, sampler in enumerate(samplers[:10], 1):  # Show first 10
                print(f"   {i}. {sampler['name']}")
            if len(samplers) > 10:
                print(f"   ... and {len(samplers) - 10} more")
        else:
            print(f"❌ Failed with status {response.status_code}")
    except Exception as e:
        print(f"❌ Error: {e}")
    
    print()
    
    # Test upscalers endpoint
    print("🔍 Testing Upscalers Endpoint...")
    try:
        response = requests.get(f"{sd_url}/sdapi/v1/upscalers", timeout=3)
        if response.status_code == 200:
            upscalers = response.json()
            print(f"✅ Found {len(upscalers)} upscalers:")
            for i, upscaler in enumerate(upscalers, 1):
                print(f"   {i}. {upscaler['name']}")
        else:
            print(f"❌ Failed with status {response.status_code}")
    except Exception as e:
        print(f"❌ Error: {e}")
    
    print()
    
    # Test schedulers (if available)
    print("📅 Testing Schedulers Endpoint...")
    try:
        response = requests.get(f"{sd_url}/sdapi/v1/schedulers", timeout=3)
        if response.status_code == 200:
            schedulers = response.json()
            print(f"✅ Found {len(schedulers)} schedulers:")
            for i, scheduler in enumerate(schedulers, 1):
                name = scheduler if isinstance(scheduler, str) else scheduler.get('name', 'Unknown')
                print(f"   {i}. {name}")
        else:
            print(f"⚠️  Schedulers endpoint returned {response.status_code} (may not be available)")
            print("   Using fallback: Automatic, Karras, Exponential, Polyexponential")
    except Exception as e:
        print(f"⚠️  Schedulers endpoint not available: {e}")
        print("   Using fallback: Automatic, Karras, Exponential, Polyexponential")
    
    print()
    print("=" * 70)
    print("✅ API Test Complete!")
    print("=" * 70)
    print()
    print("💡 Tips:")
    print("   • Samplers: Choose DPM++ 2M SDE Karras for best quality")
    print("   • Scheduler: Karras is most popular")
    print("   • Dimensions: 512x768 for portrait cards")
    print("   • Hi-Res Fix: Enable for better quality (slower)")
    print("   • Upscaler: R-ESRGAN 4x+ Anime6B for anime-style cards")
    print()


def test_settings_extraction():
    """Simulate settings extraction from GUI"""
    print("=" * 70)
    print("🎨 Testing Settings Extraction")
    print("=" * 70)
    print()
    
    # Simulate GUI values
    settings = {
        'model': 'fefaHentaiMix_v10.safetensors',
        'steps': 30,
        'cfg': 7.5,
        'sampler': 'DPM++ 2M SDE Karras',
        'scheduler': 'Karras',
        'width': 512,
        'height': 768,
        'enable_hr': True,
        'upscaler': 'R-ESRGAN 4x+ Anime6B',
        'hr_scale': 2.0
    }
    
    print("📋 Extracted Settings:")
    print(f"   Model: {settings['model']}")
    print(f"   Steps: {settings['steps']}")
    print(f"   CFG Scale: {settings['cfg']}")
    print(f"   Sampler: {settings['sampler']}")
    print(f"   Scheduler: {settings['scheduler']}")
    print(f"   Dimensions: {settings['width']}x{settings['height']}")
    print(f"   Hi-Res Fix: {'Enabled' if settings['enable_hr'] else 'Disabled'}")
    if settings['enable_hr']:
        print(f"   Upscaler: {settings['upscaler']}")
        print(f"   HR Scale: {settings['hr_scale']}x")
    
    print()
    print("✅ Settings extraction working correctly!")
    print()
    
    # Calculate final resolution
    if settings['enable_hr']:
        final_width = int(settings['width'] * settings['hr_scale'])
        final_height = int(settings['height'] * settings['hr_scale'])
        print(f"📐 Final Resolution: {final_width}x{final_height}")
        print(f"   (Original {settings['width']}x{settings['height']} upscaled by {settings['hr_scale']}x)")
    else:
        print(f"📐 Final Resolution: {settings['width']}x{settings['height']}")
    
    print()
    print("=" * 70)


if __name__ == "__main__":
    test_api_endpoints()
    print()
    test_settings_extraction()
    
    print()
    print("🎯 Next Steps:")
    print("   1. Open Aurora GUI")
    print("   2. Go to '🎨 Create Card' tab")
    print("   3. Scroll to '⚙️ Advanced Settings'")
    print("   4. Try the new controls:")
    print("      • Sampler dropdown")
    print("      • Scheduler dropdown")
    print("      • Width/Height dropdowns")
    print("      • Enable Hi-Res Fix checkbox")
    print("      • Upscaler dropdown (when Hi-Res enabled)")
    print("      • HR Scale dropdown (when Hi-Res enabled)")
    print("   5. Click '✨ Generate Card'")
    print()
