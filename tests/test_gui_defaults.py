#!/usr/bin/env python3
"""
Test Aurora GUI default settings
Verifies: Euler a sampler, automatic scheduler, 20 steps, 7.0 CFG
"""

import sys
from PyQt6.QtWidgets import QApplication
from aurora_pyqt6_main import AuroraMainWindow

def test_defaults():
    """Test that default settings are correct"""
    print("🧪 Testing Aurora GUI Default Settings")
    print("=" * 60)
    
    # Create application
    app = QApplication(sys.argv)
    window = AuroraMainWindow()
    
    # Access the dropdowns (they're created in create_card_creator)
    # Force tab creation by accessing it
    tabs = window.findChildren(QApplication.QTabWidget)
    if tabs:
        tabs[0].setCurrentIndex(3)  # Switch to Create Card tab
    
    # Check defaults
    print("\n📋 Checking Default Values:")
    print("-" * 60)
    
    # Steps
    steps = window.steps_combo.currentText()
    steps_ok = steps == '20'
    print(f"  Steps: {steps} {'✅' if steps_ok else '❌ (expected 20)'}")
    
    # CFG
    cfg = window.cfg_combo.currentText()
    cfg_ok = cfg == '7.0'
    print(f"  CFG Scale: {cfg} {'✅' if cfg_ok else '❌ (expected 7.0)'}")
    
    # Sampler
    sampler = window.sampler_combo.currentText()
    sampler_ok = 'Euler a' in sampler or sampler == 'Euler a'
    print(f"  Sampler: {sampler} {'✅' if sampler_ok else '⚠️ (expected Euler a)'}")
    
    # Scheduler
    scheduler = window.scheduler_combo.currentText()
    scheduler_ok = scheduler == 'automatic'
    print(f"  Scheduler: {scheduler} {'✅' if scheduler_ok else '⚠️ (expected automatic)'}")
    
    # Width/Height
    width = window.width_combo.currentText()
    height = window.height_combo.currentText()
    print(f"  Dimensions: {width}x{height} {'✅' if width == '512' and height == '768' else '⚠️'}")
    
    # Hi-Res Fix
    hires = window.hires_checkbox.isChecked()
    print(f"  Hi-Res Fix: {'Enabled' if hires else 'Disabled'} {'✅' if not hires else '⚠️ (should be off)'}")
    
    # Summary
    print("\n" + "=" * 60)
    all_ok = steps_ok and cfg_ok and sampler_ok and scheduler_ok
    if all_ok:
        print("✅ ALL DEFAULTS CORRECT!")
        print("\n🎨 Ready to generate with:")
        print(f"   • Euler a sampler")
        print(f"   • automatic scheduler")
        print(f"   • 20 sampling steps")
        print(f"   • 7.0 CFG scale")
        print(f"   • 512x768 resolution")
    else:
        print("⚠️  Some defaults need attention")
    
    print("=" * 60)
    
    return all_ok

if __name__ == '__main__':
    try:
        success = test_defaults()
        sys.exit(0 if success else 1)
    except Exception as e:
        print(f"\n❌ Error during test: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
