#!/usr/bin/env python3
"""
Quick test for Stable Diffusion WebUI connection
Tests the /sdapi/v1/txt2img endpoint
"""

import asyncio
import aiohttp
import json
import base64
from pathlib import Path
from datetime import datetime


async def test_sd_endpoint():
    """Test Stable Diffusion txt2img endpoint"""
    
    url = "http://localhost:7860/sdapi/v1/txt2img"
    
    # Simple test payload
    payload = {
        "prompt": "a mystical warrior, fantasy art style, detailed",
        "negative_prompt": "blurry, low quality, distorted",
        "steps": 20,
        "cfg_scale": 7.0,
        "width": 512,
        "height": 512,
        "sampler_name": "Euler a",
        "seed": -1
    }
    
    print("=" * 60)
    print("🎨 STABLE DIFFUSION CONNECTION TEST")
    print("=" * 60)
    print(f"\n📡 Endpoint: {url}")
    print(f"📝 Prompt: {payload['prompt']}")
    print(f"⚙️  Settings: {payload['steps']} steps, {payload['width']}x{payload['height']}")
    print("\n🔄 Sending request...")
    
    try:
        timeout = aiohttp.ClientTimeout(total=120)  # 2 minutes for generation
        
        async with aiohttp.ClientSession(timeout=timeout) as session:
            start_time = datetime.now()
            
            async with session.post(url, json=payload) as response:
                print(f"📊 Response status: {response.status}")
                
                if response.status == 200:
                    data = await response.json()
                    end_time = datetime.now()
                    duration = (end_time - start_time).total_seconds()
                    
                    print(f"✅ Generation successful!")
                    print(f"⏱️  Duration: {duration:.2f} seconds")
                    
                    # Save the image
                    if 'images' in data and len(data['images']) > 0:
                        image_data = base64.b64decode(data['images'][0])
                        
                        # Create output directory
                        output_dir = Path("Assets/generated_cards")
                        output_dir.mkdir(parents=True, exist_ok=True)
                        
                        # Save with timestamp
                        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                        output_path = output_dir / f"test_sd_{timestamp}.png"
                        
                        with open(output_path, 'wb') as f:
                            f.write(image_data)
                        
                        file_size_mb = len(image_data) / (1024 * 1024)
                        print(f"💾 Image saved: {output_path}")
                        print(f"📦 File size: {file_size_mb:.2f} MB")
                        
                        return {
                            'success': True,
                            'path': str(output_path),
                            'duration': duration,
                            'file_size_mb': file_size_mb
                        }
                    else:
                        print("⚠️  No image data in response")
                        return {'success': False, 'error': 'No image data returned'}
                        
                else:
                    error_text = await response.text()
                    print(f"❌ Request failed!")
                    print(f"Error: {error_text[:200]}")
                    return {'success': False, 'error': error_text}
                    
    except aiohttp.ClientConnectorError:
        print("❌ Connection failed!")
        print("💡 Make sure Stable Diffusion WebUI is running on http://localhost:7860")
        print("   Start it with: cd stable-diffusion-webui && ./webui.sh --api")
        return {'success': False, 'error': 'Connection refused'}
        
    except asyncio.TimeoutError:
        print("❌ Request timed out!")
        print("💡 Generation took too long (>2 minutes)")
        return {'success': False, 'error': 'Timeout'}
        
    except Exception as e:
        print(f"❌ Unexpected error: {e}")
        return {'success': False, 'error': str(e)}


async def test_sd_models():
    """List available models"""
    
    url = "http://localhost:7860/sdapi/v1/sd-models"
    
    print("\n" + "=" * 60)
    print("📚 AVAILABLE MODELS")
    print("=" * 60)
    
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(url) as response:
                if response.status == 200:
                    models = await response.json()
                    print(f"\n✅ Found {len(models)} model(s):\n")
                    for i, model in enumerate(models, 1):
                        print(f"  {i}. {model.get('title', 'Unknown')}")
                    return models
                else:
                    print(f"❌ Failed to get models (status: {response.status})")
                    return []
    except Exception as e:
        print(f"❌ Error: {e}")
        return []


async def test_sd_samplers():
    """List available samplers"""
    
    url = "http://localhost:7860/sdapi/v1/samplers"
    
    print("\n" + "=" * 60)
    print("🎲 AVAILABLE SAMPLERS")
    print("=" * 60)
    
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(url) as response:
                if response.status == 200:
                    samplers = await response.json()
                    print(f"\n✅ Found {len(samplers)} sampler(s):\n")
                    for i, sampler in enumerate(samplers[:10], 1):  # Show first 10
                        print(f"  {i}. {sampler.get('name', 'Unknown')}")
                    if len(samplers) > 10:
                        print(f"  ... and {len(samplers) - 10} more")
                    return samplers
                else:
                    print(f"❌ Failed to get samplers (status: {response.status})")
                    return []
    except Exception as e:
        print(f"❌ Error: {e}")
        return []


async def main():
    """Run all tests"""
    
    print("\n" + "🌅" * 30)
    print("AURORA ARCHIVE - STABLE DIFFUSION TEST")
    print("🌅" * 30 + "\n")
    
    # Test 1: Check available models
    models = await test_sd_models()
    
    # Test 2: Check available samplers
    samplers = await test_sd_samplers()
    
    # Test 3: Generate a test image
    result = await test_sd_endpoint()
    
    # Summary
    print("\n" + "=" * 60)
    print("📊 TEST SUMMARY")
    print("=" * 60)
    print(f"Models available: {'✅' if models else '❌'} ({len(models)} found)")
    print(f"Samplers available: {'✅' if samplers else '❌'} ({len(samplers)} found)")
    print(f"Image generation: {'✅' if result.get('success') else '❌'}")
    
    if result.get('success'):
        print(f"\n🎉 All tests passed!")
        print(f"📁 Test image: {result['path']}")
        print(f"⏱️  Generation time: {result['duration']:.2f}s")
    else:
        print(f"\n⚠️  Image generation failed: {result.get('error', 'Unknown error')}")
    
    print("\n" + "=" * 60 + "\n")


if __name__ == '__main__':
    asyncio.run(main())
