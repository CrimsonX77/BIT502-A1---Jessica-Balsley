# Aurora Video Upload Feature 🎬

## Overview
Aurora now supports replacing the generated PNG card image with a user-uploaded MP4 video (under 10MB) for cards that have **genuine RedSeal authentication** (embedded steganography data).

## Key Features

### 1. RedSeal Detection
- **Automatic Detection**: When a card is generated with steganography enabled, Aurora automatically detects the RedSeal
- **Visual Indicator**: Console logs show "✅ RedSeal detected" when present
- **Security**: Video upload is ONLY enabled for RedSealed cards

### 2. Video Upload Button
Located in the sidebar, the "🎬 Upload Video (RedSeal)" button:
- **Disabled** by default until a RedSealed card is generated
- **Enabled** automatically when RedSeal is detected
- **Tooltip** shows current status (RedSeal required/detected)

### 3. Video Requirements
- **Format**: MP4 (*.mp4)
- **Size Limit**: 10 MB maximum
- **Validation**: Automatic size check before loading
- **Error Handling**: Clear error messages if file is too large or invalid

### 4. Video Display
- **Seamless Replacement**: PNG image is hidden, video displays in the same card widget
- **Auto-Loop**: Video plays continuously in loop mode
- **High Quality**: 260x360 resolution maintains card aspect ratio
- **Audio Support**: Videos with audio tracks are fully supported

### 5. Mode Switching
- **Show Image Button**: Appears when video is playing, allows switching back to PNG
- **Double-Click**: Opens video in external player (VLC, mpv, etc.)
- **Graceful Toggle**: Switch between image and video modes without restarting

## Usage Guide

### Step 1: Generate a RedSealed Card
1. Open Aurora Archive
2. Go to **🎨 Card Generation** tab
3. Enter your prompt and settings
4. Click **🎨 Generate Card**
5. Wait for generation to complete
6. Check console for "✅ RedSeal detected" message

### Step 2: Upload Video
1. Once RedSealed card is generated, the **🎬 Upload Video** button enables
2. Click the button
3. Select an MP4 file from your system (must be under 10MB)
4. Aurora validates the file size
5. Video loads and starts playing automatically

### Step 3: Switch Modes
- **View Video**: Video plays in loop mode by default
- **Return to Image**: Click **🖼️ Show Image** button to display PNG again
- **External Player**: Double-click the card to open in system video player

## Technical Details

### Architecture
```
CardWidget
├── current_image_path    # Path to PNG file
├── current_video_path    # Path to MP4 file
├── is_video_mode         # Boolean flag for mode
├── has_red_seal          # RedSeal detection flag
├── media_player          # QMediaPlayer instance
├── video_widget          # QVideoWidget for display
└── audio_output          # QAudioOutput for sound
```

### File Validation
```python
# Check file size
file_size_mb = file_size / (1024 * 1024)
if file_size_mb > 10:
    # Show error, reject upload
```

### RedSeal Detection
```python
# Uses mutable_steganography module
from mutable_steganography import MutableCardSteganography
stego = MutableCardSteganography()
data = stego.extract_data(image_path)

# If data exists, card has RedSeal
has_red_seal = data is not None and len(data) > 0
```

### Video Looping
```python
# Connect to media status changed signal
media_player.mediaStatusChanged.connect(_on_media_status_changed)

def _on_media_status_changed(status):
    if status == QMediaPlayer.MediaStatus.EndOfMedia:
        media_player.setPosition(0)  # Reset to start
        media_player.play()           # Play again
```

## UI Elements

### Buttons
1. **🎬 Upload Video (RedSeal)** - Main upload button
   - Background: Red gradient (crimson to brown)
   - Disabled state: Grayed out
   - Enabled state: Full color with hover effect

2. **🖼️ Show Image** - Switch back to PNG
   - Background: Cyan/teal gradient
   - Only visible when video is playing
   - Hidden when in image mode

### Card Widget States
- **Empty**: Default placeholder text
- **Image Mode**: PNG displayed with double-click to open
- **Video Mode**: MP4 playing in loop with audio

## Error Messages

### No Card Generated
```
"No Card Generated"
"Please generate a card first before uploading a video."
```

### RedSeal Required
```
"RedSeal Required"
"Video upload is only available for cards with genuine RedSeal authentication.
This card does not contain embedded steganography data.
Generate a new card with steganography enabled."
```

### File Too Large
```
"File Too Large"
"Video file is X.XX MB.
Maximum allowed size is 10 MB.
Please compress your video and try again."
```

### Video Load Failed
```
"Video Load Failed"
"Failed to load video: [error details]"
```

## Console Output

### RedSeal Detection
```
✅ RedSeal detected in card_20241113_143022.png - Video upload enabled
```

### Video Load Success
```
✅ Video loaded successfully!
File: my_card_video.mp4
Size: 8.42 MB
```

