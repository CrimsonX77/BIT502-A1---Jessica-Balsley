import sys
from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QLabel, QPushButton, QComboBox, QHBoxLayout, QListWidget,
    QProgressBar, QSpinBox, QGroupBox, QGridLayout, QScrollArea, QFrame, QSlider
)
from PyQt6.QtCore import Qt, pyqtSignal, QObject, QTimer
import random
import json
import os
import time
from collections import defaultdict

# ---- RPG Stat & Loot Definitions ----

STAT_NAMES = ["STR", "INT", "WIS", "CHA", "AGI", "DEX", "LIB"]

DEFAULT_STATS = {stat: 0 for stat in STAT_NAMES}

LOOTBOX_TABLE = [
    # name, emoji, effects
    ("Bread", "🍞", {"WIS": 1}),
    ("Rare Idea", "🧠", {"INT": 4, "WIS": 3}),
    ("Legendary Sword", "🔥", {"STR": 5, "INT": -1, "CHA": 1, "AGI": 2}),
    ("Top Hat", "🎩", {"INT": 2, "WIS": 1, "CHA": 2}),
    ("Lucky Charm", "🍀", {"WIS": 2, "CHA": 2, "AGI": 1}),
    ("Cat Plush", "🐱", {}),
    ("Gem", "💎", {"STR": 2}),
    ("Magic Scroll", "📜", {"INT": 3, "WIS": 2}),
    ("Boots of Speed", "👢", {"AGI": 4, "DEX": 1}),
    ("Crown", "👑", {"CHA": 5, "WIS": -1}),
    ("Ancient Tome", "📚", {"INT": 4, "WIS": 4}),
    ("Dragon Egg", "🐉", {"STR": 3, "CHA": 3, "AGI": 2}),
    ("Enchanted Mirror", "🪞", {"CHA": 4, "DEX": 1}),
    ("Philosopher's Stone", "🪨", {"INT": 5, "WIS": 5, "CHA": 5}),
    ("Mystic Amulet", "📿", {"WIS": 3, "CHA": 3}),
    ("Silver Dagger", "🗡️", {"DEX": 4, "AGI": 2}),
    ("Golden Chalice", "🏆", {"CHA": 4, "WIS": 2}),
    ("Potion of Strength", "🧪", {"STR": 4}),
    ("Elven Bow", "🏹", {"DEX": 5, "AGI": 3}),
    ("Wizard's Hat", "🧙‍♂️", {"INT": 3, "WIS": 3, "CHA": 1}),
    ("Shield of Valor", "🛡️", {"STR": 3, "WIS": 2}),
    ("Ring of Invisibility", "💍", {"AGI": 5, "DEX": 2}),
    ("Cloak of Shadows", "🦹‍♂️", {"AGI": 4, "DEX": 3}),
    ("Staff of Power", "🔮", {"INT": 4, "WIS": 4}),
    ("Helmet of Insight", "⛑️", {"WIS": 5}),
    ("Boots of Levitation", "👟", {"AGI": 3, "DEX": 2}),
    ("Orb of Mystery", "🟠", {"INT": 2, "WIS": 2, "CHA": 2}),
    ("Sapphire Necklace", "💙", {"CHA": 3}),
    ("Ruby Ring", "❤️", {"STR": 2, "CHA": 2}),
    ("Emerald Bracelet", "💚", {"DEX": 3}),
    ("Amethyst Earring", "💜", {"WIS": 3}),
    ("Topaz Pendant", "💛", {"INT": 3}),
    ("Obsidian Dagger", "⚫", {"DEX": 4}),
    ("Crystal Ball", "🔵", {"WIS": 4}),
    ("Phoenix Feather", "🪶", {"STR": 3, "AGI": 3}),
    ("Unicorn Horn", "🦄", {"CHA": 5}),
    ("Griffin Claw", "🦅", {"STR": 4, "DEX": 2}),
    ("Mermaid Scale", "🧜‍♀️", {"WIS": 3, "CHA": 2}),
    ("Vampire Fang", "🧛‍♂️", {"STR": 3, "DEX": 1, "CHA": 1}),
    ("Werewolf Pelt", "🐺", {"STR": 4, "AGI": 2}),
    ("Zombie Brain", "🧟‍♂️", {"INT": -2, "WIS": -2, "CHA": -2}),
    ("Goblin Ear", "👂", {"DEX": 1, "AGI": 1}),
    ("Troll Tooth", "🦷", {"STR": 2}),
    ("Fairy Dust", "✨", {"WIS": 2, "CHA": 3}),
    ("Dwarf Hammer", "🔨", {"STR": 4, "DEX": -1}),
    ("Elf Leaf", "🍃", {"AGI": 3, "DEX": 2}),
    ("Orc Tusks", "🐗", {"STR": 5, "CHA": -1}),
    ("Skeleton Ribcage", "🦴", {"STR": 1, "WIS": -1}),
    ("Centaur Hoof", "🐴", {"STR": 3, "AGI": 2}),
    ("Minotaur Horn", "🐂", {"STR": 4, "WIS": -1}),
    ("Hydra Scale", "🐉", {"STR": 3, "WIS": 2, "CHA": 1}),
    ("Cyclops Eye", "👁️", {"INT": 2, "WIS": 3}),
    ("Giant's Toe", "🦶", {"STR": 5, "DEX": -2}),
    ("Leprechaun Gold", "💰", {"CHA": 4}),
    ("Nymph Hair", "💇‍♀️", {"CHA": 3, "WIS": 2}),
    ("Satyr Horns", "🐐", {"DEX": 2, "AGI": 2, "CHA": 1}),
    ("Siren Songbook", "📖", {"CHA": 5, "WIS": -1}),
    ("Basilisk Fang", "🦷", {"STR": 3, "DEX": 1}),
    ("Chimera Claw", "🦾", {"STR": 4, "AGI": 2}),
    ("Gorgon Scale", "🟢", {"DEX": 3, "WIS": 2}),
    ("Harpy Feather", "🪶", {"AGI": 4, "DEX": 1}),
    ("Imp Tail", "👹", {"CHA": -2, "DEX": 1}),
    ("Kelpie Mane", "🐎", {"AGI": 3, "STR": 2}),
    ("Manticore Spine", "🦴", {"STR": 4, "DEX": 2}),
    ("Pixie Wing", "🧚‍♀️", {"AGI": 5, "CHA": 2}),
    ("Quetzalcoatl Scale", "🐍", {"INT": 4, "WIS": 3}),
    ("Roc Feather", "🪶", {"STR": 4, "AGI": 3}),
    ("Yuri-Hentai", "",{"LIB":10}),
    ("Salamander Tail", "🦎", {"STR": 2, "AGI": 2}),
    ("Treant Bark", "🌳", {"STR": 3, "WIS": 2}),
    ("Wraith Essence", "👻", {"INT": 3, "WIS": 3}),
    ("Yeti Fur", "🦣", {"STR": 4, "WIS": -1}),
    ("Zombie Hand", "🧟‍♂️", {"STR": 2, "WIS": -2}),
    ("Cookie", "🍪", {"WIS": 1}),
    ("Mystery Box", "🎁", "RANDOM"),  # Special marker for random effects
    # ...extend as needed
]

