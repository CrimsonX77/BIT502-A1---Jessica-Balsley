# 📦 Aurora Archive - GitHub Upload Checklist

## ✅ CORE FILES TO UPLOAD

### 🎯 Main Application Files
```
aurora_pyqt6_main.py          # Main GUI application (4100+ lines) ⭐
card_generation.py            # Image generation engine
card_scanner.py               # Steganography scanner
api_config_manager.py         # API key management
steganography_module.py       # Data embedding
mutable_steganography.py      # Editable steg data
```

### 📄 Configuration Templates
```
.env.example                  # Create this! (see below)
sd_config.env.example         # Create this! (see below)
requirements.txt              # Python dependencies
```

### 🚀 Startup Scripts
```
start_aurora.sh               # Linux/Mac launcher
README.md                     # Main documentation ⭐
```

### 📚 Documentation (markdowns/)
```
API_CONFIGURATION_GUIDE.md    # API setup guide
AURORA_VIDEO_UPLOAD.md        # Video feature docs
GRACEFUL_SHUTDOWN.md          # Shutdown system docs
CUSTOM_SETTINGS_GUIDE.md      # User customization
DYNAMIC_MODELS.md             # Model management
ADVANCED_SD_CONFIG.md         # SD configuration
```

### 🎨 Assets
```
Assets/                       # UI icons, images
inspiration/                  # Design inspiration (optional)
refinedinspo/                # Pipeline docs
```

### 📊 Schema & Structure
```
refinedinspo/member_schema.json    # Data structure
refinedinspo/card_pipeline.py      # Pipeline logic
refinedinspo/config.py             # Config helpers
refinedinspo/payments.py           # Payment logic
refinedinspo/rentals.py            # Rental system
refinedinspo/tiers.py              # Tier management
```

---

## ❌ DO NOT UPLOAD (Handled by .gitignore)

### 🔐 CRITICAL - NEVER COMMIT THESE:
```
.env                          # Real API keys! ⚠️
sd_config.env                 # Real Grok API key! ⚠️
config/api_config.enc         # Encrypted keys
config/.key                   # Encryption key
*.pem, *.key                  # SSL certificates
```

### 💾 Too Large / Generated:
```
*.safetensors                 # SD models (GB-sized!)
*.ckpt, *.pt                  # AI model files
venv/                         # Virtual environment
SD15/                         # Stable Diffusion installation
generated_cards/              # Generated images
output/                       # Output files
videos/                       # Uploaded videos
*.db, *.sqlite                # Database files
__pycache__/                  # Python cache
logs/                         # Log files
```

---

## 🛠️ FILES YOU NEED TO CREATE

### 1. `.env.example` (Template for users)
Create this file with fake/placeholder values:

```env
# Aurora Archive - Environment Configuration Template
# Copy this to .env and fill in your real values

# ===== API KEYS (REQUIRED) =====
# Get your Grok API key from: https://x.ai/api
GROK_API_KEY=xai-YOUR_KEY_HERE_REPLACE_THIS
XAI_API_KEY=xai-YOUR_KEY_HERE_REPLACE_THIS

# Stripe (if using payment features)
STRIPE_SECRET_KEY=sk_test_YOUR_STRIPE_KEY_HERE

# ===== DATABASE (OPTIONAL) =====
DATABASE_URL=postgresql://localhost/aurora
VECTOR_DB_URL=http://localhost:6333

# ===== IMAGE GENERATION =====
GROK_BASE_URL=https://api.x.ai/v1
STABLE_DIFFUSION_URL=http://localhost:7860
DEFAULT_BACKEND=grok
GENERATION_LOG_PATH=./logs/generations.log

# ===== BACKEND SELECTION =====
PREFERRED_BACKEND=grok
ENABLE_FALLBACK=true

# ===== STABLE DIFFUSION SETTINGS =====
SD_MODEL_CHECKPOINT=AetherCrown.safetensors
SAMPLER_NAME=Euler A Automatic
SAMPLING_STEPS=20
CLIP_SKIP=2

# ===== HIGH-RES FIX =====
ENABLE_HIRES_FIX=False
HR_UPSCALER=R-ESRGAN 4x+ Anime6B
HR_STEPS=20
DENOISING_STRENGTH=0.4
HR_SCALE=2.0

# ===== TIER SETTINGS =====
KIDS_STEPS=20
STANDARD_STEPS=20
PREMIUM_STEPS=20
```

### 2. `sd_config.env.example`
Create this template:

```env
# Stable Diffusion Configuration Template
# Copy to sd_config.env and customize

# ===== GROK API =====
GROK_API_KEY=xai-YOUR_KEY_HERE
GROK_BASE_URL=https://api.x.ai/v1

# ===== STABLE DIFFUSION =====
STABLE_DIFFUSION_URL=http://localhost:7860

# ===== MODEL SETTINGS =====
SD_MODEL_CHECKPOINT=AetherCrown.safetensors
SD_MODEL_FALLBACK=Sable_room.safetensors

# ===== SAMPLING =====
SAMPLER_NAME=Euler A Automatic
sampling_steps=20
CFG_SCALE=7.0

# ===== HIGH-RES FIX =====
ENABLE_HIRES_FIX=false
HR_UPSCALER=R-ESRGAN 4x+ Anime6B
HR_STEPS=20
DENOISING_STRENGTH=0.4
HR_SCALE=2.0

# ===== TIER CONFIGURATION =====
KIDS_DAILY_LIMIT=3
STANDARD_DAILY_LIMIT=10
PREMIUM_DAILY_LIMIT=999
```

