# Aurora Default Generation Settings

## Current Default Configuration

These are the default settings when you open the **Create Card** tab:

### 🎯 Core Settings (OPTIMIZED FOR QUALITY)

| Setting | Default Value | Description |
|---------|--------------|-------------|
| **Sampler** | `Euler a` | Fast, high-quality ancestral sampler |
| **Scheduler** | `automatic` | Let SD choose optimal noise schedule |
| **Steps** | `20` | Balanced speed vs quality (30-60s generation) |
| **CFG Scale** | `7.0` | Moderate prompt adherence (not too strict) |

### 📐 Image Dimensions

| Setting | Default Value | Notes |
|---------|--------------|-------|
| **Width** | `512 px` | Standard SD resolution |
| **Height** | `768 px` | Portrait aspect ratio (good for cards) |
| **Hi-Res Fix** | `Disabled` | Disable for faster generation |

### 🔍 Hi-Res Fix (When Enabled)

| Setting | Default Value | Description |
|---------|--------------|-------------|
| **Upscaler** | `R-ESRGAN 4x+ Anime6B` | Anime-optimized upscaler |
| **HR Scale** | `2.0x` | Double resolution (512×768 → 1024×1536) |

---

## Why These Defaults?

### ✅ Euler a + automatic
- **Fastest** ancestral sampler
- **Excellent** quality at low step counts
- `automatic` scheduler lets SD optimize noise
- **Best choice** for 20-step generations

### ✅ 20 Steps
- **Fast**: 30-60 seconds per card
- **Good quality**: Sufficient detail for most cards
- **Daily generation quota**: Use efficiently

### ✅ 7.0 CFG
- **Balanced**: Not too strict, not too loose
- Allows SD **creative freedom** while following prompt
- Higher CFG (9-15) = stricter prompt adherence but less variety
- Lower CFG (5-6) = more creative but may ignore prompt

### ✅ 512×768 Portrait
- **Standard SD resolution**
- **Card-friendly** aspect ratio (taller than wide)
- **VRAM efficient**: Works on 6GB+ GPUs
- Enable Hi-Res Fix for larger outputs (2.0x = 1024×1536)

---

## Alternative Presets

### ⚡ Ultra Fast Preview (15s)
```
Sampler: Euler a
Scheduler: automatic
Steps: 10-15
CFG: 5.0-6.0
Resolution: 512×512
Hi-Res Fix: Off
```
**Use for**: Quick concept testing, daily quota conservation

### ⚖️ Balanced Quality (1-2min) - **DEFAULT**
```
Sampler: Euler a
Scheduler: automatic
Steps: 20
CFG: 7.0
Resolution: 512×768
Hi-Res Fix: Off
```
**Use for**: Most cards, daily generations

### 🎨 High Quality (3-5min)
```
Sampler: DPM++ 2M SDE Karras
Scheduler: karras
Steps: 30-40
CFG: 7.5-9.0
Resolution: 512×768
Hi-Res Fix: On (2.0x, R-ESRGAN Anime6B)
```
**Use for**: Special cards, portfolio pieces

### 🖼️ Maximum Detail (5-10min)
```
Sampler: DPM++ 2M SDE Karras
Scheduler: karras
Steps: 40-50
CFG: 8.0-11.0
Resolution: 768×1024
Hi-Res Fix: On (2.0x, R-ESRGAN 4x+)
```
**Use for**: Final showcase cards, printing
**Requires**: 8GB+ VRAM

---

## Tips for Standard Tier

### Daily Generation Quota: 3/day
With **20 steps default**, you can generate **3 quality cards per day** in under 3 minutes total.

### Template Styles
- **Fantasy** (default): Epic, magical, detailed
- **Sci-Fi**: Futuristic, tech, cyberpunk
- **Anime**: Japanese animation style, vibrant
- **Realistic**: Photorealistic, detailed textures

### Color Palettes
- **Crimson & Gold**: Warm, regal, heroic
- **Azure & Silver**: Cool, mystical, ethereal
- **Emerald & Bronze**: Nature, earthy, ancient
- **Violet & White**: Elegant, otherworldly, clean

---

## Upgrading to Premium

Premium tier ($15/mo) unlocks:
- ✨ **Unlimited** daily generations
- 🎨 **Custom prompts** (full creative control)
- ⏱️ **Higher step counts** (60-100 steps)
- 🔍 **Hi-Res Fix** by default (2x-4x upscaling)
- 📐 **Custom dimensions** (up to 2048×2048)
- 💾 **30-second motion cards** (50MB)

---

## Troubleshooting

### "Dropdowns not showing"
- **Refresh models**: Click 🔄 button next to Model dropdown
- **Check SD connection**: SD WebUI must be running on `localhost:7860`
- **Verify API**: Test with `python test_advanced_controls.py`

### "Generation too slow"
- Lower steps: 20 → 15 or even 10 for previews
- Disable Hi-Res Fix
- Reduce CFG: 7.0 → 5.0-6.0
- Use Euler a sampler (fastest)

### "Quality not good enough"
- Increase steps: 20 → 30-40
- Enable Hi-Res Fix (2.0x upscale)
- Try DPM++ 2M SDE Karras sampler
- Increase CFG: 7.0 → 8.0-9.0

### "Out of memory error"
- Lower resolution: 768 → 640 or 512
- Disable Hi-Res Fix
- Close other GPU applications
- Restart SD WebUI

---

## Quick Reference Card

```
╔════════════════════════════════════════╗
║   AURORA DEFAULT SETTINGS (OPTIMAL)    ║
╠════════════════════════════════════════╣
║ Sampler:    Euler a                    ║
║ Scheduler:  automatic                  ║
║ Steps:      20                         ║
║ CFG:        7.0                        ║
║ Size:       512 × 768 (portrait)       ║
║ Hi-Res:     Off (enable for 2x upscale)║
╠════════════════════════════════════════╣
║ ⚡ Generation Time: ~30-60 seconds     ║
║ 💾 File Size: ~2-5 MB                  ║
║ 🎨 Quality: Excellent for daily cards  ║
╚════════════════════════════════════════╝
```

**Last Updated**: November 13, 2025  
**Aurora Version**: 1.0 (PyQt6)
