#!/usr/bin/env python3
"""
🔮 CRIMSON COLLECTIVE - Master Launcher
==========================================

Manages the multi-layer authentication and generation system:
1. Obelisk Customs - Card validation & instant purge
2. Archive Sanctum - Member landing page
3. Aurora Archive - Card generation portal

Features:
- Automatic GUI transitions
- Graceful cascading shutdown
- Resource cleanup management
- Signal-based navigation
"""

import sys
from pathlib import Path
from PyQt6.QtWidgets import QApplication
from PyQt6.QtCore import QObject, pyqtSignal, QTimer
from PyQt6.QtGui import QFont

# Import our GUIs
from obelisk_customs import ObeliskMainWindow
from archive_sanctum import ArchiveSanctumWindow


class CollectiveLauncher(QObject):
    """
    Master controller for the Crimson Collective authentication flow
    
    Manages lifecycle:
    - Launch Obelisk first
    - On validation → Launch Sanctum
    - From Sanctum → Launch Aurora (card generator)
    - On Sanctum logout → Close all
    - Clean shutdown of all resources
    """
    
    shutdown_complete = pyqtSignal()
    
    def __init__(self):
        super().__init__()
        self.obelisk = None
        self.sanctum = None
        self.aurora = None
        self.is_shutting_down = False
    
    def launch_obelisk(self):
        """Launch the Obelisk Customs checkpoint"""
        print("🏛️  Launching Obelisk Customs...")
        
        self.obelisk = ObeliskMainWindow()
        
        # Connect card validation to sanctum launch
        self.obelisk.card_validated.connect(self.on_card_validated)
        
        self.obelisk.show()
        print("✅ Obelisk ready")
    
    def on_card_validated(self, card_path: str, card_data: dict):
        """Handle successful card validation"""
        print("\n🚪 Card validated! Launching Archive Sanctum...")
        
        # Launch Archive Sanctum
        self.sanctum = ArchiveSanctumWindow(card_path, card_data)
        
        # Connect sanctum logout to cleanup
        self.sanctum.session_ended.connect(self.on_sanctum_logout)
        
        self.sanctum.show()
        print("✅ Archive Sanctum opened")
        
        # Optionally hide Obelisk while in Sanctum
        # self.obelisk.hide()
    
    def on_sanctum_logout(self):
        """Handle Archive Sanctum logout"""
        if self.is_shutting_down:
            return
        
        print("\n🌙 Archive Sanctum logout initiated...")
        self.initiate_shutdown()
    
    def initiate_shutdown(self):
        """Gracefully shutdown all GUIs"""
        if self.is_shutting_down:
            return
        
        self.is_shutting_down = True
        print("🔄 Initiating cascading shutdown...")
        
        # Close Aurora first if open
        if self.aurora and not self.aurora.is_shutting_down:
            print("  → Closing Aurora Archive...")
            self.aurora.cleanup_resources()
            QTimer.singleShot(1000, self._close_aurora)
        # Then close Sanctum
        elif self.sanctum and not self.sanctum.is_shutting_down:
            print("  → Closing Archive Sanctum...")
            self.sanctum.cleanup_resources()
            QTimer.singleShot(1500, self._close_sanctum)
        else:
            self._close_obelisk()
    
    def _close_aurora(self):
        """First stage: Close Aurora"""
        if self.aurora:
            self.aurora.close()
            self.aurora = None
        print("  ✅ Aurora Archive closed")
        
        # Now close Sanctum
        if self.sanctum:
            QTimer.singleShot(500, self._close_sanctum_after_aurora)
        else:
            QTimer.singleShot(500, self._close_obelisk)
    
    def _close_sanctum_after_aurora(self):
        """Close Sanctum after Aurora"""
        if self.sanctum and not self.sanctum.is_shutting_down:
            print("  → Closing Archive Sanctum...")
            self.sanctum.cleanup_resources()
            QTimer.singleShot(1500, self._close_sanctum)
        else:
            self._close_sanctum()
    
    def _close_sanctum(self):
        """Second stage: Close sanctum"""
        if self.sanctum:
            self.sanctum.close()
            self.sanctum = None
        print("  ✅ Archive Sanctum closed")
        
        # Now close Obelisk
        QTimer.singleShot(500, self._close_obelisk)
    
    def _close_obelisk(self):
        """Third stage: Close obelisk"""
        if self.obelisk and not self.obelisk.is_shutting_down:
            print("  → Closing Obelisk Customs...")
            self.obelisk.cleanup_resources()
            QTimer.singleShot(1000, self._finalize_shutdown)
        else:
            self._finalize_shutdown()
    
    def _finalize_shutdown(self):
        """Final stage: Complete shutdown"""
        if self.obelisk:
            self.obelisk.close()
            self.obelisk = None
        print("  ✅ Obelisk Customs closed")
        
        print("\n✨ Shutdown complete. The Crimson Collective awaits your return...")
        self.shutdown_complete.emit()
        
        # Exit application
        QTimer.singleShot(500, QApplication.quit)


def main():
    """Entry point for the Crimson Collective"""
    print("═" * 70)
    print("🔮 CRIMSON COLLECTIVE - Authentication System")
    print("═" * 70)
    print()
    
    # Create application
    app = QApplication(sys.argv)
    
    # Set application-wide font
    font = QFont("Segoe UI", 10)
    app.setFont(font)
    
    # Set application metadata
    app.setApplicationName("Crimson Collective")
    app.setOrganizationName("Crimson Collective")
    
    # Create launcher
    launcher = CollectiveLauncher()
    
    # Launch Obelisk (first gate)
    launcher.launch_obelisk()
    
    # Run application
    return app.exec()


if __name__ == '__main__':
    sys.exit(main())
