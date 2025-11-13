"""
Aurora Archive - Member Registration Application
Standalone GUI for creating and editing member profiles with test card generation
"""

import sys
import json
from pathlib import Path
from datetime import datetime
from typing import Optional, Dict
from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QPushButton, QLabel, QTabWidget, QFrame, QGridLayout, QTextEdit,
    QComboBox, QLineEdit, QSpinBox, QCheckBox, QScrollArea,
    QMessageBox, QFileDialog, QSplitter
)
from PyQt6.QtCore import Qt, QThread, pyqtSignal
from PyQt6.QtGui import QFont, QPixmap


class TestGenerationWorker(QThread):
    """Background thread for test card generation"""
    
    progress = pyqtSignal(str, int)
    finished = pyqtSignal(dict)
    error = pyqtSignal(str)
    
    def __init__(self, generator, prompt, member_data):
        super().__init__()
        self.generator = generator
        self.prompt = prompt
        self.member_data = member_data
        self._is_cancelled = False
    
    def cancel(self):
        self._is_cancelled = True
    
    def run(self):
        try:
            import asyncio
            
            # Create event loop for this thread
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
            
            # Run the async generation
            result = loop.run_until_complete(
                self.generator.generate_static_card(
                    prompt=self.prompt,
                    style="Fantasy",
                    color_palette="azure_silver",
                    progress_callback=self.on_progress
                )
            )
            
            loop.close()
            
            if self._is_cancelled:
                self.error.emit("Generation cancelled by user")
            elif result.get('success'):
                self.finished.emit(result)
            else:
                self.error.emit(result.get('error', 'Unknown error'))
                
        except Exception as e:
            self.error.emit(f"Generation error: {str(e)}")
    
    def on_progress(self, message: str, percentage: int):
        if not self._is_cancelled:
            self.progress.emit(message, percentage)