## Dependencies

### Required Modules
- `PyQt6.QtMultimedia` - Media player functionality
- `PyQt6.QtMultimediaWidgets` - Video widget display
- `mutable_steganography` - RedSeal detection

### Audio Support
- `QAudioOutput` - Handles audio playback from video
- Automatically configured when media player is created

## File System

### Video Storage
- Videos are NOT copied to Aurora's directory
- Original file location is referenced by path
- Moving/deleting the original file will break video playback

### Best Practices
1. Keep videos in a permanent location
2. Use descriptive filenames
3. Compress videos to stay under 10MB limit
4. Test playback before uploading

## Video Compression Tips

### Tools for Compression
1. **ffmpeg** (Linux/Mac/Windows):
   ```bash
   ffmpeg -i input.mp4 -vcodec h264 -acodec aac -b:v 800k output.mp4
   ```

2. **HandBrake** (GUI tool):
   - Web optimized preset
   - Target file size: 10MB
   - Quality: 22-24 RF

3. **Online Tools**:
   - CloudConvert
   - Online-Convert.com
   - Clideo

### Recommended Settings
- **Resolution**: 720p or lower (1280x720)
- **Bitrate**: 800-1000 kbps
- **Frame Rate**: 24-30 fps
- **Codec**: H.264 (MP4)
- **Audio**: AAC, 128 kbps

## Security Features

### RedSeal Verification
- Only cards with embedded steganography data can have videos
- Prevents unauthorized video attachments
- Maintains data integrity

### File Validation
- Extension check (.mp4 only)
- Size limit enforcement (10MB max)
- Error handling for corrupted files

## Troubleshooting

### Button Not Enabling
**Problem**: Video upload button stays disabled after generation
**Solution**: 
- Check console for "RedSeal detected" message
- Ensure `mutable_steganography` module is available
- Regenerate card with steganography enabled

### Video Not Playing
**Problem**: Video loads but doesn't play
**Solution**:
- Check file format (must be MP4)
- Verify codec compatibility (H.264 recommended)
- Try re-encoding video with standard settings

### Video Stuttering
**Problem**: Video playback is choppy
**Solution**:
- Reduce video resolution
- Lower bitrate
- Close other resource-intensive applications

### Audio Not Playing
**Problem**: Video plays but no sound
**Solution**:
- Check system volume
- Verify video file has audio track
- Ensure QAudioOutput is initialized (automatic)

## Future Enhancements

### Planned Features
1. **Thumbnail Preview**: Show video thumbnail before upload
2. **Duration Display**: Show video length in file dialog
3. **Compression Helper**: Built-in video compression tool
4. **Multiple Videos**: Support for video playlists
5. **Embed in Export**: Include video in exported card package
6. **WebM Support**: Add support for WebM format
7. **Video Filters**: Apply effects/filters to uploaded videos

### API Integration
- Grok AI video generation could directly output to card widget
- Seamless transition from generation to display
- No manual upload needed for AI-generated videos

## Performance

### Memory Usage
- Video widget: ~50-100MB RAM (depending on resolution)
- Media player: ~20-50MB RAM
- Total overhead: ~100-150MB for video mode

### Cleanup
- Media player automatically stopped on close
- Resources freed in `cleanup_resources()` method
- No memory leaks detected

## Testing Checklist

### Basic Functionality
- [ ] Generate card without steganography → Video button disabled
- [ ] Generate card with steganography → Video button enabled
- [ ] Upload valid MP4 under 10MB → Success
- [ ] Upload MP4 over 10MB → Error message
- [ ] Upload non-MP4 file → Filtered in dialog
- [ ] Video plays in loop → Continuous playback
- [ ] Double-click video → Opens in external player
- [ ] Switch to image mode → PNG displays correctly
- [ ] Switch back to video → Video resumes playing

### Edge Cases
- [ ] Upload video with no audio track → Visual-only playback
- [ ] Upload very short video (< 1 second) → Loops rapidly
- [ ] Upload corrupted MP4 → Error message
- [ ] Close app while video playing → Graceful cleanup
- [ ] Generate new card while video showing → Replace with new image

## Changelog

### Version 2.0 (November 13, 2025)
- ✨ **New**: Video upload feature for RedSealed cards
- ✨ **New**: QMediaPlayer integration with auto-loop
- ✨ **New**: Mode switching between image and video
- ✨ **New**: Double-click to open in external player
- ✨ **New**: File size validation (10MB limit)
- ✨ **New**: RedSeal detection and button state management
- 🔧 **Fixed**: Event filter for video widget double-click
- 🔧 **Fixed**: Cleanup resources on application close
- 📚 **Docs**: Complete video upload documentation

---

**Built with ❤️ by the Crimson Collective**  
*"Where PNG meets MP4, and steganography meets motion"*