RARITY_WEIGHTS = None  # Will be generated dynamically to match LOOTBOX_TABLE size

def get_rarity_weights():
    """Generate rarity weights that match the lootbox table size"""
    if RARITY_WEIGHTS is not None and len(RARITY_WEIGHTS) == len(LOOTBOX_TABLE):
        return RARITY_WEIGHTS
    
    # Create weights with rarity distribution
    # Common items (first ~60%): weight 10
    # Uncommon items (next ~25%): weight 5  
    # Rare items (next ~10%): weight 2
    # Legendary items (last ~5%): weight 1
    
    total_items = len(LOOTBOX_TABLE)
    weights = []
    
    for i in range(total_items):
        if i < total_items * 0.6:  # Common (60%)
            weights.append(10)
        elif i < total_items * 0.85:  # Uncommon (25%) 
            weights.append(5)
        elif i < total_items * 0.95:  # Rare (10%)
            weights.append(2)
        else:  # Legendary (5%)
            weights.append(1)
    
# ---- Mood System & Advanced Mechanics ----

MOOD_TIERS = [
    # (min_mood_value, mood_name, emoji, description)
    (-100, "devastated", "💀", "Utterly broken"),
    (-50, "despondent", "😭", "In despair"),
    (-30, "miserable", "😰", "Deeply unhappy"),
    (-15, "troubled", "😟", "Quite worried"),
    (-5, "uneasy", "😕", "Mildly concerned"),
    (-1, "slightly down", "😐", "A bit off"),
    (0, "neutral", "😶", "Balanced"),
    (2, "content", "🙂", "Reasonably pleased"),
    (5, "pleased", "😊", "Quite happy"),
    (10, "confident", "😎", "Self-assured"),
    (20, "joyful", "😄", "Very happy"),
    (35, "elated", "🤩", "Extremely pleased"),
    (50, "euphoric", "🥳", "Overwhelmed with joy"),
    (70, "transcendent", "✨", "Beyond earthly concerns"),
    (100, "divine", "👑", "Godlike satisfaction"),
    (150, "erotic", "💋", "Intensely aroused"),  # Special threshold
]

