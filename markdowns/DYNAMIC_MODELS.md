# Dynamic Model Detection - User Guide

## Overview
Aurora now features **dynamic model detection** that automatically discovers available Stable Diffusion models from your SD WebUI installation. No more manual updates needed!

## ✨ New Features

### 🔄 Refresh Button
- **Location**: Next to the Model dropdown in the "⚙️ Advanced Settings" section
- **Icon**: 🔄 (refresh icon)
- **Function**: Click to refresh the model list from SD WebUI
- **Visual Feedback**: 
  - ✓ (checkmark) - Successfully refreshed
  - ⚠ (warning) - Connection failed, using fallback models

### 📡 Automatic Detection
- Models are automatically loaded when you open the "🎨 Create Card" tab
- No need to edit code or config files when you add new models
- Works seamlessly with SD WebUI's model folder

## 🚀 How It Works

### Model Discovery Process
1. **API Connection**: Connects to SD WebUI API at `http://localhost:7860`
2. **Model Query**: Fetches list of models via `/sdapi/v1/sd-models` endpoint
3. **Dropdown Update**: Populates the model dropdown with available models
4. **Selection Persistence**: Remembers your last selected model

### Current Detection Results
Based on your SD WebUI instance, **22 models** were detected:

```
✅ Found Models:
1. abyssorangemix2NSFW_abyssorangemix2Nsfw.safetensors
2. anythingV3_fp16.safetensors
3. bb95FurryMix_v140.safetensors
4. coconutFurryMix2_coconut20Av3.safetensors
5. counterfeitV30_v30.safetensors
6. dreamshaper_8.safetensors
7. fefaHentaiMix_v10.safetensors [eac3a88364]
8. foxyansfw_v4.safetensors
9. furryblend_v10.safetensors
10. hardcoreHentai13_v13Baked.safetensors
11. hassakuHentaiModel_v13.safetensors
12. kda_all_out_kaisa-000034.safetensors
13. meinahentai_v4.safetensors
14. meinamix_meinaV11.safetensors
15. meinapastel_v6Pastel.safetensors
16. neatnessFluffyFurMix_alioth.safetensors
17. nightSkyYOZORAStyle_yozoraV1Origin.safetensors
18. pornmasterAnime_v5.safetensors
19. uberRealisticPornMerge_urpmv13.safetensors
20. v1-5-pruned-emaonly.safetensors [6ce0161689]
21. yiffymix_v37.safetensors
22. yiffymix_v44.safetensors
```

## 📝 Usage Guide

### Adding New Models
1. **Download Model**: Get a `.safetensors` or `.ckpt` model file
2. **Place in Models Folder**: Put it in your SD WebUI's models folder
   - Typical path: `stable-diffusion-webui/models/Stable-diffusion/`
3. **Restart SD WebUI**: Restart the WebUI to detect the new model
4. **Click Refresh**: In Aurora, click the 🔄 button
5. **Select Model**: Your new model now appears in the dropdown!

### Manual Refresh
- **When to use**: After adding new models to SD WebUI
- **How**: Click the 🔄 button next to the model dropdown
- **Result**: Model list updates instantly

### Fallback Mode
If SD WebUI is not running, Aurora uses these fallback models:
- `fefaHentaiMix_v10.safetensors`
- `v1-5-pruned-emaonly.safetensors`
- `YiffMix_v37.safetensors`

## ⚙️ Configuration

### SD WebUI URL
Default: `http://localhost:7860`

To change, update your `.env` file:
```bash
STABLE_DIFFUSION_URL=http://your-custom-url:port
```

### API Requirements
SD WebUI must be started with the `--api` flag:
```bash
python launch.py --api
```

## 🔧 Troubleshooting

### ⚠️ Refresh Button Shows Warning
**Problem**: Cannot connect to SD API

**Solutions**:
1. **Check SD WebUI is Running**:
   ```bash
   # Should see "Running on local URL: http://127.0.0.1:7860"
   ```

2. **Verify API Flag**:
   - SD WebUI must be started with `--api` flag
   - Check your launch command or webui-user.bat/sh

