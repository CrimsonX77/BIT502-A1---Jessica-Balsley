# Steganography Data Viewer - Update Documentation

## Overview
The `SteganographyDataViewer` dialog has been updated to fix text visibility issues and add full editing capabilities with automatic re-encoding.

## Changes Made

### A) Text Visibility Fixed ✅

**Problem:** Half of the text was invisible due to poor color contrast.

**Solution:**
- **Column A (Property)**: Dark purple background (#2d1b4e) with light gray text (#e0e0e0)
- **Column B (Value)**: Dark blue background (#1e1b4b) with white text (#ffffff)
- **Alternating rows**: Semi-transparent purple overlay for better row distinction
- **Selected items**: Bright purple highlight (#9333ea) with white text
- **Headers**: Purple background with white bold text

**Result:** All text is now clearly visible with excellent contrast ratios.

### B) Editable Value Column ✅

**Implementation:**
```python
# Column A (Property) - Read-only
key_item.setFlags(key_item.flags() & ~Qt.ItemFlag.ItemIsEditable)

# Column B (Value) - Editable
value_item.setFlags(value_item.flags() | Qt.ItemFlag.ItemIsEditable)
```

**Features:**
- Column A locked (property names cannot be changed)
- Column B fully editable (values can be modified)
- Real-time change tracking via `itemChanged` signal
- Visual feedback when edits are made

### C) Re-encoding Functionality ✅

**Workflow:**

1. **Extract**: Load embedded data from original image
2. **Flatten**: Convert nested structures to dot-notation (e.g., `subscription.tier`)
3. **Display**: Show in editable table
4. **Edit**: User modifies values in Column B
5. **Track**: Changes detected and save button enabled
6. **Unflatten**: Convert dot-notation back to nested structure
7. **Re-encode**: Embed edited data into new image
8. **Save**: Create timestamped file, preserve original

**Code Flow:**
```python
# Flattening (for display)
{
    "subscription": {"tier": "Premium", "status": "active"}
}
↓
{
    "subscription.tier": "Premium",
    "subscription.status": "active"
}

# Unflattening (for re-encoding)
{
    "subscription.tier": "Premium",
    "subscription.status": "active"
}
↓
{
    "subscription": {"tier": "Premium", "status": "active"}
}
```

## New Features

### 1. Real-time Change Tracking

```python
def on_item_changed(self, item):
    """Track when table items are edited"""
    if item.column() == 1:  # Only track Value column
        self.has_changes = True
        self.save_encode_btn.setEnabled(True)
        # Update info label to yellow warning
```

**Behavior:**
- Info label starts cyan with normal message
- Changes to yellow with warning when edits made
- Changes to green with success after save
- Save button disabled until edits are made

### 2. Smart Data Handling

**Nested Dictionaries:**
```
Input:  {"member": {"name": "John", "email": "john@example.com"}}
Flat:   member.name = "John", member.email = "john@example.com"
Edit:   Change to "Jane", "jane@example.com"
Unflatten: {"member": {"name": "Jane", "email": "jane@example.com"}}
```

**Arrays with Indexes:**
```
Input:  {"rentals": [{"book": "Book1"}, {"book": "Book2"}]}
Flat:   rentals[0].book = "Book1", rentals[1].book = "Book2"
Edit:   Change Book1 to "NewBook"
Unflatten: {"rentals": [{"book": "NewBook"}, {"book": "Book2"}]}
```

### 3. Safe File Operations

**Filename Generation:**
```python
original: member_card_123.png
edited:   member_card_123_edited_20251113_143500.png
```

**Features:**
- Original image never modified
- Timestamp ensures unique filenames
- Both files remain in same directory
- Success dialog shows exact location

## UI Improvements

### Color Scheme
```css
Table Background:       #1e1b4b (deep blue)
Column A Background:    #2d1b4e (dark purple)
Column B Background:    #1e1b4b (dark blue)
Column A Text:          #e0e0e0 (light gray)
Column B Text:          #ffffff (white)
Headers:                #9333ea (bright purple)
Selected Items:         #9333ea (bright purple)
Alternating Rows:       rgba(88, 28, 135, 0.2) (transparent purple)
```

### Button Styling
```css
Save & Re-encode:   Green gradient, disabled until changes
Export to CSV:      Purple, always enabled
Close:              Purple, always enabled
```

## Usage Instructions

### Basic Workflow

1. **Open Viewer**
   - From card scanner: Click "🔍 Scan Card Data"
   - From main app: Select card image and view steganography

2. **View Data**
   - Column A shows property names (read-only)
   - Column B shows values (editable)
   - Scroll through all embedded metadata

3. **Edit Data**
   - Click any cell in Column B
   - Type new value
   - Info label turns yellow: "⚠️ Unsaved changes"
   - "Save & Re-encode" button enables

4. **Save Changes**
   - Click "💾 Save & Re-encode Image"
   - Progress shown (if needed)
   - Success dialog appears with new filename
   - Info label turns green: "✅ Changes saved to new file"

5. **Export (Optional)**
   - Click "📊 Export to CSV"
   - All data (including edits) exported
   - Saved to Desktop with timestamp

### Example Use Cases

**Use Case 1: Update Member Email**
```
1. Open card steganography viewer
2. Find row: "email" | "old@example.com"
3. Edit: "email" | "new@example.com"
4. Click "Save & Re-encode"
5. New card created with updated email
```

**Use Case 2: Change Subscription Tier**
```
1. Open viewer
2. Find: "subscription.tier" | "Standard"
3. Edit: "subscription.tier" | "Premium"
4. Save & Re-encode
5. Card now shows Premium tier
```

**Use Case 3: Update Rental Due Date**
```
1. Open viewer
2. Find: "rentals[0].due_date" | "2025-11-15"
3. Edit: "rentals[0].due_date" | "2025-11-30"
4. Save & Re-encode
5. Extended rental period embedded
```

## Technical Details

### Data Structure Preservation

**Problem:** Flattening loses structure information.

**Solution:** Use dot-notation and array indexes:
```
subscription.tier           → {"subscription": {"tier": ...}}
rentals[0].book_title       → {"rentals": [{"book_title": ...}]}
preferences.notifications[1] → {"preferences": {"notifications": [...]}}
```

### Error Handling

**No Data Found:**
```python
metadata = {
    "Status": "⚠️ No embedded data found",
    "Note": "Card does not contain Aurora embedded metadata"
}
```

**Re-encoding Failed:**
```python
QMessageBox.critical(
    "❌ Re-encoding Failed",
    "Failed to re-encode image:\n{error}\n\n"
    "Make sure mutable_steganography module is available."
)
```

### Dependencies

Required modules:
- `mutable_steganography.MutableCardSteganography`
- `PyQt6.QtWidgets` (QTableWidget, etc.)
- `PyQt6.QtGui.QColor`
- Standard library: `json`, `pathlib`, `datetime`

## API Reference

### Class: SteganographyDataViewer

**Constructor:**
```python
SteganographyDataViewer(image_path: str, parent=None)
```

**Attributes:**
- `image_path`: Current image file path
- `original_data`: Extracted data before any edits
- `has_changes`: Boolean flag for tracking edits
- `table`: QTableWidget displaying data
- `save_encode_btn`: Button to save and re-encode

**Methods:**

```python
def load_steg_data(self, image_path: str) -> None:
    """Load and display steganography data from image"""

def on_item_changed(self, item: QTableWidgetItem) -> None:
    """Track when table items are edited"""

def save_and_reencode(self) -> None:
    """Save edited data and re-encode the image"""

def _flatten_dict(self, data: dict, parent_key: str = '', sep: str = '.') -> dict:
    """Flatten nested dictionary structure"""

def _unflatten_dict(self, flat_data: dict, sep: str = '.') -> dict:
    """Unflatten a flattened dictionary back to nested structure"""

def export_to_csv(self) -> None:
    """Export table data to CSV file"""
```

## Future Enhancements

The following features are planned for a separate versioning app:

1. **Version Tracking**
   - Track edit history
   - Show who made changes and when
   - Compare versions side-by-side

2. **Verification System**
   - Digital signatures for data integrity
   - Checksum validation
   - Tamper detection

3. **Rollback Capability**
   - Restore previous versions
   - Undo/redo functionality
   - Version branching

4. **Audit Trail**
   - Complete change log
   - User attribution
   - Timestamp recording

5. **Batch Operations**
   - Edit multiple cards at once
   - Bulk updates
   - Template-based changes

## Testing Checklist

- [x] Module imports successfully
- [x] SteganographyDataViewer class exists
- [x] All new methods present
- [x] Text visibility fixed (both columns readable)
- [x] Column A read-only
- [x] Column B editable
- [x] Change tracking works
- [x] Save button enables on edit
- [x] Flattening/unflattening preserves structure
- [x] Re-encoding creates new file
- [x] Original file preserved
- [x] Success message displays
- [x] Export to CSV works

## Files Modified

1. **aurora_pyqt6_main.py**
   - `SteganographyDataViewer` class completely rewritten
   - Added `on_item_changed()` method
   - Added `save_and_reencode()` method
   - Added `_unflatten_dict()` method
   - Updated `load_steg_data()` method
   - Fixed table styling for visibility
   - Added real-time change tracking

## Conclusion

The steganography viewer is now fully functional with:
- ✅ Perfect text visibility
- ✅ Editable value column
- ✅ Automatic re-encoding
- ✅ Safe file operations
- ✅ Real-time feedback
- ✅ Smart data handling

The viewer provides a complete workflow for viewing and editing embedded card data while preserving data integrity and file safety.
