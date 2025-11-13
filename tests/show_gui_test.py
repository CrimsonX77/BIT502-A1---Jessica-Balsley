#!/usr/bin/env python3
"""
Actually show the Aurora GUI and check if dropdowns are visible
"""

import sys
from PyQt6.QtWidgets import QApplication, QTabWidget
from PyQt6.QtCore import QTimer
from aurora_pyqt6_main import AuroraMainWindow

def check_after_show():
    """Check widgets after window is shown"""
    print("\n🔍 Checking widgets after window is shown...")
    print("=" * 70)
    
    # Switch to Create Card tab
    tabs = window.findChild(QTabWidget)
    if tabs:
        tabs.setCurrentIndex(3)
        print("✅ Switched to Create Card tab (index 3)")
    
    app.processEvents()
    
    widgets = [
        ('steps_combo', 'Steps'),
        ('cfg_combo', 'CFG'),
        ('sampler_combo', 'Sampler'),
        ('scheduler_combo', 'Scheduler'),
        ('width_combo', 'Width'),
        ('height_combo', 'Height'),
    ]
    
    print("\nWidget visibility:")
    for attr, name in widgets:
        if hasattr(window, attr):
            widget = getattr(window, attr)
            visible = widget.isVisible()
            count = widget.count() if hasattr(widget, 'count') else 0
            current = widget.currentText() if hasattr(widget, 'currentText') else 'N/A'
            print(f"  {name:12} | Visible: {visible} | Items: {count:2} | Current: '{current}'")
    
    print("\n" + "=" * 70)
    print("✅ Diagnostics complete!")
    print("\nThe window should be visible now.")
    print("Go to the '🎨 Create Card' tab to see the advanced settings.")
    print("=" * 70)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = AuroraMainWindow()
    
    print("🚀 Launching Aurora GUI...")
    print("Window will open in 1 second...")
    
    # Show the window
    window.show()
    
    # Check widgets after a short delay to allow rendering
    QTimer.singleShot(1000, check_after_show)
    
    sys.exit(app.exec())
