# CSV Export/Import & Image Linking Guide

## 🎯 Overview
Complete CSV export/import system that maintains links to card images and supports re-scanning for up-to-date information. All card generation now uses consistent member_schema structure.

## ✨ New Features

### 1. Card Image Path Tracking
- **Database Enhancement**: Every user record now stores the absolute path to their card image
- **Field Name**: `_card_image_path` (prefixed with _ to appear first in sorted CSV)
- **Automatic**: Path is captured whenever a card is scanned or generated
- **Persistent**: Survives database saves and reloads

### 2. CSV Export with Image Links
- **Export Button**: "📊 Export All to CSV" in Card Scanner Dialog
- **Image Column**: `_card_image_path` column contains full path to each user's card
- **Complete Data**: All member_schema fields flattened and exported
- **Metadata Included**: 
  - `_user_id`: Unique identifier
  - `_card_format`: Format type (aurora_member, aether_soul, etc.)
  - `_card_image_path`: ✨ **NEW** - Absolute path to card image
  - `_first_scan`: When user was first registered
  - `_last_scan`: Last time card was scanned
  - `_scan_count`: Number of times scanned

### 3. CSV Import & Rescan
- **Import Button**: "📥 Import CSV" in Card Scanner Dialog (orange button)
- **Smart Reload**: 
  1. Reads CSV file
  2. Extracts `_card_image_path` from each row
  3. Re-scans the actual card image to get fresh data
  4. Updates database with current embedded data
- **Use Cases**:
  - Reload database after manual edits to card images
  - Sync data from cards shared across systems
  - Recover database from exported CSV
  - Verify data integrity by comparing CSV to embedded data

### 4. Unified Card Generation
- **Member Schema**: All generated cards now embed complete member_schema structure
- **Consistency**: New Member cards and Quick Generate cards use same format
- **Automatic Registration**: Cards auto-register in database with image path
- **Card History**: Generation metadata stored in member's `cards` array
- **Usage Tracking**: `usage_stats` updated with each generation

## 📋 Workflow Examples

### Export All Users to CSV
```
1. Open Card Scanner Dialog (📷 button in sidebar)
2. Click "📊 Export All to CSV"
3. Choose save location (default: Desktop/aurora_users_TIMESTAMP.csv)
4. Done! CSV contains all fields + image paths
```

**CSV Structure**:
```csv
_card_image_path,_card_format,_first_scan,_last_scan,_scan_count,_user_id,card_id,member_id,member_profile.name,member_profile.email,...
/home/user/cards/card_001.png,aurora_member,2025-11-13T08:00:00,2025-11-13T09:00:00,5,m_abc123,aurora_m_abc123_000,m_abc123,John Doe,john@example.com,...
/home/user/cards/card_002.png,aurora_member,2025-11-13T08:30:00,2025-11-13T08:30:00,1,m_def456,aurora_m_def456_000,m_def456,Jane Smith,jane@example.com,...
```

### Import CSV & Rescan Cards
```
1. Open Card Scanner Dialog
2. Click "📥 Import CSV"
3. Browse to exported CSV file
4. System re-scans all card images from _card_image_path column
5. Database updates with fresh data from embedded images
6. Results displayed: Success count, Error count
```

**What Happens During Import**:
- Each row in CSV is processed
- `_card_image_path` column is read
- Card image is located and re-scanned using MutableCardSteganography
- Fresh data is extracted from image
- Database is updated with current embedded data
- Old data is replaced with up-to-date information

### Generate Card with Embedded Data
```
1. Method A - New Member:
   - Click "👤 New Member"
   - Fill registration form
   - Click "✓ Create Member & Generate Card"
   - Confirm card generation
   - Complete member_schema embedded in card

2. Method B - Quick Generate:
   - Click "⚡ Quick Generate" in sidebar
   - Card generated with current member data
   - Member_schema automatically embedded
   - Card registered in database with image path
   - Generation metadata added to member's cards array

3. Method C - Full Creator:
   - Go to "🎨 Card Creator" tab
   - Enter character concept
   - Choose style and color
   - Configure advanced settings (optional)
   - Click "Generate Card"
   - Complete member_schema embedded
   - Card registered automatically
```