def get_mood_from_value(mood_value):
    """Get mood info from mood value"""
    for min_val, name, emoji, desc in reversed(MOOD_TIERS):
        if mood_value >= min_val:
            return name, emoji, desc
    return MOOD_TIERS[0][1], MOOD_TIERS[0][2], MOOD_TIERS[0][3]

def get_rarity_from_index(idx, total_items):
    """Get rarity tier from lootbox table index"""
    if idx < total_items * 0.6:
        return "common", 1.0
    elif idx < total_items * 0.85:
        return "uncommon", 1.5
    elif idx < total_items * 0.95:
        return "rare", 2.5
    else:
        return "legendary", 4.0

def calculate_main_stat_bonus(stats):
    """Calculate bonus from having high main stats"""
    main_stats = ["STR", "INT", "WIS", "CHA"]
    total_main = sum(stats.get(stat, 0) for stat in main_stats)
    return total_main * 0.3  # Each main stat point gives 0.3 mood bonus

# ---- Data Persistence ----

def load_stats(filepath="cookiejar_stats.json"):
    if os.path.exists(filepath):
        with open(filepath, "r") as f:
            data = json.load(f)
            if isinstance(data, dict) and 'stats' in data:
                return data
            else:
                # Legacy format - convert to new format
                return {
                    'stats': data if isinstance(data, dict) else dict(DEFAULT_STATS),
                    'inventory': defaultdict(int),
                    'mood_value': 0.0,
                    'last_lootbox_time': 0,
                    'total_boxes_opened': 0
                }
    return {
        'stats': dict(DEFAULT_STATS),
        'inventory': defaultdict(int),
        'mood_value': 0.0,
        'last_lootbox_time': 0,
        'total_boxes_opened': 0
    }

def save_stats(data, filepath="cookiejar_stats.json"):
    # Convert defaultdict to regular dict for JSON serialization
    save_data = dict(data)
    save_data['inventory'] = dict(save_data['inventory'])
    with open(filepath, "w") as f:
        json.dump(save_data, f, indent=2)

# ---- Lootbox Engine (standalone) ----

