#!/usr/bin/env python3
"""
Minimal test to see if QComboBox shows in QGridLayout
"""

import sys
from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, 
    QGridLayout, QLabel, QComboBox, QFrame
)

class TestWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Minimal ComboBox Test")
        self.setGeometry(100, 100, 600, 400)
        
        central = QWidget()
        self.setCentralWidget(central)
        layout = QVBoxLayout(central)
        
        # Create frame (like form_frame)
        frame = QFrame()
        frame.setStyleSheet("""
            QFrame {
                background-color: rgba(0, 0, 0, 0.3);
                border: 1px solid rgba(168, 85, 247, 0.3);
                border-radius: 12px;
                padding: 30px;
            }
        """)
        frame_layout = QVBoxLayout(frame)
        
        # Add label
        label = QLabel("⚙️ Test Settings")
        label.setStyleSheet("font-weight: bold; font-size: 14px; color: #c084fc;")
        frame_layout.addWidget(label)
        
        # Add grid
        grid = QGridLayout()
        grid.setSpacing(16)
        
        # Add combos
        for row in range(3):
            for col in range(2):
                lbl = QLabel(f"Setting {row},{col}")
                combo = QComboBox()
                combo.addItems(['Option 1', 'Option 2', 'Option 3'])
                grid.addWidget(lbl, row * 2, col)
                grid.addWidget(combo, row * 2 + 1, col)
        
        frame_layout.addLayout(grid)
        layout.addWidget(frame)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    
    # Dark theme
    app.setStyleSheet("""
        QWidget {
            background-color: #0f172a;
            color: white;
        }
        QComboBox {
            background-color: rgba(0, 0, 0, 0.5);
            border: 1px solid rgba(168, 85, 247, 0.3);
            border-radius: 8px;
            padding: 8px;
            color: white;
        }
    """)
    
    window = TestWindow()
    window.show()
    
    print("✅ Test window shown!")
    print("If you see 6 dropdowns in a 3x2 grid, Qt layout is working.")
    print("If not, there may be a Qt/display issue.")
    
    sys.exit(app.exec())