## 🔄 Data Flow

### Generation → Embedding → Registration
```
1. Card Generated (Stable Diffusion)
   ↓
2. Member Schema Prepared
   - Uses existing member_data or creates new
   - Adds generation metadata to cards array
   - Updates usage_stats (cards_generated, last_generation_date)
   - Adds audit_trail entry
   ↓
3. Data Embedded (MutableCardSteganography)
   - Original card image used as template
   - Complete member_schema embedded invisibly
   - Saved as *_embedded.png
   ↓
4. Database Registration (CardScanner)
   - Card scanned to verify embedded data
   - User registered/updated in database
   - Image path stored: _card_image_path
   ↓
5. Display Updated
   - Embedded card displayed in main window
   - Ready for export to CSV
```

### Export → Edit → Import → Update
```
1. Export CSV
   - All users + image paths exported
   ↓
2. Edit Cards Externally (Optional)
   - Re-embed data using external tools
   - Modify card images
   - Update embedded information
   ↓
3. Import CSV
   - CSV read for image paths
   - Each card re-scanned from disk
   ↓
4. Database Updated
   - Fresh data from images replaces old data
   - All fields updated from embedded data
   - Image paths verified/updated
```

## 🗂️ Database Structure

### User Record (Enhanced)
```json
{
  "user_id": "m_abc123",
  "data": {
    "card_id": "aurora_m_abc123_000",
    "member_id": "m_abc123",
    "member_profile": {
      "name": "John Doe",
      "email": "john@example.com",
      ...
    },
    "subscription": {...},
    "cards": [
      {
        "card_id": "card_20251113_120000",
        "art_style": "Fantasy",
        "color_scheme": "Azure & Silver",
        "generation_date": "2025-11-13T12:00:00Z",
        "image_path": "/path/to/card.png",
        "metadata": {
          "backend": "stable_diffusion",
          "generation_time": 4.5,
          "resolution": "512x768"
        }
      }
    ],
    "usage_stats": {
      "cards_generated": 5,
      "last_generation_date": "2025-11-13T12:00:00Z"
    },
    ...
  },
  "format": "aurora_member",
  "card_image_path": "/home/user/Authunder/generated_cards/aurora_m_abc123_000_embedded.png",  ← NEW
  "first_scan": "2025-11-13T08:00:00.123456",
  "last_scan": "2025-11-13T12:05:30.654321",
  "scan_count": 5
}
```

## 📊 CSV Column Reference

### Metadata Columns (prefixed with _)
| Column | Description | Example |
|--------|-------------|---------|
| `_user_id` | Unique user identifier | m_abc123 |
| `_card_format` | Card type | aurora_member |
| `_card_image_path` | **Full path to card image** | /home/user/cards/card_001.png |
| `_first_scan` | First registration timestamp | 2025-11-13T08:00:00.123456 |
| `_last_scan` | Most recent scan timestamp | 2025-11-13T12:00:00.654321 |
| `_scan_count` | Number of scans | 5 |

### Member Schema Columns (flattened)
- `card_id`: Card identifier
- `member_id`: Member identifier
- `member_profile.name`: Full name
- `member_profile.email`: Email address
- `member_profile.phone`: Phone number
- `member_profile.gender`: Gender identity
- `member_profile.age`: Age
- `member_profile.bio`: Biography
- `member_profile.location`: City, State/Country
- `member_profile.interests.0`, `.1`, etc.: Individual interests
- `member_profile.membership_tier`: Subscription tier
- `member_profile.address.street`: Street address
- `member_profile.address.city`: City
- `member_profile.address.state`: State/Province
- `member_profile.address.zip`: ZIP/Postal code
- `member_profile.address.country`: Country
- `subscription.tier`: Tier name
- `subscription.monthly_cost`: Monthly cost ($)
- `subscription.billing_cycle`: Billing frequency
- `subscription.next_billing_date`: Next billing date
- `subscription.status`: active/inactive/suspended
- `subscription.auto_renew`: true/false
- `payment_method.type`: Payment type
- `payment_method.last_four`: Last 4 digits
- `payment_method.expiry`: Expiration MM/YY
- `cards.0.card_id`, `.1.card_id`, etc.: Generated card IDs
- `cards.0.art_style`: Art style used
- `cards.0.color_scheme`: Color palette
- `cards.0.generation_date`: When generated
- `cards.0.image_path`: Path to card image
- `usage_stats.cards_generated`: Total cards generated
- `usage_stats.last_generation_date`: Last generation timestamp
- `usage_stats.daily_generations_used`: Today's usage
- `usage_stats.daily_generation_limit`: Daily limit (-1 = unlimited)
- `preferences.card_generation.art_style`: Preferred art style
- `preferences.card_generation.color_scheme`: Preferred colors
- `preferences.notification_settings.*`: Notification preferences
- `preferences.reading_preferences.*`: Reading preferences
- `security.steganographic_hash`: Data integrity hash
- `security.hash_algorithm`: Hash algorithm (SHA-256)
- `security.last_verified`: Last verification timestamp
- `audit_trail.0.action`, `.1.action`, etc.: Audit log actions
- `metadata.created_at`: Account creation timestamp
- `metadata.updated_at`: Last update timestamp
- `metadata.version`: Schema version
- `metadata.schema_type`: Schema type identifier

