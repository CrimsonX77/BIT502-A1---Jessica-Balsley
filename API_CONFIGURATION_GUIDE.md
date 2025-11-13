# Aurora API Configuration System

## Overview
Secure API key management with encrypted storage, auto-connect, and connection testing.

## Features

### ✨ Key Features
- **Encrypted Storage**: API keys encrypted with machine-specific encryption
- **Multiple Backends**: Support for Grok AI, Stable Diffusion, OpenAI, Stability AI, Midjourney
- **Auto-Connect**: Automatically reconnect to verified APIs on startup
- **Connection Testing**: Test API connections before saving
- **Secure Display**: Password-masked API keys with show/hide toggle
- **Export to .env**: Automatically updates .env file with API configurations

### 🔒 Security
- Keys encrypted using Fernet symmetric encryption
- Machine-specific encryption key derived from system ID
- File permissions restricted to owner only (Unix)
- Keys stored in `config/api_config.enc`
- Encryption key stored in `config/.key`

## Supported APIs

### 1. **Grok AI (xAI)**
- **Purpose**: Primary AI generation backend
- **URL**: https://api.x.ai/v1
- **Requires**: API Key
- **Features**: Still images, short videos (3-5s), animated GIFs

### 2. **Stable Diffusion WebUI**
- **Purpose**: Local generation fallback
- **URL**: http://localhost:7860
- **Requires**: No API key (local)
- **Features**: Full SD generation capabilities

### 3. **OpenAI DALL-E**
- **Purpose**: Alternative cloud generation
- **URL**: https://api.openai.com/v1
- **Requires**: API Key
- **Features**: Image generation

### 4. **Stability AI**
- **Purpose**: Professional-grade generation
- **URL**: https://api.stability.ai
- **Requires**: API Key
- **Features**: High-quality images

### 5. **Midjourney API**
- **Purpose**: Artistic generation
- **URL**: https://api.midjourney.com
- **Requires**: API Key
- **Features**: Midjourney-style artwork

## Usage Guide

### Adding an API

1. **Navigate to API Settings**
   - Open Aurora Archive
   - Click "⚙️ API Settings" tab

2. **Configure API**
   - Find the API section (e.g., "🔌 Grok AI (xAI)")
   - Enter the API URL (or use default)
   - Enter your API Key (if required)
   - Check "Auto-connect on startup" (optional)

3. **Test Connection**
   - Click "🔍 Test Connection"
   - Wait for verification
   - Green ✅ status = successful connection

4. **Save Configuration**
   - Click "💾 Save"
   - Configuration is encrypted and stored
   - API key exported to `.env` file

### Managing APIs

#### View Status
- **✅ Connected**: API verified and working
- **⚠️ Not Verified**: Saved but not tested
- **⭕ Not Configured**: No configuration saved

#### Auto-Connect
- Check "Auto-connect on startup" before saving
- Aurora will automatically load this API on launch
- Console output: `🔌 Auto-connecting to N API(s)...`

#### Remove API
- Click "🗑️ Remove" button
- Confirm deletion
- Configuration and auto-connect removed

### Using APIs in Generation

When generating cards:
1. Select backend via "Use Grok AI..." checkbox
2. Aurora uses configured API credentials
3. Backend indicator shows current API
4. Progress dialog displays generation backend

## Configuration Files

### `config/api_config.enc`
Encrypted JSON containing:
```json
{
  "apis": {
    "grok": {
      "url": "https://api.x.ai/v1",
      "api_key": "xai-...",
      "verified": true,
      "last_used": 1699876543.123,
      "added_at": "..."
    }
  },
  "last_used": "grok",
  "auto_connect": ["grok", "stable_diffusion"]
}
```

### `config/.key`
Binary encryption key (auto-generated)
- Derived from machine ID
- Used for Fernet encryption
- Permissions: 0600 (owner read/write only)

### `.env` (auto-updated)
Plain-text environment variables:
```bash
GROK_API_KEY=xai-...
GROK_BASE_URL=https://api.x.ai/v1
STABLE_DIFFUSION_URL=http://localhost:7860
OPENAI_API_KEY=sk-...
OPENAI_BASE_URL=https://api.openai.com/v1
```

## API Configuration Class

### `APIConfigManager` Methods

```python
# Initialize
manager = APIConfigManager(config_dir='config')

# Add/Update API
manager.add_api('grok', 'https://api.x.ai/v1', 'xai-...')

# Get configuration
config = manager.get_api('grok')
# Returns: {'url': '...', 'api_key': '...', 'verified': bool, ...}

# Mark as verified
manager.mark_verified('grok', True)

# Set auto-connect
manager.set_auto_connect('grok', True)

# Get auto-connect list
apis = manager.get_auto_connect_apis()
# Returns: ['grok', 'stable_diffusion']

# Export to .env
manager.export_to_env('grok', '.env')

# Remove API
manager.remove_api('grok')
```

