# 🔮 CRIMSON COLLECTIVE - Integration Guide

## System Overview

The Crimson Collective authentication system consists of multiple layers working in harmony:

```
┌─────────────────────────────────────────────────────────┐
│                 CRIMSON COLLECTIVE                      │
│                  Master Launcher                        │
└──────────────┬──────────────────────────┬───────────────┘
               │                          │
        ┌──────▼──────┐          ┌───────▼────────┐
        │  LAYER 1    │          │    LAYER 2     │
        │  Obelisk    │─────────▶│    Archive     │
        │  Customs    │◀─────────│    Sanctum     │
        └─────────────┘          └────────────────┘
        Card Validation          Member Portal
        Instant Purge            Graceful Logout
```

---

## Component Files

### Core System
- **collective_launcher.py** - Master orchestrator
- **obelisk_customs.py** - Layer 1 authentication (598 lines)
- **archive_sanctum.py** - Layer 2 member portal (1,153 lines)
- **steganography_module.py** - Card encoding/decoding

### Documentation
- **OBELISK_LAYER.md** - Layer 1 details
- **GRACEFUL_SHUTDOWN.md** - Resource cleanup system
- **INTEGRATION_GUIDE.md** - This file

### Support Files
- **aurora_pyqt6_main.py** - Card generator
- **refinedinspo/** - Backend schemas and API designs

---

## Launch Sequence

### 1. Collective Launcher Start
```python
# collective_launcher.py main()
app = QApplication(sys.argv)
launcher = CollectiveLauncher()
launcher.launch_obelisk()
```

### 2. Obelisk Opens
```python
# User sees:
🏛️ OBELISK - Crimson Collective Customs
[Browse Card Button]
[Validation Log]
[Status: Awaiting card submission]
```

### 3. Card Validation
```python
# User drops/selects card
→ CardVerificationWorker starts (background thread)
→ 5-stage verification process:
   1. Extract steganography
   2. Check Crimson seal
   3. Verify seal integrity
   4. Check authenticity
   5. Validate timestamps

# On success:
✅ Append obelisk_verification marker
✅ Enable "Enter Account Realm" button

# On failure:
❌ Instant delete (os.remove, no confirmation)
❌ Show error dialog
```

### 4. Archive Sanctum Opens
```python
# After "Enter Account Realm" clicked
→ Emit card_validated signal
→ Launcher receives signal
→ Launch ArchiveSanctumWindow
→ Pass card_path and card_data

# User sees:
🏛️ THE ARCHIVE SANCTUM
[Soulcard Display] [Quest Menu] [Constellation]
Welcome back, {member_name}
```

### 5. Session Active
```python
# Sanctum features available:
- Constellation dashboard (8 nodes)
- Quest menu (11 items including logout)
- Achievement showcase
- Tier upgrade portal
- Rotating status messages (5s cycle)
```

### 6. Logout & Shutdown
```python
# User clicks "Leave Archive" or X button
→ Show confirmation dialog
→ If confirmed:
   → cleanup_resources() in Sanctum
   → Emit session_ended signal
   → Launcher.on_sanctum_logout()
   → Cascading shutdown:
      1. Close Sanctum (1.5s)
      2. Close Obelisk (0.5s)
      3. Finalize (1.0s)
      4. Quit app (0.5s)

# Total shutdown time: ~3.5 seconds
```

---

## Signal Connections

### Obelisk → Sanctum
```python
# In collective_launcher.py
self.obelisk.card_validated.connect(self.on_card_validated)

# Signal definition (obelisk_customs.py)
card_validated = pyqtSignal(str, dict)  # card_path, card_data

# Emitted when:
self.card_validated.emit(self.current_card_path, self.current_card_data)
```

### Sanctum → Launcher
```python
# In collective_launcher.py
self.sanctum.session_ended.connect(self.on_sanctum_logout)

# Signal definition (archive_sanctum.py)
session_ended = pyqtSignal()

# Emitted when:
self.session_ended.emit()  # During logout
```

---

## Data Flow

### Card Data Structure
```python
card_data = {
    "user_id": "CrimsonMage",
    "tier": "Premium",
    "timeline": {
        "created": "2025-01-15T10:30:00",
        "exported": "2025-01-15T11:45:00"
    },
    "crimson_collective": {
        "sigil": "abc123def456",  # Unique 32-char hex
        "seal": "forged in the Crimson Void...",  # Mythic prose
        "covenant": "authentic",
        "authority": "Crimson Collective Official"
    },
    "obelisk_verification": {  # Added by Obelisk
        "passed": True,
        "verification_sigil": "a7f2d9c4b1e8563a",
        "timestamp": "2025-01-15T12:00:00",
        "gate": 1
    }
}
```

### Steganography Layers
```python
# Original export (from Aurora)
{
    "user_id": "...",
    "tier": "...",
    "crimson_collective": {...},
    "timeline": {...}
}

# After Obelisk validation
{
    ...original data...,
    "obelisk_verification": {
        "passed": True,
        "verification_sigil": "...",
        "timestamp": "...",
        "gate": 1
    }
}

# Could add more layers:
# "archive_sanctum": {...}  - Session data
# "rental_system": {...}    - Active book rentals
# "payment_history": {...}  - Transaction records
```

---

## Resource Management

### Archive Sanctum Resources

#### Timers
```python
self.active_timers = []

# Status rotation timer
self.status_timer = QTimer()
self.status_timer.timeout.connect(self.rotate_status_message)
self.status_timer.start(5000)
self.active_timers.append(self.status_timer)

# Cleanup
def cleanup_timers(self):
    for timer in self.active_timers:
        if timer and timer.isActive():
            timer.stop()
    self.active_timers.clear()
```

#### Dialogs
```python
self.active_dialogs = []

# Tier upgrade dialog
dialog = SubscriptionUpgradeDialog(current_tier, self)
self.active_dialogs.append(dialog)
result = dialog.exec()
self.active_dialogs.remove(dialog)

# Cleanup
def cleanup_dialogs(self):
    for dialog in self.active_dialogs[:]:
        if dialog and dialog.isVisible():
            dialog.close()
    self.active_dialogs.clear()
```

### Obelisk Customs Resources

#### Workers
```python
self.active_workers = []

# Card verification worker
worker = CardVerificationWorker(card_path)
self.active_workers.append(worker)
worker.start()

# Cleanup
def cleanup_workers(self):
    for worker in self.active_workers[:]:
        if worker and worker.isRunning():
            worker.terminate()
            worker.wait(1000)
    self.active_workers.clear()
```

---

## Adding New Features

### New Quest Item in Sanctum
```python
# 1. Add to quests list in create_center_panel()
quests = [
    ...existing quests...,
    ("🎲", "Your New Feature", "Description here", "Normal"),
]

# 2. Connect action in the loop
if "Your New Feature" in title_text:
    quest_item.clicked.connect(self.your_new_method)

# 3. Define method
def your_new_method(self):
    """Handle your new feature"""
    self.status_label.setText("🎲 Opening your feature...")
    # TODO: Implement feature
```

### New Constellation Node
```python
# In ConstellationDashboard.setup_constellation()
nodes = {
    ...existing nodes...,
    "new_node": {
        "name": "Your Node",
        "icon": "🎲",
        "color": "#your_color",
        "description": "Node description"
    }
}

# Connect in ArchiveSanctumWindow.on_constellation_node_clicked()
def on_constellation_node_clicked(self, node_id: str):
    if node_id == "new_node":
        self.your_new_node_handler()
```

### New Background Worker
```python
# Create worker class
class YourWorker(QThread):
    result_ready = pyqtSignal(dict)
    error_occurred = pyqtSignal(str)
    
    def run(self):
        try:
            # Do work
            result = self.do_work()
            self.result_ready.emit(result)
        except Exception as e:
            self.error_occurred.emit(str(e))

# Use in GUI
worker = YourWorker()
self.active_workers.append(worker)
worker.result_ready.connect(self.handle_result)
worker.error_occurred.connect(self.handle_error)
worker.finished.connect(lambda: self.active_workers.remove(worker))
worker.start()
```

---

## Testing

### Manual Test Flow
1. **Launch System**
   ```bash
   source venv/bin/activate
   python collective_launcher.py
   ```

2. **Validate Card**
   - Export a card from Aurora
   - Drop/select in Obelisk
   - Wait for validation
   - Check for obelisk_verification in data

3. **Enter Sanctum**
   - Click "Enter Account Realm"
   - Verify Sanctum opens
   - Check constellation loads
   - Verify quest menu displays

4. **Test Features**
   - Click constellation nodes
   - Open tier upgrade dialog
   - Check status rotation
   - View achievements

5. **Test Logout**
   - Click "Leave Archive"
   - Confirm in dialog
   - Verify graceful shutdown
   - Check console messages
   - Verify clean exit

### Automated Tests (Future)
```python
import pytest
from PyQt6.QtTest import QTest

def test_obelisk_validation():
    obelisk = ObeliskMainWindow()
    # Load test card
    # Verify validation
    # Check signals
    
def test_sanctum_logout():
    sanctum = ArchiveSanctumWindow(test_card, test_data)
    # Trigger logout
    # Verify cleanup
    # Check signals

def test_launcher_cascade():
    launcher = CollectiveLauncher()
    # Launch GUIs
    # Trigger shutdown
    # Verify sequence
```

---

## Styling Guide

### Color Palette
```python
# Primary Colors
CRIMSON_DARK = "#7f1d1d"    # Dark crimson
CRIMSON_MID = "#b91c1c"     # Mid crimson
CRIMSON_BRIGHT = "#dc2626"  # Bright crimson
CRIMSON_LIGHT = "#ef4444"   # Light crimson accent

# Accents
GOLD = "#fbbf24"            # Gold for highlights
ORANGE = "#f59e0b"          # Orange for tier
PURPLE = "#8b5cf6"          # Purple for magic
CYAN = "#06b6d4"            # Cyan for info
GREEN = "#10b981"           # Green for success
PINK = "#ec4899"            # Pink for achievements

# Neutrals
BLACK = "#0a0a0a"           # Background
DARK_GRAY = "#1a1a1a"       # Panels
MID_GRAY = "#3f3f3f"        # Buttons
LIGHT_GRAY = "#666"         # Borders
TEXT_GRAY = "#999"          # Secondary text
WHITE = "#ccc"              # Primary text
```

### Font Sizes
```python
HEADER = 32px               # Main titles
SUBTITLE = 18px             # Section headers
BODY = 14px                 # Standard text
SMALL = 12px                # Descriptions
TINY = 10px                 # Meta info
```

### Spacing
```python
MARGIN = 20px               # Outer margins
PADDING = 20px              # Inner padding
SPACING = 20px              # Between elements
BORDER_RADIUS = 12px        # Rounded corners
BORDER_WIDTH = 2px          # Border thickness
```

---

## Security Considerations

### Card Validation
- ✅ Multi-stage verification
- ✅ Instant purge on failure
- ✅ No second chances
- ✅ Cryptographic sigils
- ✅ Timestamp validation
- ✅ Checksum verification

### Data Handling
- ⚠️ Card data in memory (not persistent)
- ⚠️ No encryption on local files (yet)
- ⚠️ Sigils stored in plain text
- ✅ No sensitive data in variables
- ✅ Cleanup on logout

### Future Security
- 🔮 Encrypt card files at rest
- 🔮 Session tokens with expiry
- 🔮 Two-factor authentication
- 🔮 Rate limiting on validation
- 🔮 Audit logging of access
- 🔮 Remote card revocation

---

## Performance

### Startup Time
- Obelisk: ~1-2 seconds
- Sanctum: ~1-2 seconds
- Total: ~2-4 seconds

### Memory Usage
- Obelisk: ~50-80 MB
- Sanctum: ~80-120 MB
- Total: ~130-200 MB

### Shutdown Time
- Sanctum: ~1.5 seconds
- Obelisk: ~1.6 seconds
- Cascade: ~3.5 seconds
- Total: ~3.5 seconds (overlapped)

---

## Troubleshooting

### "DeprecationWarning: sipPyTypeDict"
- Non-critical PyQt6 warning
- Can be ignored
- Will be fixed in future PyQt6 versions

### GUI doesn't open
- Check venv activated
- Verify PyQt6 installed
- Check Python version (3.8+)
- Look for import errors

### Validation fails for good card
- Check steganography magic header
- Verify crimson_collective present
- Check seal integrity
- Validate export timestamp

### Shutdown hangs
- Check for infinite timer loops
- Verify workers terminate
- Look for blocking operations
- Check signal connections

---

## Roadmap

### Phase 1: Core System ✅
- [x] Steganography integration
- [x] Obelisk Customs GUI
- [x] Archive Sanctum GUI
- [x] Graceful shutdown system
- [x] Master launcher

### Phase 2: Features 🚧
- [ ] Book rental system
- [ ] Generation history
- [ ] Timeline visualization
- [ ] Transaction history
- [ ] Customization studio
- [ ] Settings panel

### Phase 3: Integration 📋
- [ ] Connect to Aurora generator
- [ ] Backend API integration
- [ ] Database persistence
- [ ] Payment processing
- [ ] Email notifications

### Phase 4: Polish ✨
- [ ] Sound effects
- [ ] Animations
- [ ] Themes
- [ ] Keyboard shortcuts
- [ ] Tooltips
- [ ] Help system

---

## Conclusion

The Crimson Collective authentication system provides:

✅ **Security**: Multi-layer validation with instant purge  
✅ **User Experience**: Over-engineered but intuitive  
✅ **Reliability**: Graceful shutdown with resource cleanup  
✅ **Extensibility**: Easy to add new features  
✅ **Style**: Dark crimson aesthetic throughout  

The system is production-ready for the authentication layer. Backend integration and additional features can be added incrementally without disrupting the core flow.

---

**The Crimson Collective awaits. 🔮**