### 3. Update `README.md`
Make sure your README has:
- **Installation instructions**
- **Model setup guide** (where to get AetherCrown/Sable_room)
- **API key setup** (point to .env.example)
- **Quick start guide**
- **Features list**
- **Screenshots/demo** (optional but recommended!)

---

## 📋 PRE-UPLOAD CHECKLIST

### Security Audit:
- [ ] No real API keys in any committed files
- [ ] `.env` and `sd_config.env` in `.gitignore`
- [ ] Created `.env.example` with placeholders
- [ ] Removed any personal paths (e.g., `/home/crimson/...`)
- [ ] No database credentials
- [ ] No email/personal info in comments

### File Cleanup:
- [ ] Removed `*.pyc` and `__pycache__`
- [ ] Deleted any `.db` or `.sqlite` files
- [ ] Cleared `logs/` directory
- [ ] Removed generated images from repo
- [ ] Cleaned up any test files

### Documentation:
- [ ] `README.md` is complete and clear
- [ ] `requirements.txt` is up to date
- [ ] All markdown docs are reviewed
- [ ] Added license file (LICENSE.md)
- [ ] Added contribution guidelines (optional)

### Code Quality:
- [ ] Removed debug `print()` statements (or kept intentional ones)
- [ ] Removed commented-out code blocks
- [ ] Updated hardcoded paths to be relative
- [ ] Tested that it runs on a fresh clone

---

## 🚀 UPLOAD COMMAND SEQUENCE

```bash
# 1. Initialize git (if not done)
cd /home/crimson/Desktop/Authunder
git init

# 2. Add all core files
git add .gitignore
git add *.py
git add requirements.txt
git add start_aurora.sh
git add README.md
git add .env.example
git add sd_config.env.example
git add markdowns/
git add Assets/
git add refinedinspo/

# 3. Check what's staged (make sure no secrets!)
git status

# 4. Commit
git commit -m "Initial commit: Aurora Archive v2.0 - Card Generation System"

# 5. Add remote (replace with your repo URL)
git remote add origin https://github.com/YourUsername/aurora-archive.git

# 6. Push
git push -u origin main
```

---

## 🎯 RECOMMENDED REPO STRUCTURE

```
aurora-archive/
├── .gitignore                    ⭐ Critical!
├── README.md                     ⭐ Main docs
├── requirements.txt              ⭐ Dependencies
├── LICENSE.md                    ⭐ Choose a license
├── .env.example                  ⭐ Template
├── sd_config.env.example         ⭐ Template
├── start_aurora.sh               Launcher
│
├── aurora_pyqt6_main.py          Main app
├── card_generation.py            Core logic
├── card_scanner.py               Scanner
├── api_config_manager.py         API management
├── steganography_module.py       Steg
├── mutable_steganography.py      Editable steg
│
├── Assets/                       UI resources
├── markdowns/                    Documentation
│   ├── API_CONFIGURATION_GUIDE.md
│   ├── AURORA_VIDEO_UPLOAD.md
│   ├── CUSTOM_SETTINGS_GUIDE.md
│   └── ...
│
├── refinedinspo/                 Pipeline & schemas
│   ├── member_schema.json
│   ├── card_pipeline.py
│   ├── config.py
│   └── ...
│
├── cards/.gitkeep                Empty dir for cards
├── output/.gitkeep               Empty dir for output
└── logs/.gitkeep                 Empty dir for logs
```

---

## 💡 BONUS TIPS

### Add a Beautiful README Badge:
```markdown
![Python](https://img.shields.io/badge/python-3.10+-blue.svg)
![PyQt6](https://img.shields.io/badge/PyQt6-6.0+-green.svg)
![License](https://img.shields.io/badge/license-MIT-purple.svg)
```

### Add Screenshots:
Create a `screenshots/` folder and add:
- Main UI screenshot
- Card generation example
- API settings tab
- Video upload feature

### Consider Adding:
- `CHANGELOG.md` - Version history
- `CONTRIBUTING.md` - How others can contribute
- `LICENSE.md` - MIT, GPL, or your choice
- `CODE_OF_CONDUCT.md` - Community guidelines

---

## ⚠️ FINAL SECURITY CHECK

Before pushing, run these commands:

```bash
# Check for any accidentally added secrets
git log --all --full-history --source -- '**/.env'
git log --all --full-history --source -- '**/config/api_config.enc'

# Search for API keys in committed files
git grep -i "xai-" 
git grep -i "sk_test"
git grep -i "sk_live"

# If you find any, IMMEDIATELY:
git reset --hard HEAD~1  # Undo last commit
# Or use git filter-branch to remove from history
```

---

## 🎉 YOU'RE READY!

Once you've:
1. ✅ Created `.env.example` and `sd_config.env.example`
2. ✅ Verified `.gitignore` is working
3. ✅ Removed all secrets/keys
4. ✅ Updated README.md
5. ✅ Run the security checks

You can safely push to GitHub! 🚀

---

**Remember**: The world gets to see your beautiful code, but your API keys stay safely on your machine~ 💜✨

*Generated for Aurora Archive - World Tease Release Prep* 🐉