## Testing APIs

### Manual Test
1. Open API Settings tab
2. Enter URL and API key
3. Click "🔍 Test Connection"
4. Check response:
   - Success: ✅ "Connection Successful"
   - Failure: ⚠️ Error message with details

### Test Endpoints

Each API has a test endpoint:
- **Grok**: `/models`
- **Stable Diffusion**: `/sdapi/v1/sd-models`
- **OpenAI**: `/models`
- **Stability**: `/v1/engines/list`
- **Midjourney**: `/info`

### Connection Errors

**Timeout**
- Check URL is correct
- Verify service is running
- Test network connection

**401 Unauthorized**
- API key invalid or expired
- Check key format (bearer token, etc.)

**404 Not Found**
- URL incorrect
- Test endpoint may have changed

## Encryption Details

### Key Derivation
```python
# Machine ID sources (in order):
1. /etc/machine-id
2. /var/lib/dbus/machine-id
3. User home directory path

# Key generation:
PBKDF2(
    algorithm=SHA256,
    length=32 bytes,
    salt=b'crimson_collective_aurora',
    iterations=100,000
)
```

### Encryption Algorithm
- **Cipher**: Fernet (symmetric encryption)
- **Key Size**: 32 bytes (256 bits)
- **Encoding**: Base64 URL-safe

## Backend Integration

### Card Generation with Configured APIs

```python
# In start_generation():
if self.use_grok_checkbox.isChecked():
    backend = 'grok'
    # Uses api_manager.get_api('grok') credentials
else:
    backend = 'stable_diffusion'
    # Uses api_manager.get_api('stable_diffusion') URL

# CardGenerator receives backend configuration
generator = CardGenerator(
    backend=backend,
    tier=tier,
    user_id=user_id
)

# API credentials loaded from encrypted config
```

### Fallback Logic
1. Try primary backend (e.g., Grok)
2. If fails, fallback to Stable Diffusion
3. Use last successful backend
4. Console logs show backend switches

## Troubleshooting

### API Not Showing in Dropdown
- Restart Aurora
- Check API_CONFIG_AVAILABLE = True
- Verify api_config_manager.py imported

### Connection Test Fails
1. Verify URL format (include http:// or https://)
2. Check API key is correct
3. Test with curl:
   ```bash
   curl -H "Authorization: Bearer YOUR_KEY" https://api.x.ai/v1/models
   ```

### Keys Not Persisting
- Check file permissions on `config/` directory
- Verify `config/api_config.enc` created
- Check console for encryption errors

### Auto-Connect Not Working
1. Verify "Auto-connect" was checked when saving
2. Check `api_manager.get_auto_connect_apis()` includes API
3. Look for console message on startup:
   ```
   🔌 Auto-connecting to 2 API(s)...
     ✓ Connected to Grok AI (xAI)
   ```

## Best Practices

### Security
- ✅ Never commit `config/.key` or `config/api_config.enc` to git
- ✅ Add to `.gitignore`:
  ```
  config/.key
  config/api_config.enc
  ```
- ✅ Regularly rotate API keys
- ✅ Use read-only API keys when possible

### Workflow
1. Configure all APIs first
2. Test each connection
3. Enable auto-connect for primary APIs
4. Save configurations before testing generation
5. Monitor console for connection messages

### Multi-Machine Setup
- Encryption keys are machine-specific
- Export APIs to `.env` for portability
- Reconfigure on new machines
- Backup `.env` (not encrypted config)

## Console Output

### Successful Startup
```
🔌 Auto-connecting to 2 API(s)...
  ✓ Connected to Grok AI (xAI)
    (Using saved credentials)
  ✓ Connected to Stable Diffusion WebUI
    (Using saved credentials)
```

### Generation
```
Backend: Grok AI
Initializing Grok AI...
Generating with grok...
Complete!
```

## Future Enhancements

### Planned Features
- [ ] API usage tracking (calls/day)
- [ ] Cost estimation per generation
- [ ] Multi-account support per API
- [ ] Backup/restore configurations
- [ ] API health monitoring dashboard
- [ ] Webhook notifications
- [ ] Rate limit tracking
- [ ] API response caching

## Support

For issues or questions:
1. Check console output for errors
2. Verify API credentials in web dashboard
3. Test API with curl/Postman
4. Check `logs/card_generation.log`
5. Review `config/api_config.enc` permissions