class LootboxEngine(QObject):
    lootbox_opened = pyqtSignal(dict, dict, float)  # loot_item, new_stats, mood_change

    def __init__(self, save_data=None):
        super().__init__()
        if save_data is None:
            save_data = load_stats()
        
        self.stats = save_data.get('stats', dict(DEFAULT_STATS))
        self.inventory = defaultdict(int, save_data.get('inventory', {}))
        self.mood_value = save_data.get('mood_value', 0.0)
        self.last_lootbox_time = save_data.get('last_lootbox_time', 0)
        self.total_boxes_opened = save_data.get('total_boxes_opened', 0)

    def open_lootbox(self, specific_item_idx=None):
        current_time = time.time()
        
        # Calculate time-based diminishing returns
        time_since_last = current_time - self.last_lootbox_time
        time_multiplier = min(1.0, time_since_last / 3.0)  # Full effect after 3 seconds
        
        if specific_item_idx is not None:
            idx = specific_item_idx
        else:
            weights = get_rarity_weights()
            idx = random.choices(range(len(LOOTBOX_TABLE)), weights=weights)[0]
        
        name, emoji, effects = LOOTBOX_TABLE[idx]
        
        # Handle special Mystery Box with random effects
        if effects == "RANDOM":
            effects = {
                stat: random.randint(-1, 3) 
                for stat in STAT_NAMES
            }
        
        # Apply effects to stats
        for stat, value in effects.items():
            self.stats[stat] = self.stats.get(stat, 0) + value
        
        # Add to inventory
        self.inventory[name] += 1
        
        # Calculate mood change
        mood_change = self.calculate_mood_change(idx, name, effects, time_multiplier)
        self.mood_value += mood_change
        
        # Update tracking
        self.last_lootbox_time = current_time
        self.total_boxes_opened += 1
        
        loot_item = {"name": name, "emoji": emoji, "effects": effects, "rarity": get_rarity_from_index(idx, len(LOOTBOX_TABLE))[0]}
        self.lootbox_opened.emit(loot_item, dict(self.stats), mood_change)
        return loot_item, dict(self.stats), mood_change

    def calculate_mood_change(self, item_idx, item_name, effects, time_multiplier):
        """Calculate mood change from opening a lootbox"""
        mood_change = 0.0
        
        # Base mood from opening any lootbox
        base_mood = 1.0 * time_multiplier
        
        # Rarity bonus
        rarity_name, rarity_multiplier = get_rarity_from_index(item_idx, len(LOOTBOX_TABLE))
        rarity_bonus = rarity_multiplier * time_multiplier
        
        # Diminishing returns for duplicate items (more you have, less exciting)
        owned_count = self.inventory[item_name]
        duplicate_penalty = max(0.1, 1.0 - (owned_count * 0.15))  # Min 10% excitement
        
        # Main stat bonus (positive effects on STR, INT, WIS, CHA are more exciting)
        main_stat_bonus = 0.0
        main_stats = ["STR", "INT", "WIS", "CHA"]
        for stat, value in effects.items():
            if stat in main_stats and value > 0:
                main_stat_bonus += value * 0.8
            elif stat in main_stats and value < 0:
                main_stat_bonus += value * 1.5  # Negative effects hurt mood more
        
        # Special bonuses for high-tier items
        if rarity_name == "legendary":
            main_stat_bonus *= 1.5
        
        # Calculate total mood change
        mood_change = (base_mood + rarity_bonus + main_stat_bonus) * duplicate_penalty
        
        # Add small random variance (±20%)
        variance = mood_change * 0.2 * (random.random() - 0.5) * 2
        mood_change += variance
        
        return round(mood_change, 2)

    def get_save_data(self):
        """Get all data for saving"""
        return {
            'stats': dict(self.stats),
            'inventory': dict(self.inventory),
            'mood_value': self.mood_value,
            'last_lootbox_time': self.last_lootbox_time,
            'total_boxes_opened': self.total_boxes_opened
        }

    def get_stats(self):
        return dict(self.stats)
    
    def get_mood_value(self):
        return self.mood_value
    
    def get_inventory(self):
        return dict(self.inventory)

    def set_mood_value(self, value):
        self.mood_value = value

# ---- PyQt6 Main GUI ----