## 🔧 Technical Details

### Card Image Path Storage
**Location**: `card_scanner.py` → `UserDatabase.add_user()`
```python
def add_user(self, user_data: Dict, card_format: str, card_image_path: str = "") -> str:
    # Stores absolute path to card image
    user_record = {
        "user_id": user_id,
        "data": user_data,
        "format": card_format,
        "card_image_path": card_image_path,  # NEW
        ...
    }
```

**Capture Point**: `card_scanner.py` → `CardScanner.scan_card()`
```python
def scan_card(self, card_image_path: str, register_user: bool = True):
    # Converts to absolute path and stores
    user_id = self.database.add_user(
        raw_data, 
        card_format, 
        str(Path(card_image_path).absolute())
    )
```

### CSV Export Enhancement
**Location**: `aurora_pyqt6_main.py` → `CardScannerDialog.export_all_users_csv()`
```python
# Add card image path to flattened data
flattened['_card_image_path'] = user.get('card_image_path', '')
```

### CSV Import & Rescan
**Location**: `aurora_pyqt6_main.py` → `CardScannerDialog.import_csv_and_reload()`
```python
def import_csv_and_reload(self):
    # 1. Read CSV
    with open(csv_path, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        rows = list(reader)
    
    # 2. Extract image paths and rescan
    for row in rows:
        card_path = row.get('_card_image_path', '').strip()
        if Path(card_path).exists():
            self.scanner.scan_card(card_path, register_user=True)
```

### Unified Card Embedding
**Location**: `aurora_pyqt6_main.py` → `AuroraMainWindow.embed_member_data_in_card()`
```python
def embed_member_data_in_card(self, card_image_path: str, generation_metadata: dict):
    # 1. Build complete member schema
    member_data = self.member_data.copy()
    
    # 2. Add generation info to cards array
    card_entry = {
        "card_id": generation_metadata.get('session_id'),
        "art_style": generation_metadata.get('style'),
        "generation_date": generation_metadata.get('timestamp'),
        "image_path": card_image_path,
        "metadata": {...}
    }
    member_data['cards'].append(card_entry)
    
    # 3. Update usage stats
    member_data['usage_stats']['cards_generated'] = len(member_data['cards'])
    
    # 4. Embed using MutableCardSteganography
    embedded_path = member_manager.create_member_card(
        member_data,
        card_image_path,  # Template
        output_path
    )
    
    return embedded_path
```

## 🚀 Use Cases

### 1. Backup & Recovery
```bash
# Export database to CSV
1. Open Card Scanner → Export All to CSV
2. Save to external drive: /backup/aurora_backup_20251113.csv
3. Store card images: copy generated_cards/ folder

# Restore from CSV
1. Copy card images back to original location
2. Open Card Scanner → Import CSV
3. Select backup CSV file
4. Database rebuilt from card images
```

### 2. Cross-System Sync
```bash
# System A (Generate cards)
1. Generate cards with embedded data
2. Export to CSV
3. Copy CSV + card images to System B

# System B (Import cards)
1. Place card images in accessible location
2. Edit CSV _card_image_path if paths differ
3. Import CSV
4. All cards registered with correct data
```