3. **Check Firewall**:
   - Ensure localhost connections are allowed
   - Port 7860 should be accessible

4. **Test Connection**:
   ```bash
   curl http://localhost:7860/sdapi/v1/sd-models
   ```

### 🔄 Models Not Showing After Adding
**Problem**: New model doesn't appear in dropdown

**Solutions**:
1. **Restart SD WebUI**: It only scans models on startup
2. **Check Model Location**: Must be in correct folder
3. **Verify File Format**: Should be `.safetensors` or `.ckpt`
4. **Click Refresh**: After SD WebUI restart, click 🔄

### 💾 Model Selection Not Remembered
**Problem**: Dropdown resets to first model

**Note**: This is expected behavior when refreshing. The system tries to restore your previous selection if the model still exists.

## 🎯 Best Practices

### Model Organization
- **Use descriptive names**: Makes selection easier
- **Keep models up-to-date**: Newer versions often perform better
- **Test before production**: Try new models before important generations

### Performance Tips
- **Larger models = Better quality**: But slower generation
- **SD 1.5 models**: Fastest, good for testing
- **SDXL models**: Higher quality, requires more VRAM
- **Custom models**: Often optimized for specific styles

### Workflow
1. Start with a known-good model (e.g., fefaHentaiMix)
2. Test with default settings (30 steps, 7.5 CFG)
3. Experiment with other models for different styles
4. Use refresh button when switching between projects

## 🌟 Advanced Features

### Model Hash Display
Some models show hash codes (e.g., `[eac3a88364]`):
- Helps verify model authenticity
- Useful when sharing generation settings
- Identifies exact model version

### Selection Persistence
- Last selected model is remembered during session
- Survives refresh button clicks
- Resets when closing Aurora

## 📊 Technical Details

### API Endpoint
```
GET http://localhost:7860/sdapi/v1/sd-models
```

### Response Format
```json
[
  {
    "title": "fefaHentaiMix_v10.safetensors",
    "model_name": "fefaHentaiMix_v10",
    "hash": "eac3a88364",
    "sha256": "...",
    "filename": "/path/to/model.safetensors"
  }
]
```

### Timeout Settings
- **Connection timeout**: 3 seconds
- **Visual feedback**: 1-2 seconds
- **Auto-refresh**: On tab open

## 🎨 UI Elements

### Refresh Button Styling
```css
🔄 - Normal state (ready to refresh)
✓  - Success state (models loaded)
⚠  - Warning state (connection failed)
```

### Tooltip Information
- **Normal**: "Refresh model list from Stable Diffusion"
- **Success**: "Last updated: N models found"
- **Error**: "Could not connect to SD API..."

## 🔮 Future Enhancements

### Planned Features
- [ ] Auto-refresh on model folder change
- [ ] Model preview thumbnails
- [ ] Model metadata display (size, type, VRAM)
- [ ] Favorite models system
- [ ] Model sorting (by name, date, size)
- [ ] Quick model switching keyboard shortcuts

### Community Requests
- Remote SD WebUI support
- Multiple SD instance management
- Model comparison view
- Generation history per model

## 💡 Tips & Tricks

1. **Quick Testing**: Use refresh button to verify SD connection before generation
2. **Model Switching**: Try different models without editing config files
3. **Backup Selections**: Screenshot your favorite model settings
4. **Performance**: Test generation speed with different models
5. **Quality**: Compare output quality across models with same prompt

## 📚 Related Documentation
- `CUSTOM_SETTINGS_GUIDE.md` - Advanced generation settings
- `ADVANCED_SD_CONFIG.md` - Stable Diffusion configuration
- `PYQT6_MIGRATION.md` - PyQt6 framework details

## 🆘 Support

If you encounter issues:
1. Check SD WebUI logs for errors
2. Verify API is enabled (`--api` flag)
3. Test with `test_model_refresh.py` script
4. Check `.env` file for correct SD URL

---

**Last Updated**: November 2025  
**Version**: 1.0  
**Feature Status**: ✅ Production Ready