class CookieJarGUI(QMainWindow):
    def __init__(self, orchestrator_hook=None):
        super().__init__()
        self.setWindowTitle("Cookie Jar RPG Lootbox - Advanced Edition")
        self.setGeometry(100, 100, 800, 700)
        
        save_data = load_stats()
        self.engine = LootboxEngine(save_data)
        self.orchestrator_hook = orchestrator_hook

        # ---- UI Layout ----
        widget = QWidget()
        self.setCentralWidget(widget)
        main_layout = QVBoxLayout(widget)

        # Stats and Mood Row
        stats_mood_layout = QHBoxLayout()
        
        # Stats Panel
        stats_group = QGroupBox("📊 Character Stats")
        stats_layout = QVBoxLayout(stats_group)
        self.stats_label = QLabel(self.stats_text())
        self.stats_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        stats_layout.addWidget(self.stats_label)
        stats_mood_layout.addWidget(stats_group)
        
        # Mood Panel
        mood_group = QGroupBox("💭 Current Mood")
        mood_layout = QVBoxLayout(mood_group)
        self.mood_label = QLabel("")
        self.mood_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        mood_layout.addWidget(self.mood_label)
        
        # Mood value display
        self.mood_value_label = QLabel("Mood Value: 0.0")
        self.mood_value_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        mood_layout.addWidget(self.mood_value_label)
        
        # Mood progress bar
        self.mood_progress = QProgressBar()
        self.mood_progress.setRange(-200, 200)
        mood_layout.addWidget(self.mood_progress)
        
        stats_mood_layout.addWidget(mood_group)
        main_layout.addLayout(stats_mood_layout)

        # Lootbox Controls
        loot_group = QGroupBox("🎁 Lootbox Controls")
        loot_layout = QVBoxLayout(loot_group)
        
        # Main lootbox button
        button_layout = QHBoxLayout()
        self.open_button = QPushButton("Open Random Lootbox 🎁")
        self.open_button.setMinimumHeight(40)
        button_layout.addWidget(self.open_button)
        
        # Specific item selector
        self.item_selector = QComboBox()
        self.item_selector.addItem("🎲 Random Item", -1)
        for idx, (name, emoji, effects) in enumerate(LOOTBOX_TABLE):
            rarity = get_rarity_from_index(idx, len(LOOTBOX_TABLE))[0]
            self.item_selector.addItem(f"{emoji} {name} ({rarity})", idx)
        button_layout.addWidget(self.item_selector)
        
        self.open_specific_button = QPushButton("Open Selected Item")
        self.open_specific_button.setMinimumHeight(40)
        button_layout.addWidget(self.open_specific_button)
        
        loot_layout.addLayout(button_layout)
        
        # Loot history (scrollable)
        history_layout = QHBoxLayout()
        
        # Recent loot
        recent_group = QGroupBox("📜 Recent Loot")
        recent_layout = QVBoxLayout(recent_group)
        self.loot_history = QListWidget()
        self.loot_history.setMaximumHeight(150)
        recent_layout.addWidget(self.loot_history)
        history_layout.addWidget(recent_group)
        
        # Inventory summary
        inventory_group = QGroupBox("🏰 Inventory Summary")
        inventory_layout = QVBoxLayout(inventory_group)
        
        # Scrollable inventory
        scroll_area = QScrollArea()
        scroll_widget = QWidget()
        self.inventory_layout = QGridLayout(scroll_widget)
        scroll_area.setWidget(scroll_widget)
        scroll_area.setWidgetResizable(True)
        scroll_area.setMaximumHeight(150)
        inventory_layout.addWidget(scroll_area)
        
        history_layout.addWidget(inventory_group)
        loot_layout.addLayout(history_layout)
        
        main_layout.addWidget(loot_group)
        
        # Advanced Controls
        advanced_group = QGroupBox("⚙️ Advanced Controls")
        advanced_layout = QHBoxLayout(advanced_group)
        
        # Mood controls
        mood_controls_layout = QVBoxLayout()
        mood_controls_layout.addWidget(QLabel("Mood Adjustment:"))
        self.mood_slider = QSlider(Qt.Orientation.Horizontal)
        self.mood_slider.setRange(-50, 50)
        self.mood_slider.setValue(0)
        mood_controls_layout.addWidget(self.mood_slider)
        
        mood_buttons_layout = QHBoxLayout()
        self.reset_mood_btn = QPushButton("Reset Mood")
        self.apply_mood_btn = QPushButton("Apply Adjustment")
        mood_buttons_layout.addWidget(self.reset_mood_btn)
        mood_buttons_layout.addWidget(self.apply_mood_btn)
        mood_controls_layout.addLayout(mood_buttons_layout)
        advanced_layout.addLayout(mood_controls_layout)
        
        # Stats display
        stats_info_layout = QVBoxLayout()
        self.total_boxes_label = QLabel("Total Boxes: 0")
        self.unique_items_label = QLabel("Unique Items: 0")
        stats_info_layout.addWidget(self.total_boxes_label)
        stats_info_layout.addWidget(self.unique_items_label)
        advanced_layout.addLayout(stats_info_layout)
        
        main_layout.addWidget(advanced_group)

        # ---- Signals ----
        self.open_button.clicked.connect(self.handle_random_lootbox)
        self.open_specific_button.clicked.connect(self.handle_specific_lootbox)
        self.engine.lootbox_opened.connect(self.update_after_loot)
        self.reset_mood_btn.clicked.connect(self.reset_mood)
        self.apply_mood_btn.clicked.connect(self.apply_mood_adjustment)

        # ---- Init ----
        self.update_all_displays()

    def stats_text(self):
        stats = self.engine.get_stats()
        return " | ".join([f"{k}: {v}" for k, v in stats.items()])

    def handle_random_lootbox(self):
        self.engine.open_lootbox()

    def handle_specific_lootbox(self):
        selected_idx = self.item_selector.currentData()
        if selected_idx >= 0:
            self.engine.open_lootbox(selected_idx)
        else:
            self.handle_random_lootbox()

    def update_after_loot(self, loot_item, stats, mood_change):
        self.update_all_displays()
        
        # Add to history with mood change info
        rarity = loot_item['rarity']
        mood_sign = "+" if mood_change >= 0 else ""
        desc = f"{loot_item['emoji']} {loot_item['name']} [{rarity}] (Mood: {mood_sign}{mood_change:.2f})"
        self.loot_history.addItem(desc)
        
        # Keep only last 20 items
        if self.loot_history.count() > 20:
            self.loot_history.takeItem(0)
        
        # Auto-scroll to bottom
        self.loot_history.scrollToBottom()
        
        # Save data
        save_stats(self.engine.get_save_data())
        
        if self.orchestrator_hook:
            self.orchestrator_hook("lootbox_opened", loot_item, stats, mood_change)

    def update_mood_display(self):
        mood_value = self.engine.get_mood_value()
        
        # Calculate mood with main stat bonus
        main_stat_bonus = calculate_main_stat_bonus(self.engine.get_stats())
        total_mood = mood_value + main_stat_bonus
        
        mood_name, mood_emoji, mood_desc = get_mood_from_value(total_mood)
        
        # Update displays
        self.mood_label.setText(f"{mood_emoji} {mood_name.title()}")
        self.mood_value_label.setText(f"Mood Value: {total_mood:.2f} (Base: {mood_value:.2f} + Stats: {main_stat_bonus:.2f})")
        
        # Update progress bar
        self.mood_progress.setValue(int(total_mood))
        
        # Color coding for mood progress bar
        if total_mood >= 150:  # Erotic threshold
            color = "#FF1493"  # Deep pink
        elif total_mood >= 100:  # Divine
            color = "#FFD700"  # Gold
        elif total_mood >= 50:  # Euphoric+
            color = "#00FF00"  # Bright green
        elif total_mood >= 10:  # Positive
            color = "#90EE90"  # Light green
        elif total_mood >= -10:  # Neutral range
            color = "#FFFF00"  # Yellow
        elif total_mood >= -30:  # Negative
            color = "#FFA500"  # Orange
        else:  # Very negative
            color = "#FF0000"  # Red
        
        self.mood_progress.setStyleSheet(f"QProgressBar::chunk {{ background-color: {color}; }}")

    def update_inventory_display(self):
        # Clear existing inventory display
        for i in reversed(range(self.inventory_layout.count())): 
            self.inventory_layout.itemAt(i).widget().setParent(None)
        
        inventory = self.engine.get_inventory()
        if not inventory:
            no_items_label = QLabel("No items collected yet")
            no_items_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
            self.inventory_layout.addWidget(no_items_label, 0, 0)
            return
        
        # Sort by count (most owned first)
        sorted_items = sorted(inventory.items(), key=lambda x: x[1], reverse=True)
        
        row, col = 0, 0
        max_cols = 4
        
        for item_name, count in sorted_items:
            # Find emoji for this item
            emoji = "❓"  # Default
            for name, item_emoji, _ in LOOTBOX_TABLE:
                if name == item_name:
                    emoji = item_emoji
                    break
            
            item_label = QLabel(f"{emoji} {count}")
            item_label.setToolTip(f"{item_name}: {count} owned")
            item_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
            item_label.setStyleSheet("border: 1px solid gray; padding: 2px; margin: 1px;")
            
            self.inventory_layout.addWidget(item_label, row, col)
            col += 1
            if col >= max_cols:
                col = 0
                row += 1

    def update_stats_display(self):
        # Update basic stats
        self.stats_label.setText(self.stats_text())
        
        # Update advanced info
        self.total_boxes_label.setText(f"Total Boxes: {self.engine.total_boxes_opened}")
        self.unique_items_label.setText(f"Unique Items: {len(self.engine.get_inventory())}")

    def update_all_displays(self):
        self.update_mood_display()
        self.update_inventory_display() 
        self.update_stats_display()

    def reset_mood(self):
        self.engine.set_mood_value(0.0)
        self.update_mood_display()
        save_stats(self.engine.get_save_data())

    def apply_mood_adjustment(self):
        adjustment = self.mood_slider.value()
        current_mood = self.engine.get_mood_value()
        self.engine.set_mood_value(current_mood + adjustment)
        self.mood_slider.setValue(0)
        self.update_mood_display()
        save_stats(self.engine.get_save_data())

    # ---- Modular hooks for orchestrator integration ----
    def start(self):
        self.show()

    def shutdown(self):
        save_stats(self.engine.get_save_data())
        self.close()

# ---- For Standalone Launch ----

def main():
    app = QApplication(sys.argv)
    gui = CookieJarGUI()
    gui.start()
    sys.exit(app.exec())

if __name__ == "__main__":
    main()