### 3. Data Verification
```bash
# Check if CSV matches embedded data
1. Export CSV (gets data from database)
2. Import CSV (rescans actual card images)
3. Compare before/after in database
4. Any differences indicate data drift
```

### 4. Bulk Card Update
```bash
# Update all cards with new embedded data
1. Export CSV
2. Use external tool to re-embed updated data in all card images
3. Import CSV
4. Database updates with fresh data from images
```

## 🔒 Data Integrity

### Verification Flow
1. **Generation**: Data embedded during card creation
2. **Export**: CSV captures database state + image paths
3. **Import**: Re-scans verify embedded data matches paths
4. **Checksum**: MutableCardSteganography validates data integrity

### Error Handling
- **Missing Image**: Row skipped, error logged
- **Invalid Path**: Row skipped with warning
- **Corrupt Data**: Card scan fails, original data retained
- **Missing Column**: CSV rejected if no `_card_image_path`

## 📝 Best Practices

### Export
1. **Regular Backups**: Export CSV weekly + backup generated_cards/
2. **Descriptive Names**: Use timestamps in filename
3. **External Storage**: Save to cloud/external drive
4. **Verify Export**: Check CSV has _card_image_path column

### Import
1. **Verify Paths**: Ensure all image paths are accessible
2. **Path Editing**: Update CSV paths if cards moved
3. **Test First**: Try importing one row to verify
4. **Database Backup**: Export before import (safety)

### Card Generation
1. **Let System Embed**: Don't manually edit embedded data
2. **Check Registration**: Verify card appears in "👥 All Users"
3. **Monitor Usage**: Track cards_generated in usage_stats
4. **Audit Trail**: Review audit_trail for generation history

## 🐛 Troubleshooting

### "CSV file does not contain '_card_image_path' column"
**Cause**: CSV not exported from Aurora Archive  
**Fix**: Export CSV using "📊 Export All to CSV" button

### "Image not found at /path/to/card.png"
**Cause**: Card image moved or deleted  
**Fix**: 
1. Locate actual card image
2. Edit CSV to update _card_image_path
3. Re-import CSV

### "Card does not contain valid embedded data"
**Cause**: Image corrupted or data not embedded  
**Fix**:
1. Regenerate card from member data
2. Use "👤 New Member" to create fresh card

### CSV Import Shows Many Errors
**Cause**: Paths invalid or images missing  
**Fix**:
1. Check first error to identify issue
2. Verify card images in expected location
3. Update paths in CSV if cards moved
4. Re-import after correction

### Card Not Appearing After Generation
**Cause**: Registration failed  
**Fix**:
1. Manually scan card: "📷 Scan New Card"
2. Browse to generated_cards/ folder
3. Select *_embedded.png file
4. Verify appears in "👥 All Users"

## ✅ Success Checklist

- [x] Card image paths tracked in database
- [x] CSV export includes _card_image_path column
- [x] Import CSV button available in Card Scanner Dialog
- [x] Import rescans images and updates database
- [x] All card generation embeds complete member_schema
- [x] New Member cards use member_schema
- [x] Quick Generate cards use member_schema
- [x] Card Creator cards use member_schema
- [x] Cards auto-register with image path
- [x] Generation metadata stored in cards array
- [x] Usage stats updated automatically
- [x] Audit trail tracks card generation

## 🎉 Summary

**Created**: Complete CSV export/import system with:
- ✅ Card image path tracking in database
- ✅ CSV export with image links
- ✅ CSV import with automatic rescan
- ✅ Unified card generation using member_schema
- ✅ Automatic registration with image paths
- ✅ Data verification through rescan
- ✅ Cross-system compatibility

**Benefits**:
- 📦 **Portable**: CSV + images = complete backup
- 🔄 **Sync-able**: Share cards across systems
- ✅ **Verified**: Import validates embedded data
- 🎨 **Consistent**: All cards use same schema
- 🔗 **Linked**: Images always connected to data
- 📊 **Trackable**: Full generation history

---

**Created**: 2025-11-13  
**Version**: 1.0.0  
**Status**: ✅ Production Ready