class IdentityPreviewPanel(QFrame):
    """Panel for identity description and test generation preview"""
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.current_image_path = None
        self.setup_ui()
    
    def setup_ui(self):
        self.setStyleSheet("""
            QFrame {
                background-color: rgba(0, 0, 0, 0.3);
                border: 1px solid rgba(168, 85, 247, 0.3);
                border-radius: 8px;
                padding: 16px;
            }
        """)
        
        layout = QVBoxLayout(self)
        
        # Header
        header = QLabel("🎨 Identity & Preview")
        header.setStyleSheet("font-size: 16px; font-weight: bold; color: #9333ea;")
        layout.addWidget(header)
        
        # Identity description input
        desc_label = QLabel("Identity Description (for card generation):")
        desc_label.setStyleSheet("color: #c084fc; margin-top: 10px;")
        layout.addWidget(desc_label)
        
        self.identity_input = QTextEdit()
        self.identity_input.setPlaceholderText(
            "Describe the member's visual identity for card generation...\n\n"
            "Example:\n"
            "A mystical warrior with flowing silver hair and piercing blue eyes. "
            "Wears elegant armor with arcane symbols. Surrounded by ethereal energy."
        )
        self.identity_input.setMaximumHeight(150)
        self.identity_input.setStyleSheet("""
            QTextEdit {
                background-color: rgba(0, 0, 0, 0.5);
                border: 1px solid rgba(168, 85, 247, 0.3);
                border-radius: 6px;
                padding: 10px;
                color: white;
                font-size: 13px;
            }
        """)
        layout.addWidget(self.identity_input)
        
        # Test generation button
        test_btn = QPushButton("🔮 Generate Test Preview")
        test_btn.setStyleSheet("""
            QPushButton {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                    stop:0 #7c3aed, stop:1 #2563eb);
                color: white;
                border: none;
                border-radius: 6px;
                padding: 12px;
                font-weight: bold;
                font-size: 14px;
            }
            QPushButton:hover {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                    stop:0 #8b5cf6, stop:1 #3b82f6);
            }
        """)
        test_btn.clicked.connect(self.on_test_generate)
        layout.addWidget(test_btn)
        
        # Preview area
        preview_label = QLabel("Preview:")
        preview_label.setStyleSheet("color: #c084fc; margin-top: 15px;")
        layout.addWidget(preview_label)
        
        self.preview_display = QLabel("No preview generated yet")
        self.preview_display.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.preview_display.setMinimumHeight(400)
        self.preview_display.setStyleSheet("""
            QLabel {
                background-color: rgba(0, 0, 0, 0.5);
                border: 2px dashed rgba(168, 85, 247, 0.3);
                border-radius: 8px;
                color: #a78bfa;
                padding: 20px;
            }
        """)
        self.preview_display.setScaledContents(False)
        layout.addWidget(self.preview_display, stretch=1)
        
        # Status label
        self.status_label = QLabel("")
        self.status_label.setStyleSheet("color: #a78bfa; font-size: 11px; margin-top: 5px;")
        layout.addWidget(self.status_label)
    
    def on_test_generate(self):
        """Handle test generation button"""
        identity = self.identity_input.toPlainText().strip()
        
        if not identity:
            QMessageBox.warning(
                self,
                "No Description",
                "Please enter an identity description first."
            )
            return
        
        # Check if card generator is available
        try:
            from card_generation import CardGenerator
        except ImportError:
            QMessageBox.warning(
                self,
                "Generator Unavailable",
                "Card generator module (card_generation.py) is not available.\n\n"
                "Test generation requires the card generator module."
            )
            self.status_label.setText("❌ Generator not available")
            return
        
        # Get member data from parent window
        parent = self.window()
        if hasattr(parent, 'get_current_member_data'):
            member_data = parent.get_current_member_data()
            
            # Start test generation
            self.status_label.setText("⏳ Generating test preview...")
            
            try:
                # Initialize CardGenerator with proper settings
                # Try Grok first (faster), fallback to SD if Grok fails
                tier = member_data.get('tier', 'Premium')
                user_id = member_data.get('email', 'test_user')
                
                generator = CardGenerator(
                    backend='grok',
                    tier=tier,
                    user_id=user_id
                )
                
                # Create worker thread
                self.worker = TestGenerationWorker(generator, identity, member_data)
                self.worker.progress.connect(self.on_progress)
                self.worker.finished.connect(self.on_generation_complete)
                self.worker.error.connect(self.on_generation_error)
                self.worker.start()
                
            except Exception as e:
                QMessageBox.critical(
                    self,
                    "Generation Error",
                    f"Failed to start generation:\n{str(e)}"
                )
                self.status_label.setText("❌ Failed to start generation")
    
    def on_progress(self, message: str, percentage: int):
        """Update progress status"""
        self.status_label.setText(f"⏳ {message} ({percentage}%)")
    
    def on_generation_complete(self, result: dict):
        """Display generated preview"""
        if result.get("success"):
            # CardGenerator returns 'path' not 'image_path'
            image_path = result.get("path")
            if image_path and Path(image_path).exists():
                self.current_image_path = image_path
                
                # Load and display image
                pixmap = QPixmap(image_path)
                if not pixmap.isNull():
                    scaled = pixmap.scaled(
                        self.preview_display.size(),
                        Qt.AspectRatioMode.KeepAspectRatio,
                        Qt.TransformationMode.SmoothTransformation
                    )
                    self.preview_display.setPixmap(scaled)
                    self.status_label.setText("✓ Preview generated successfully!")
                else:
                    self.status_label.setText("❌ Failed to load image")
            else:
                self.status_label.setText(f"❌ Image file not found: {image_path}")
        else:
            self.status_label.setText(f"❌ {result.get('error', 'Generation failed')}")
    
    def on_generation_error(self, error: str):
        """Handle generation error"""
        self.status_label.setText(f"❌ Error: {error}")
        QMessageBox.critical(
            self,
            "Generation Error",
            f"Failed to generate preview:\n{error}"
        )
    
    def get_identity_description(self) -> str:
        """Get current identity description"""
        return self.identity_input.toPlainText().strip()
    
    def set_identity_description(self, text: str):
        """Set identity description"""
        self.identity_input.setText(text)


