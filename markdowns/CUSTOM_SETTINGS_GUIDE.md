# Custom Generation Settings - User Guide

## 🎨 Overview
The Card Creator tab now includes **Advanced Settings** that give you full control over the AI generation process!

## ⚙️ New Controls

### 1. **Model Selection**
- **Options:**
  - `fefaHentaiMix_v10.safetensors` - Anime-optimized model (default)
  - `v1-5-pruned-emaonly.safetensors` - General purpose model
- **What it does:** Different AI models produce different art styles
- **Tip:** fefaHentaiMix is best for anime/manga style cards

### 2. **Sampling Steps** (20-60)
- **Default:** 30 steps
- **Lower (20):** Faster generation, less detail (~2 min)
- **Medium (30-40):** Balanced quality/speed (~2-3 min)
- **Higher (50-60):** Maximum detail, slower (~3-4 min)
- **What it does:** Controls how many iterations the AI uses to refine the image
- **Tip:** 20 steps is usually perfect for most cards

### 3. **CFG Scale** (5.0-15.0)
- **Default:** 7.0
- **Lower (5-7):** More creative, less literal interpretation
- **Medium (7.5-9):** Balanced prompt adherence
- **Higher (11-15):** Strict prompt following, less variation
- **What it does:** Controls how closely the AI follows your prompt
- **Tip:** Use 9-11 for very specific character designs

## 📊 How to Use

1. **Go to the "🎨 Create Card" tab**
2. **Enter your character concept** (e.g., "Sci-Fi space explorer with glowing armor")
3. **Choose style and color palette**
4. **Adjust Advanced Settings:**
   - Pick your preferred model
   - Set steps (higher = better quality but slower)
   - Adjust CFG scale (how strictly to follow prompt)
5. **Click "✨ Generate Card"**
6. **Watch the progress dialog** - it shows which settings are being used!

## 🎯 Recommended Presets

### Fast Preview (Quick Tests)
- Model: v1-5-pruned-emaonly
- Steps: 20
- CFG: 7.0
- Time: ~2 minutes

### Balanced Quality (Standard Use)
- Model: fefaHentaiMix_v10
- Steps: 30
- CFG: 7.5
- Time: ~2-3 minutes

### Maximum Quality (Final Cards)
- Model: fefaHentaiMix_v10
- Steps: 40-50
- CFG: 9.0
- Time: ~3-4 minutes

### Artistic/Creative
- Model: fefaHentaiMix_v10
- Steps: 30
- CFG: 5.0-6.0
- Time: ~2 minutes

## 💡 Pro Tips

1. **Start with defaults** (Model: fefaHentaiMix, Steps: 30, CFG: 7.5)
2. **Experiment with CFG first** - it's the quickest to adjust and has dramatic effects
3. **Use lower steps for testing** prompts, then higher steps for final generation
4. **Different models excel at different styles:**
   - fefaHentaiMix: Anime, manga, fantasy characters
   - v1-5-pruned-emaonly: Realistic, general purpose

## 🔧 Technical Details

- **All settings work with High-Res Fix** - your 512x768 images are automatically upscaled to 1024x1536
- **Settings persist during session** - your last choices are remembered
- **Progress dialog shows active settings** - so you know exactly what's being used
- **No restart required** - changes apply immediately

## 🆘 Troubleshooting

**Generation is too slow:**
- Lower steps to 20-30
- Try the v1-5-pruned-emaonly model (slightly faster)

**Results don't match prompt:**
- Increase CFG scale to 9-11
- Make your prompt more specific
- Ensure you include the style keyword (Fantasy, Sci-Fi, etc.)

**Images look low quality:**
- Increase steps to 40-50
- Keep CFG around 7.5-9.0
- Use fefaHentaiMix model for anime styles

**Want more variety:**
- Lower CFG scale to 5-7
- Try different models
- Keep prompts less specific

## 📝 Example Settings for Common Goals

### Detailed Character Portrait
```
Model: fefaHentaiMix_v10
Steps: 40
CFG: 8.5
Prompt: "Fantasy elven warrior girls, Furry, Lesbians with intricate armor and flowing cape and barely exposed vagina and intimate sex intense,"
```

### Quick Concept Art
```
Model: v1-5-pruned-emaonly
Steps: 20
CFG: 7.0
Prompt: "Sci-Fi space explorer"
```

### Stylized Anime Card
```
Model: fefaHentaiMix_v10
Steps: 30
CFG: 6.0
Prompt: "Anime magical girl with colorful outfit"
```

---

**Enjoy your enhanced creative control! 🎨✨**
