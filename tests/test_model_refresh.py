#!/usr/bin/env python3
"""
Test script for dynamic model detection
Tests the get_available_sd_models function
"""

import requests

def get_available_sd_models(sd_url: str = "http://localhost:7860") -> list:
    """
    Fetch available Stable Diffusion models from the SD WebUI API.
    
    Args:
        sd_url: Base URL of the SD WebUI instance
        
    Returns:
        List of model filenames (e.g., ['model1.safetensors', 'model2.ckpt'])
    """
    try:
        print(f"🔍 Connecting to SD API at {sd_url}...")
        response = requests.get(
            f"{sd_url}/sdapi/v1/sd-models",
            timeout=3
        )
        
        if response.status_code == 200:
            models_data = response.json()
            print(f"✅ Successfully connected! Found {len(models_data)} models")
            
            # Extract model titles (filenames)
            models = [model.get('title', model.get('model_name', '')) 
                     for model in models_data]
            
            # Filter out empty strings
            models = [m for m in models if m]
            
            print("\n📦 Available Models:")
            for i, model in enumerate(models, 1):
                print(f"   {i}. {model}")
            
            return models
        else:
            print(f"❌ SD API returned status {response.status_code}")
            return []
            
    except requests.exceptions.ConnectionError:
        print("❌ Cannot connect to Stable Diffusion API")
        print("   Make sure SD WebUI is running with --api flag")
        print(f"   Expected URL: {sd_url}")
        return []
    except requests.exceptions.Timeout:
        print("⏱️  Stable Diffusion API request timed out")
        return []
    except Exception as e:
        print(f"❌ Error fetching SD models: {e}")
        return []


if __name__ == "__main__":
    print("=" * 60)
    print("🧪 Testing Dynamic Model Detection")
    print("=" * 60)
    print()
    
    models = get_available_sd_models()
    
    print()
    print("=" * 60)
    if models:
        print(f"✅ Test PASSED - Found {len(models)} models")
        print("\n💡 Your model dropdown will now show these models!")
    else:
        print("⚠️  No models found")
        print("\n📋 Troubleshooting:")
        print("   1. Start Stable Diffusion WebUI with: python launch.py --api")
        print("   2. Check if it's running at http://localhost:7860")
        print("   3. Place .safetensors/.ckpt models in the models folder")
        print("   4. Restart SD WebUI to detect new models")
    print("=" * 60)