class MemberRegistrationWindow(QMainWindow):
    """Main window for member registration"""
    
    # Signal emitted when member is created
    member_created = pyqtSignal(dict)
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Aurora Archive - Member Registration")
        self.setMinimumSize(1200, 800)
        
        # Member data being created
        self.member_data = {}
        
        self.setup_ui()
        self.apply_styles()
    
    def setup_ui(self):
        central = QWidget()
        self.setCentralWidget(central)
        layout = QVBoxLayout(central)
        layout.setContentsMargins(20, 20, 20, 20)
        
        # Header
        header = QLabel("👤 New Member Registration")
        header.setStyleSheet("font-size: 24px; font-weight: bold; color: #9333ea; padding: 10px;")
        layout.addWidget(header)
        
        # Main splitter (form on left, preview on right)
        splitter = QSplitter(Qt.Orientation.Horizontal)
        
        # Left side: Form tabs
        form_widget = self.create_form_tabs()
        splitter.addWidget(form_widget)
        
        # Right side: Identity & Preview
        self.preview_panel = IdentityPreviewPanel()
        splitter.addWidget(self.preview_panel)
        
        # Set initial splitter sizes (60% form, 40% preview)
        splitter.setSizes([720, 480])
        
        layout.addWidget(splitter, stretch=1)
        
        # Bottom buttons
        button_layout = QHBoxLayout()
        button_layout.addStretch()
        
        cancel_btn = QPushButton("✖ Cancel")
        cancel_btn.clicked.connect(self.close)
        button_layout.addWidget(cancel_btn)
        
        save_draft_btn = QPushButton("💾 Save Draft")
        save_draft_btn.clicked.connect(self.save_draft)
        button_layout.addWidget(save_draft_btn)
        
        create_btn = QPushButton("✓ Create Member & Generate Card")
        create_btn.setStyleSheet("""
            QPushButton {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                    stop:0 #9333ea, stop:1 #ec4899);
                color: white;
                font-weight: bold;
                padding: 12px 24px;
                border-radius: 6px;
                font-size: 14px;
            }
            QPushButton:hover {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                    stop:0 #a855f7, stop:1 #f472b6);
            }
        """)
        create_btn.clicked.connect(self.create_member)
        button_layout.addWidget(create_btn)
        
        layout.addLayout(button_layout)
    
    def create_form_tabs(self) -> QWidget:
        """Create tabbed form interface"""
        tabs = QTabWidget()
        tabs.setStyleSheet("""
            QTabWidget::pane {
                border: 1px solid rgba(168, 85, 247, 0.3);
                background-color: rgba(0, 0, 0, 0.2);
            }
            QTabBar::tab {
                background-color: rgba(255, 255, 255, 0.05);
                color: #c084fc;
                padding: 12px 24px;
                margin-right: 4px;
                border-radius: 8px;
                font-weight: bold;
            }
            QTabBar::tab:selected {
                background-color: #9333ea;
                color: white;
            }
        """)
        
        # Profile tab
        tabs.addTab(self.create_profile_tab(), "📋 Profile")
        
        # Subscription tab
        tabs.addTab(self.create_subscription_tab(), "💳 Subscription")
        
        # Preferences tab
        tabs.addTab(self.create_preferences_tab(), "⚙️ Preferences")
        
        # Contact tab
        tabs.addTab(self.create_contact_tab(), "📞 Contact & Address")
        
        return tabs
    
    def create_profile_tab(self):
        """Create profile tab"""
        widget = QWidget()
        layout = QVBoxLayout(widget)
        
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll_content = QWidget()
        form = QGridLayout(scroll_content)
        form.setColumnStretch(1, 1)
        
        row = 0
        
        # Name (required)
        form.addWidget(QLabel("* Full Name:"), row, 0)
        self.name_input = QLineEdit()
        self.name_input.setPlaceholderText("Enter full name")
        form.addWidget(self.name_input, row, 1)
        row += 1
        
        # Email (required)
        form.addWidget(QLabel("* Email:"), row, 0)
        self.email_input = QLineEdit()
        self.email_input.setPlaceholderText("email@example.com")
        form.addWidget(self.email_input, row, 1)
        row += 1
        
        # Phone
        form.addWidget(QLabel("Phone:"), row, 0)
        self.phone_input = QLineEdit()
        self.phone_input.setPlaceholderText("+1234567890")
        form.addWidget(self.phone_input, row, 1)
        row += 1
        
        # Gender
        form.addWidget(QLabel("Gender:"), row, 0)
        self.gender_combo = QComboBox()
        self.gender_combo.addItems(["Prefer not to say", "Male", "Female", "Non-binary", "Other"])
        form.addWidget(self.gender_combo, row, 1)
        row += 1
        
        # Age
        form.addWidget(QLabel("Age:"), row, 0)
        self.age_input = QSpinBox()
        self.age_input.setRange(0, 150)
        self.age_input.setValue(0)
        self.age_input.setSpecialValueText("Not specified")
        form.addWidget(self.age_input, row, 1)
        row += 1
        
        # Birthdate (for age verification and auto-tier assignment)
        form.addWidget(QLabel("Birthdate:"), row, 0)
        birthdate_layout = QHBoxLayout()
        self.birthdate_input = QLineEdit()
        self.birthdate_input.setPlaceholderText("YYYY-MM-DD (for age verification)")
        self.birthdate_input.textChanged.connect(self.on_birthdate_changed)
        birthdate_layout.addWidget(self.birthdate_input)
        
        self.age_auto_label = QLabel("")
        self.age_auto_label.setStyleSheet("color: #10b981; font-size: 11px;")
        birthdate_layout.addWidget(self.age_auto_label)
        
        form.addLayout(birthdate_layout, row, 1)
        row += 1
        
        # Age restriction warning
        self.age_restriction_warning = QLabel("")
        self.age_restriction_warning.setStyleSheet("""
            QLabel {
                background-color: rgba(234, 179, 8, 0.2);
                border: 1px solid #eab308;
                border-radius: 6px;
                padding: 8px;
                color: #fbbf24;
                font-size: 11px;
            }
        """)
        self.age_restriction_warning.setWordWrap(True)
        self.age_restriction_warning.hide()
        form.addWidget(self.age_restriction_warning, row, 0, 1, 2)
        row += 1
        
        # Bio
        form.addWidget(QLabel("Bio:"), row, 0, Qt.AlignmentFlag.AlignTop)
        self.bio_input = QTextEdit()
        self.bio_input.setPlaceholderText("Brief description...")
        self.bio_input.setMaximumHeight(80)
        form.addWidget(self.bio_input, row, 1)
        row += 1
        
        # Location
        form.addWidget(QLabel("Location:"), row, 0)
        self.location_input = QLineEdit()
        self.location_input.setPlaceholderText("City, State/Country")
        form.addWidget(self.location_input, row, 1)
        row += 1
        
        # Interests
        form.addWidget(QLabel("Interests:"), row, 0)
        self.interests_input = QLineEdit()
        self.interests_input.setPlaceholderText("reading, gaming, art (comma-separated)")
        form.addWidget(self.interests_input, row, 1)
        row += 1
        
        scroll.setWidget(scroll_content)
        layout.addWidget(scroll)
        
        return widget
    
    def create_subscription_tab(self):
        """Create subscription tab"""
        widget = QWidget()
        layout = QVBoxLayout(widget)
        
        form = QGridLayout()
        form.setColumnStretch(1, 1)
        row = 0
        
        # Tier
        form.addWidget(QLabel("* Membership Tier:"), row, 0)
        self.tier_combo = QComboBox()
        self.tier_combo.addItems(["Kids ($5/month)", "Standard ($10/month)", "Premium ($15/month)"])
        self.tier_combo.setCurrentIndex(1)
        self.tier_combo.currentIndexChanged.connect(self.on_tier_changed)
        form.addWidget(self.tier_combo, row, 1)
        row += 1
        
        # Tier restriction note
        self.tier_restriction_label = QLabel("")
        self.tier_restriction_label.setStyleSheet("""
            QLabel {
                background-color: rgba(239, 68, 68, 0.2);
                border: 1px solid #ef4444;
                border-radius: 6px;
                padding: 8px;
                color: #fca5a5;
                font-size: 11px;
            }
        """)
        self.tier_restriction_label.setWordWrap(True)
        self.tier_restriction_label.hide()
        form.addWidget(self.tier_restriction_label, row, 0, 1, 2)
        row += 1
        
        # Tier info
        tier_info = QLabel(
            "🔒 Age-based tier restrictions:\n"
            "• Under 18: Automatically assigned Kids tier (safety restrictions apply)\n"
            "• 18+: Can select any tier\n\n"
            "📊 Tier features:\n"
            "• Kids: 5 generations/day, safe content only, template-based\n"
            "• Standard: 3 generations/day, custom prompts, standard features\n"
            "• Premium: Unlimited generations, all features, priority support"
        )
        tier_info.setStyleSheet("color: #a78bfa; font-size: 11px; padding: 10px;")
        form.addWidget(tier_info, row, 0, 1, 2)
        row += 1
        
        # Billing cycle
        form.addWidget(QLabel("Billing Cycle:"), row, 0)
        self.billing_combo = QComboBox()
        self.billing_combo.addItems(["Monthly", "Yearly (10% off)"])
        form.addWidget(self.billing_combo, row, 1)
        row += 1
        
        # Auto-renew
        self.auto_renew_check = QCheckBox("Auto-renew subscription")
        self.auto_renew_check.setChecked(True)
        form.addWidget(self.auto_renew_check, row, 0, 1, 2)
        row += 1
        
        layout.addLayout(form)
        layout.addStretch()
        
        return widget
    
    def create_preferences_tab(self):
        """Create preferences tab"""
        widget = QWidget()
        layout = QVBoxLayout(widget)
        
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll_content = QWidget()
        form = QGridLayout(scroll_content)
        form.setColumnStretch(1, 1)
        
        row = 0
        
        # Card Generation
        form.addWidget(QLabel("─── Card Generation ───"), row, 0, 1, 2)
        row += 1
        
        form.addWidget(QLabel("Art Style:"), row, 0)
        self.art_style_combo = QComboBox()
        self.art_style_combo.addItems(["fantasy", "sci-fi", "anime", "realistic", "abstract", "cyberpunk"])
        form.addWidget(self.art_style_combo, row, 1)
        row += 1
        
        form.addWidget(QLabel("Color Scheme:"), row, 0)
        self.color_scheme_combo = QComboBox()
        self.color_scheme_combo.addItems([
            "azure_silver", "crimson_gold", "emerald_jade", "violet_amethyst",
            "sapphire_pearl", "ruby_onyx", "amber_bronze"
        ])
        form.addWidget(self.color_scheme_combo, row, 1)
        row += 1
        
        form.addWidget(QLabel("Card Border:"), row, 0)
        self.border_combo = QComboBox()
        self.border_combo.addItems(["tribal_arcane", "futuristic_tech", "elegant_classic", "ornate_baroque"])
        form.addWidget(self.border_combo, row, 1)
        row += 1
        
        # Notifications
        form.addWidget(QLabel("─── Notifications ───"), row, 0, 1, 2)
        row += 1
        
        self.email_notif_check = QCheckBox("Email notifications")
        self.email_notif_check.setChecked(True)
        form.addWidget(self.email_notif_check, row, 0, 1, 2)
        row += 1
        
        self.sms_notif_check = QCheckBox("SMS notifications")
        form.addWidget(self.sms_notif_check, row, 0, 1, 2)
        row += 1
        
        # Reading
        form.addWidget(QLabel("─── Reading ───"), row, 0, 1, 2)
        row += 1
        
        form.addWidget(QLabel("Favorite Genres:"), row, 0)
        self.genres_input = QLineEdit()
        self.genres_input.setPlaceholderText("fantasy, sci-fi, mystery")
        self.genres_input.setText("fantasy, sci-fi")
        form.addWidget(self.genres_input, row, 1)
        row += 1
        
        form.addWidget(QLabel("Language:"), row, 0)
        self.language_combo = QComboBox()
        self.language_combo.addItems(["en", "es", "fr", "de", "ja", "zh"])
        form.addWidget(self.language_combo, row, 1)
        row += 1
        
        scroll.setWidget(scroll_content)
        layout.addWidget(scroll)
        
        return widget
    
    def create_contact_tab(self):
        """Create contact/address tab"""
        widget = QWidget()
        layout = QVBoxLayout(widget)
        
        form = QGridLayout()
        form.setColumnStretch(1, 1)
        row = 0
        
        # Address
        form.addWidget(QLabel("Street Address:"), row, 0)
        self.street_input = QLineEdit()
        form.addWidget(self.street_input, row, 1)
        row += 1
        
        form.addWidget(QLabel("City:"), row, 0)
        self.city_input = QLineEdit()
        form.addWidget(self.city_input, row, 1)
        row += 1
        
        form.addWidget(QLabel("State/Province:"), row, 0)
        self.state_input = QLineEdit()
        form.addWidget(self.state_input, row, 1)
        row += 1
        
        form.addWidget(QLabel("ZIP/Postal Code:"), row, 0)
        self.zip_input = QLineEdit()
        form.addWidget(self.zip_input, row, 1)
        row += 1
        
        form.addWidget(QLabel("Country:"), row, 0)
        self.country_input = QLineEdit()
        self.country_input.setPlaceholderText("USA")
        form.addWidget(self.country_input, row, 1)
        row += 1
        
        layout.addLayout(form)
        layout.addStretch()
        
        return widget
    
    def get_current_member_data(self) -> Dict:
        """Get current member data from form"""
        interests_text = self.interests_input.text().strip()
        interests = [i.strip() for i in interests_text.split(',')] if interests_text else []
        
        genres_text = self.genres_input.text().strip()
        genres = [g.strip() for g in genres_text.split(',')] if genres_text else []
        
        tier_text = self.tier_combo.currentText()
        tier = tier_text.split()[0]  # Extract "Kids", "Standard", "Premium"
        
        return {
            'name': self.name_input.text().strip(),
            'email': self.email_input.text().strip(),
            'phone': self.phone_input.text().strip(),
            'gender': self.gender_combo.currentText(),
            'age': self.age_input.value() if self.age_input.value() > 0 else None,
            'birthdate': self.birthdate_input.text().strip() or None,  # For age verification
            'bio': self.bio_input.toPlainText().strip(),
            'location': self.location_input.text().strip(),
            'interests': interests,
            'tier': tier,
            'billing_cycle': self.billing_combo.currentText(),
            'auto_renew': self.auto_renew_check.isChecked(),
            'art_style': self.art_style_combo.currentText(),
            'color_scheme': self.color_scheme_combo.currentText(),
            'card_border': self.border_combo.currentText(),
            'email_notifications': self.email_notif_check.isChecked(),
            'sms_notifications': self.sms_notif_check.isChecked(),
            'reading_genres': genres,  # Changed from 'favorite_genres'
            'language': self.language_combo.currentText(),
            'street': self.street_input.text().strip(),
            'city': self.city_input.text().strip(),
            'state': self.state_input.text().strip(),
            'zip': self.zip_input.text().strip(),
            'country': self.country_input.text().strip(),
            'identity_description': self.preview_panel.get_identity_description()
        }
    
    def save_draft(self):
        """Save draft to JSON file"""
        member_data = self.get_current_member_data()
        
        if not member_data['name']:
            QMessageBox.warning(
                self,
                "Incomplete Data",
                "Please enter at least a name before saving draft."
            )
            return
        
        # Ask where to save
        filepath, _ = QFileDialog.getSaveFileName(
            self,
            "Save Member Draft",
            str(Path.home() / "Desktop" / f"{member_data['name']}_draft.json"),
            "JSON Files (*.json);;All Files (*)"
        )
        
        if filepath:
            try:
                with open(filepath, 'w', encoding='utf-8') as f:
                    json.dump(member_data, f, indent=2, ensure_ascii=False)
                
                QMessageBox.information(
                    self,
                    "Draft Saved",
                    f"✓ Member draft saved to:\n{filepath}"
                )
            except Exception as e:
                QMessageBox.critical(
                    self,
                    "Save Error",
                    f"Failed to save draft:\n{str(e)}"
                )
    
    def on_birthdate_changed(self):
        """Handle birthdate input changes - calculate age and check tier restrictions"""
        birthdate = self.birthdate_input.text().strip()
        
        if not birthdate:
            self.age_auto_label.setText("")
            self.age_restriction_warning.hide()
            self.tier_combo.setEnabled(True)
            self.tier_restriction_label.hide()
            return
        
        try:
            from member_manager import MemberManager
            manager = MemberManager()
            
            # Calculate age
            age = manager.calculate_age_from_birthdate(birthdate)
            self.age_auto_label.setText(f"✓ Age: {age}")
            
            # Check if under 18
            if age < 18:
                days_until_18 = (datetime.fromisoformat(manager.calculate_18th_birthday(birthdate)).date() - 
                               datetime.now().date()).days
                
                self.age_restriction_warning.setText(
                    f"⚠️ Age Restriction: Users under 18 are automatically assigned to Kids tier with safety restrictions.\n"
                    f"You will be able to upgrade to Standard tier in {days_until_18} days (on your 18th birthday)."
                )
                self.age_restriction_warning.show()
                
                # Force Kids tier selection
                self.tier_combo.setCurrentIndex(0)  # Kids
                self.tier_combo.setEnabled(False)  # Lock tier selection
                self.tier_restriction_label.setText(
                    "🔒 Tier selection locked: Under 18 must use Kids tier"
                )
                self.tier_restriction_label.show()
            else:
                self.age_restriction_warning.hide()
                self.tier_combo.setEnabled(True)
                self.tier_restriction_label.hide()
                
        except Exception as e:
            self.age_auto_label.setText(f"❌ Invalid date format")
            self.age_auto_label.setStyleSheet("color: #ef4444; font-size: 11px;")
    
    def on_tier_changed(self):
        """Handle tier selection changes - validate against age restrictions"""
        # Get birthdate if entered
        birthdate = self.birthdate_input.text().strip()
        
        if not birthdate:
            return
        
        try:
            from member_manager import MemberManager
            manager = MemberManager()
            age = manager.calculate_age_from_birthdate(birthdate)
            
            selected_tier = self.tier_combo.currentText().split()[0]  # Extract tier name
            
            # Prevent non-Kids tier selection for under 18
            if age < 18 and selected_tier != "Kids":
                self.tier_combo.setCurrentIndex(0)  # Force Kids
                QMessageBox.warning(
                    self,
                    "Age Restriction",
                    f"Users under 18 must use Kids tier.\n\n"
                    f"Current age: {age}\n"
                    f"You can upgrade to {selected_tier} tier on your 18th birthday."
                )
        except:
            pass
    
    def load_draft(self, filepath: str):
        """Load draft from JSON file"""
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                data = json.load(f)
            
            # Populate form fields
            self.name_input.setText(data.get('name', ''))
            self.email_input.setText(data.get('email', ''))
            self.phone_input.setText(data.get('phone', ''))
            
            gender = data.get('gender', 'Prefer not to say')
            index = self.gender_combo.findText(gender)
            if index >= 0:
                self.gender_combo.setCurrentIndex(index)
            
            if data.get('age'):
                self.age_input.setValue(data['age'])
            
            self.bio_input.setText(data.get('bio', ''))
            self.location_input.setText(data.get('location', ''))
            self.interests_input.setText(', '.join(data.get('interests', [])))
            
            # Subscription
            tier = data.get('tier', 'Standard')
            for i in range(self.tier_combo.count()):
                if tier in self.tier_combo.itemText(i):
                    self.tier_combo.setCurrentIndex(i)
                    break
            
            # Preferences
            self.art_style_combo.setCurrentText(data.get('art_style', 'fantasy'))
            self.color_scheme_combo.setCurrentText(data.get('color_scheme', 'azure_silver'))
            self.border_combo.setCurrentText(data.get('card_border', 'tribal_arcane'))
            
            # Identity
            if data.get('identity_description'):
                self.preview_panel.set_identity_description(data['identity_description'])
            
            QMessageBox.information(
                self,
                "Draft Loaded",
                f"✓ Member draft loaded successfully!"
            )
            
        except Exception as e:
            QMessageBox.critical(
                self,
                "Load Error",
                f"Failed to load draft:\n{str(e)}"
            )
    
    def create_member(self):
        """Create member and generate card"""
        member_data = self.get_current_member_data()
        
        # Validation
        if not member_data['name']:
            QMessageBox.warning(self, "Required Field", "Please enter a name.")
            return
        
        if not member_data['email'] or '@' not in member_data['email']:
            QMessageBox.warning(self, "Required Field", "Please enter a valid email.")
            return
        
        try:
            from member_manager import MemberManager
            
            member_manager = MemberManager()
            
            # Create full member schema
            full_member_data = member_manager.create_new_member(
                name=member_data['name'],
                email=member_data['email'],
                tier=member_data['tier'],
                phone=member_data.get('phone'),
                gender=member_data.get('gender'),
                age=member_data.get('age'),
                birthdate=member_data.get('birthdate'),  # For age-based tier assignment
                bio=member_data.get('bio'),
                location=member_data.get('location'),
                interests=member_data.get('interests', []),
                street=member_data.get('street', ''),
                city=member_data.get('city', ''),
                state=member_data.get('state', ''),
                zip_code=member_data.get('zip', ''),
                country=member_data.get('country', ''),
                billing_cycle=member_data.get('billing_cycle', 'monthly'),
                auto_renew=member_data.get('auto_renew', True),
                reading_genres=member_data.get('reading_genres', []),
                reading_language=member_data.get('language', 'en'),
                art_style=member_data.get('art_style', 'fantasy'),
                color_scheme=member_data.get('color_scheme', 'azure_silver'),
                card_border=member_data.get('card_border', 'tribal_arcane'),
                email_notifications=member_data.get('email_notifications', True),
                sms_notifications=member_data.get('sms_notifications', False)
            )
            
            # Add identity description to metadata
            if member_data.get('identity_description'):
                if 'metadata' not in full_member_data:
                    full_member_data['metadata'] = {}
                full_member_data['metadata']['identity_description'] = member_data['identity_description']
            
            # Emit signal with member data
            self.member_created.emit(full_member_data)
            
            # Build success message
            assigned_tier = full_member_data['subscription']['tier']
            tier_reason = full_member_data['subscription'].get('tier_assignment_reason', '')
            
            success_msg = f"✓ Member {member_data['name']} created successfully!\n\n"
            success_msg += f"Tier: {assigned_tier}\n"
            
            # Show tier assignment reason if auto-assigned
            if 'Automatic' in tier_reason:
                success_msg += f"\n{tier_reason}\n"
                
                if assigned_tier == "Kids":
                    upgrade_date = full_member_data['subscription'].get('auto_upgrade_date')
                    if upgrade_date:
                        success_msg += f"Auto-upgrade to Standard on: {upgrade_date}\n"
            
            success_msg += "\nReturning to main application..."
            
            # Show success and close
            QMessageBox.information(
                self,
                "Member Created",
                success_msg
            )
            
            self.accept() if hasattr(self, 'accept') else self.close()
            
        except Exception as e:
            QMessageBox.critical(
                self,
                "Creation Error",
                f"Failed to create member:\n{str(e)}"
            )
    
    def apply_styles(self):
        """Apply dark theme styling"""
        self.setStyleSheet("""
            QMainWindow, QWidget {
                background-color: #0f172a;
                color: white;
            }
            QLabel {
                color: #c084fc;
            }
            QLineEdit, QTextEdit, QSpinBox, QComboBox {
                background-color: rgba(255, 255, 255, 0.05);
                border: 1px solid rgba(168, 85, 247, 0.3);
                border-radius: 4px;
                padding: 8px;
                color: white;
            }
            QLineEdit:focus, QTextEdit:focus {
                border: 1px solid #9333ea;
            }
            QCheckBox {
                color: white;
            }
            QPushButton {
                background-color: #9333ea;
                color: white;
                border: none;
                border-radius: 6px;
                padding: 10px 16px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #a855f7;
            }
            QScrollArea {
                border: none;
            }
            QComboBox::drop-down {
                border: none;
            }
            QComboBox::down-arrow {
                image: none;
                border-left: 5px solid transparent;
                border-right: 5px solid transparent;
                border-top: 5px solid white;
            }
        """)


def main():
    """Standalone application entry point"""
    app = QApplication(sys.argv)
    
    # Set application font
    font = QFont("Segoe UI", 10)
    app.setFont(font)
    
    window = MemberRegistrationWindow()
    
    # Connect member_created signal for standalone mode
    def on_member_created(member_data):
        print("✓ Member created successfully!")
        print(json.dumps(member_data, indent=2))
    
    window.member_created.connect(on_member_created)
    window.show()
    
    sys.exit(app.exec())


if __name__ == '__main__':
    main()
