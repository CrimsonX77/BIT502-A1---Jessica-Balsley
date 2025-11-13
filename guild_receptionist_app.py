"""
╔═══════════════════════════════════════════════════════════════╗
║  GUILD RECEPTIONIST ARCHETYPE CREATOR v1.0                    ║
║  "Where Souls Are Divined and Adventures Begin"               ║
╚═══════════════════════════════════════════════════════════════╝

A PyQt6 application for analyzing character archetypes through
the lens of an enthusiastic anime guild receptionist.

Requirements:
    pip install PyQt6 pyyaml aiohttp
    ollama running locally with models installed
"""

import sys
import json
import yaml
import hashlib
import asyncio
from datetime import datetime, timezone
from pathlib import Path
from typing import Dict, List, Optional, Any
import traceback

from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QTabWidget, QCheckBox, QLabel, QTextEdit, QPushButton,
    QComboBox, QScrollArea, QGridLayout, QMessageBox, QDialog,
    QTableWidget, QTableWidgetItem, QHeaderView, QSlider, QLineEdit,
    QFileDialog, QProgressBar, QGroupBox, QSplitter
)
from PyQt6.QtCore import Qt, QThread, pyqtSignal, QTimer
from PyQt6.QtGui import QFont, QColor, QPalette

import aiohttp


# ═══════════════════════════════════════════════════════════════
# ARCHETYPE LENS DEFINITIONS
# ═══════════════════════════════════════════════════════════════

ARCHETYPE_LENSES = {
    "jungian": {
        "name": "Jungian Archetypes",
        "description": (
            "Classic depth psychology—universal roles and symbolic patterns as identified by Carl Jung. "
            "Focuses on internal growth, narrative arcs, and the interplay of light/shadow in the psyche."
        ),
        "archetypes": [
            # Primary Journey
            "The Hero",           # Protagonist, self-actualization quest
            "The Shadow",         # Hidden/dark self, repressed aspects, nemesis within
            "The Anima",          # Feminine principle (in men): intuition, emotion, creativity
            "The Animus",         # Masculine principle (in women): logic, will, structure
            "The Persona",        # Social mask, outward identity
            "The Self",           # Integrated wholeness, true self, unity
            # Classic 12 Archetypes (Jung + expanded)
            "The Explorer",       # Seeker, wanderer, restless for new
            "The Sage",           # Wisdom, knowledge, insight
            "The Rebel",          # Breaks rules, disrupts, transforms
            "The Magician",       # Transformation, synchronicity, vision
            "The Lover",          # Passion, connection, empathy
            "The Jester",         # Humor, joy, mischief, lightener
            "The Caregiver",      # Support, healing, nurturing
            "The Creator",        # Innovation, art, generativity
            "The Ruler",          # Leadership, order, sovereignty
            "The Innocent",       # Purity, optimism, faith
            "The Orphan",         # Outsider, abandonment, seeking belonging
            # Jungian Subtypes / Related Patterns
            "The Everyman",       # Relatable, grounded, “just like us”
            "The Warrior",        # Courage, discipline, fighting spirit
            "The Destroyer",      # Endings, sacrifice, clearing for growth
            "The Fool",           # Openness, naivety, sacred clown
            "The Child",          # New beginnings, dependency, curiosity
            "The Maiden",         # Potential, beauty, growth phase
            "The Wise Old Man",   # Mentor, sage, timeless counsel
            "The Trickster",      # Subverts, disrupts, reveals truth through mischief
            "The Outlaw",         # Marginal, rejected, finds own path
            "The Martyr",         # Sacrifice for others, suffering as meaning
            "The Pilgrim",        # Journey, spiritual search, quest for truth
            "The Alchemist"       # Seeks transformation, inner/outer change
        ],
        "analysis_focus": (
            "psychological depth, symbolic roles, shadow integration, "
            "life-stage narrative, and the dance between persona and true self."
        )
    },

    "dnd_alignment": {
        "name": "D&D Alignment Matrix",
        "description": "Lawful/Chaotic + Good/Evil moral framework",
        "archetypes": [
            "Lawful Good", "Neutral Good", "Chaotic Good",
            "Lawful Neutral", "True Neutral", "Chaotic Neutral",
            "Lawful Evil", "Neutral Evil", "Chaotic Evil"
        ],
        "analysis_focus": "moral compass, rule adherence, ethical framework"
    },
    
    "tarot_major": {
        "name": "Tarot Major Arcana",
        "description": (
            "The 22-stage heroes journey from innocence to cosmic integration. "
            "Each card is a symbol, a phase, and an archetype in both story and soul."
        ),
        "archetypes": [
            "The Fool",           # 0: Innocence, new beginnings, leap of faith, pure potential
            "The Magician",       # 1: Manifestation, willpower, resourcefulness, action
            "The High Priestess", # 2: Intuition, hidden knowledge, subconscious, mystery
            "The Empress",        # 3: Fertility, creation, nurturing, abundance, Mother Earth
            "The Emperor",        # 4: Structure, authority, leadership, discipline, the Father
            "The Hierophant",     # 5: Tradition, spiritual wisdom, institutions, teaching
            "The Lovers",         # 6: Union, choices, relationships, alignment of values
            "The Chariot",        # 7: Determination, control, victory through will, direction
            "Strength",           # 8: Inner strength, courage, resilience, gentle power
            "The Hermit",         # 9: Solitude, introspection, searching for truth, guidance
            "Wheel of Fortune",   # 10: Cycles, fate, turning points, change, destiny
            "Justice",            # 11: Fairness, law, cause and effect, truth, balance
            "The Hanged Man",     # 12: Surrender, suspension, seeing differently, sacrifice
            "Death",              # 13: Endings, transformation, release, renewal, rebirth
            "Temperance",         # 14: Balance, harmony, moderation, integration, healing
            "The Devil",          # 15: Temptation, bondage, materialism, shadow, addiction
            "The Tower",          # 16: Sudden upheaval, chaos, revelation, breakdown, awakening
            "The Star",           # 17: Hope, inspiration, faith, spiritual clarity, serenity
            "The Moon",           # 18: Illusion, dreams, intuition, confusion, subconscious
            "The Sun",            # 19: Success, vitality, joy, enlightenment, celebration
            "Judgement",          # 20: Reckoning, self-reflection, renewal, calling, absolution
            "The World"           # 21: Completion, integration, wholeness, mastery, unity
        ],
        "analysis_focus": (
            "life stage, spiritual journey, archetypal transformation, mythic cycles, "
            "narrative phase, and soul development."
        )
    },

    "anime_trope": {
        "name": "Anime Character Archetypes",
        "description": (
            "Extensive archetypes from anime, manga, and light novels—"
            "from the classic -dere personalities, to role-based, genre-defining, meta, and deconstructed types. "
            "Use for narrative pattern analysis, energy profiling, and group dynamics."
        ),
        "archetypes": [
        # Core -Dere Types
            "Tsundere", "Kuudere", "Dandere", "Yandere", "Deredere", "Himedere", "Oujidere", "Kanedere", "Bakadere", "Dorodere", "Undere",
            "Mayadere", "Sadodere", "Bokodere", "Kamidere", "Goudere", "Shundere", "Utsudere", "Nemuidere", "Shundere",
        # Protagonist / Main Cast
            "Shonen Protagonist", "Reluctant Hero", "Chosen One", "Tragic Hero", "Anti-Hero", "Brooding Anti-Hero", "Wildcard Chaos Agent",
            # Companions & Sidekicks
            "Energetic Sidekick", "Comic Relief", "Best Friend", "Straight Man (Tsukkomi)", "Silly Fool (Boke)", "Cheerful Healer",
            # Rivals & Antagonists
            "Rival", "Villain", "Anti-Villain", "Sympathetic Villain", "Redeemed Villain", "Shadow Doppelgänger", "Evil Twin",
            # Mentors & Elders
            "Mysterious Mentor", "Wise Elder", "Eccentric Teacher", "Fallen Mentor",
            # Supporting Roles
            "Gentle Giant", "Silent Stoic", "Brilliant Strategist", "Genius Prodigy", "Otaku/Nerd", "Idol/Pop Star", "Delinquent", "Rebel", "Transfer Student",
            # Supernatural & Sci-Fi
            "Magical Girl", "Magical Boy", "Magical Girlfriend/Boyfriend", "Spirit Familiar", "Cyborg/Android/Clone", "Time Traveler", "Mecha Pilot",
            # Genre-Specific
            "Samurai", "Ninja/Kunoichi", "Martial Artist", "Healer", "Inventor/Mad Scientist", "Shaman/Oracle", "Beastkin/Demi-Human", "Villager/Normie",
            # Comic/Behavioral Types
            "Ditzy Airhead", "Glasses Intellectual", "Childhood Friend", "Class President", "School Idol", "Festival Planner",
            # Tropes by Energy/Disposition
            "Genki (Hyperactive)", "Cool/Aloof", "Ice Queen/King", "Stoic Knight", "Wallflower", "Shrinking Violet", "Big Eater",
            # Meta & Deconstruction
            "Chuunibyou", "Meta-Character", "Self-Aware", "Unreliable Narrator", "Fourth Wall Breaker", "Subverted Archetype", "Deconstructed Archetype",
            # Edgy/Hybrid
            "Dark Tsundere", "Yandere-Tsundere Hybrid", "Masked Avenger", "Posthuman Entity", "Cursed Hero", "Double Agent", "Ship Tease Catalyst",
            # Utility/Structural Roles
            "Gatekeeper", "Guildmaster", "Shopkeeper", "Quest Giver", "Prophecy Voice", "Heir/Royal", "Townsfolk", "Midboss"
        ],
        "analysis_focus": (
            "Identifies interaction style, narrative function, group role, emotional signature, energy balance, "
            "character arc, and trope subversions. Supports multi-label and weighted archetype profiling."
        )
    },    
    
    "elemental_essence": {
            "name": "Elemental & Cosmic Essence",
            "description": (
                "Defines a character's fundamental energy signature—drawn from classical elements, "
                "Eastern/Western cosmology, and modern mysticism. "
                "Maps mythic, magical, and emotional resonance."
            ),
            "archetypes": [
                "Pure Fire",      # Passion, drive, transformation, destruction and renewal, willpower, fierce creativity
                "Deep Water",     # Emotion, intuition, empathy, subconscious, adaptability, flow, psychic depth
                "Solid Earth",    # Stability, endurance, grounding, reliability, physicality, patience, strength
                "Free Air",       # Intellect, logic, communication, ideas, inspiration, clarity, freedom
                "Void/Aether",    # Mystery, transcendence, spirituality, potential, cosmic connection, beyond elements
                "Lightning",      # Sudden change, breakthrough, genius, innovation, speed, chaos, divine spark
                "Ice",            # Control, preservation, discipline, clarity under pressure, distance, stasis
                "Shadow"          # Hidden depths, integration, secrets, transformation through adversity, facing the unknown
            ],
            "analysis_focus": (
                "energy type, elemental balance, magical affinity, personal resonance, "
                "cosmic signature, mythic role."
            )
        },    

        "mythic_pantheon": {
            "name": "Mythological Deity Resonance",
            "description": (
                "Discovers which gods, heroes, or cosmic beings echo through your soul—"
                "from Greco-Roman legends, Norse sagas, Egyptian mysteries, and beyond. "
                "Each archetype is a cosmic domain, a mythic energy, and a legendary path."
            ),
            "archetypes": [
                "Zeus / Jupiter",         # King of gods, thunder, law, authority—wielder of fate and cosmic order
                "Athena / Minerva",       # Wisdom, strategy, creative intellect, the guiding hand in war and peace
                "Ares / Mars",            # Warrior spirit, aggression, primal force—battle, courage, and conflict
                "Aphrodite / Venus",      # Love, beauty, sensuality, harmony—magnetism, allure, and creative spark
                "Hephaestus / Vulcan",    # The forge, craft, creation through fire, perseverance, innovation
                "Hermes / Mercury",       # Messenger, trickster, boundary-crosser, wit, travel, and divine communication
                "Apollo",                 # Sun, light, music, prophecy, clarity—vision, artistry, and healing
                "Artemis / Diana",        # Wilds, the hunt, moonlight, independence—untamed nature, purity, protector of outsiders
                "Prometheus",             # Rebel creator, sacrifice for progress, bringer of forbidden knowledge, suffering for humanity
                "Persephone",             # Queen of transitions, transformation, cyclical change, rebirth from darkness
                "Loki",                   # Chaos, shapeshifting, deconstruction, prankster energies—necessary disorder
                "Odin",                   # Knowledge seeker, wisdom at a price, runes, prophecy, the all-seeing wanderer
                # Expandable slots for more pantheons:
                "Anubis",                 # Guardian of thresholds, soul-weighing, passage between worlds
                "Isis",                   # Motherhood, magic, devotion, resurrection, hidden strength
                "Ra",                     # Solar king, renewal, illumination, source of life and cosmic rhythm
                "Thor",                   # Strength, thunder, protector, champion of the people, unyielding spirit
                "Hecate",                 # Crossroads, magic, liminality, gatekeeping, shadow wisdom
                "Morrigan",               # Fate, prophecy, battle, shape-shifting, the cycle of life and death
                "Amaterasu",              # Sun goddess, radiance, harmony, bringing light to darkness, renewal of hope
                "Susanoo",                # Storm, chaos, challenge to order, breaking limits, cleansing conflict
                "Shiva",                  # Destruction and rebirth, cosmic dance, transcendent transformation
                "Guanyin",                # Compassion, mercy, healing, unconditional support, peaceful strength
                "Coyote",                 # Trickster, teacher, folly and wisdom through mischief, evolutionary chaos
                "The World Serpent",      # Cyclicality, wholeness, boundaries and their dissolution, infinite recursion
                "Unknown / The Nameless", # Archetype of the ineffable, pure potential, the myth not yet written
            ],
            "analysis_focus": (
                "divine domain, cosmic energy, heroic flaw, mythic affinity, "
                "epic journey, and legendary resonance. Highlights both your strengths "
                "and your personal trial by myth."
            )
        },
        "heroic_mythos": {
            "name": "Heroic Mythos & Legendary Figures",
            "description": (
                "Identifies legendary heroes, tragic figures, and mythic archetypes from global lore—"
                "those whose stories have shaped cultures and echoed through time. "
                "Each archetype embodies a heroic ideal, a cautionary tale, or a transformative journey."
            ),
            "archetypes": [
                "Achilles",          # The Invincible Warrior - Strengths: unmatched combat skills, bravery; Weaknesses: fatal flaw (heel), pride
                "Odysseus",          # The Cunning Strategist - Strengths: intelligence, resourcefulness; Weaknesses: hubris, temptation
                "Hercules",         # The Strongman - Strengths: superhuman strength, courage; Weaknesses: impulsiveness, lack of foresight
                "Perseus",          # The Slayer of Monsters - Strengths: bravery, divine assistance; Weaknesses: reliance on fate, youth
                "Theseus",          # The Founder Hero - Strengths: leadership, bravery; Weaknesses: arrogance, recklessness
                "Jason",             # The Questing Leader - Strengths: charisma, determination; Weaknesses: indecision, reliance on others
                "King Arthur",       # The Noble King - Strengths: leadership, justice; Weaknesses: tragic flaws, betrayal
                "Robin Hood",        # The Outlaw Hero - Strengths: skill, charisma; Weaknesses: lawlessness, moral ambiguity
                "Beowulf",          # The Epic Warrior - Strengths: strength, honor; Weaknesses: pride, mortality
                "Gilgamesh",        # The Demigod King - Strengths: strength, leadership; Weaknesses: arrogance, quest for immortality
                "Mulan",            # The Warrior Maiden - Strengths: bravery, loyalty; Weaknesses: societal constraints, identity struggle
                "Joan of Arc",      # The Divine Messenger - Strengths: faith, leadership; Weaknesses: youth, martyrdom
                "Robin",             # The Trickster Hero - Strengths: cleverness, adaptability; Weaknesses: deceit, lack of reliability
                "Cú Chulainn",      # The Hound of Ulster - Strengths: combat prowess, loyalty; Weaknesses: rage, tragic destiny
                "Sigurd",           # The Dragon Slayer - Strengths: bravery, skill; Weaknesses: fate, hubris
                "Lancelot",         # The Tragic Knight - Strengths: combat skill, loyalty; Weaknesses: forbidden love, betrayal
                "Tristan",          # The Romantic Knight - Strengths: bravery, passion; Weaknesses: tragic love, loyalty conflict
                "Hiawatha",         # The Peacemaker - Strengths: diplomacy, vision; Weaknesses: idealism, cultural conflict
                "Rama",             # The Virtuous Prince - Strengths: righteousness, skill; Weaknesses: exile, duty
                "Arjuna",           # The Warrior Prince - Strengths: skill, devotion; Weaknesses: doubt, moral conflict
                "Hercules",         # The Strongman - Strengths: superhuman strength, courage; Weaknesses: impulsiveness, lack of foresight
                "Siegfried",        # The Dragon Slayer - Strengths: bravery, skill; Weaknesses: fate, hubris
                "The Unknown Hero"   # The Everyman - Strengths: relatability, potential; Weaknesses: ordinariness, lack of distinction
            ],
            "analysis_focus": (
                "heroic ideal, tragic flaw, transformative journey, cultural resonance, "
                "mythic symbolism, and legendary impact."
            )
        },
        "female_archetypes": {
            "name": "Female Divine & Heroic Archetypes",
            "description": (
                "Powerful feminine archetypes from mythology and legend—"
                "goddesses, heroines, and archetypal feminine roles representing "
                "different aspects of feminine power, wisdom, and transformation."
            ),
            "archetypes": [
                "Athena",           # The Wise Mentor - Strengths: wisdom, strategy; Weaknesses: aloofness, over-caution
                "Artemis",          # The Huntress - Strengths: independence, agility; Weaknesses: isolation, vengeance
                "Demeter",          # The Nurturing Mother - Strengths: fertility, compassion; Weaknesses: possessiveness, grief
                "Persephone",      # The Duality of Life - Strengths: adaptability, resilience; Weaknesses: naivety, conflict
                "Freya",           # The Warrior Goddess - Strengths: beauty, combat skill; Weaknesses: vanity, impulsiveness
                "Morrigan",        # The Fate Weaver - Strengths: foresight, cunning; Weaknesses: manipulation, darkness
                "Bastet",          # The Protector - Strengths: loyalty, ferocity; Weaknesses: territoriality, jealousy
                "Kali",            # The Destroyer - Strengths: transformation, power; Weaknesses: chaos, fear
                "Isis",            # The Healer - Strengths: magic, knowledge; Weaknesses: vulnerability, obsession
                "Brigid",          # The Flame Keeper - Strengths: inspiration, creativity; Weaknesses: distraction, impatience
            ],
            "analysis_focus": (
                "feminine power, goddess energy, transformative journey, cultural resonance, "
                "mythic symbolism, and archetypal feminine roles."
            )
        },
        "shadow_archetypes": {
            "name": "Shadow & Transgressive Archetypes",
            "description": (
                "The forbidden, the fallen, the taboo—archetypes that exist in moral grey zones, "
                "representing humanity's complex relationship with desire, power, corruption, and redemption. "
                "These are the archetypes society whispers about but secretly recognizes."
            ),
            "archetypes": [
                # Sacred & Profane
                "The Whore",              # Sacred sexuality, transgression, commodified intimacy, power through desire
                "The Virgin",             # Untouched potential, purity, protected innocence, idealized perfection
                "The Magdalene",          # Fallen woman redeemed, sacred prostitute, transformation through love
                "The Seductress",         # Temptation incarnate, manipulation through desire, dangerous allure
                "The Concubine",          # Kept woman, gilded cage, beauty as currency, power through submission
                
                # Divine Corruption
                "The Fallen Angel",       # Divine nature corrupted, beauty twisted by pride, grace lost to rebellion
                "The Arrogant Angel",     # Celestial being drunk on power, divine authority gone wrong
                "The Lost Demon",         # Infernal being seeking redemption, darkness yearning for light
                "The Corrupted Saint",    # Holy person fallen from grace, virtue turned to vice
                "The False Prophet",      # Divine messenger with twisted agenda, spiritual authority corrupted
                "The Blasphemer",         # One who speaks against the sacred, challenger of divine order
                
                # Moral Outcasts
                "The Pariah",             # Social outcast, untouchable, rejected by society, marked as other
                "The Scapegoat",          # Bearer of collective guilt, blamed for society's sins
                "The Exile",              # Banished wanderer, cut off from home, perpetual outsider
                "The Bastard",            # Illegitimate child, born outside social order, fighting for recognition
                "The Apostate",           # One who abandons faith, religious rebel, spiritual turncoat
                "The Heretic",            # Challenger of orthodox belief, dangerous thinker, subversive truth-teller
                
                # Power & Corruption
                "The Tyrant",             # Absolute power corrupted, ruler become monster, order through oppression
                "The Despot",             # Petty dictator, small-scale tyranny, power over the powerless
                "The Usurper",            # Throne-stealer, illegitimate ruler, power through betrayal
                "The Puppet Master",      # Hidden controller, power through manipulation, strings in the shadows
                "The Kingmaker",          # Power behind the throne, influence without responsibility
                "The War Profiteer",      # One who gains from conflict, merchant of death, chaos for profit
                
                # Addiction & Compulsion
                "The Addict",             # Slave to substance or compulsion, self-destruction incarnate
                "The Glutton",            # Insatiable appetite, consumption without end, desire made flesh
                "The Gambler",            # Risk addiction, fortune's fool, chance as religion
                "The Collector",          # Obsessive accumulator, hoarder of objects or experiences
                "The Perfectionist",      # Paralyzed by impossible standards, excellence as prison
                
                # Violence & Darkness
                "The Executioner",        # Dealer of death, necessary evil, justice through violence
                "The Torturer",           # Inflicts suffering, power through pain, darkness given purpose
                "The Assassin",           # Death in the shadows, killer for hire, violence as profession
                "The Berserker",          # Rage incarnate, controlled by fury, destruction without thought
                "The Sadist",             # Pleasure in others' pain, cruelty as entertainment
                "The Masochist",          # Pleasure in own pain, suffering as transcendence
                
                # Madness & Obsession
                "The Mad Scientist",      # Knowledge without ethics, progress without conscience
                "The Fanatic",            # Extremism incarnate, cause above all else, blind devotion
                "The Obsessed",           # Single-minded pursuit, tunnel vision, goal as everything
                "The Paranoid",           # Suspicious of all, isolated by fear, conspiracy as worldview
                "The Nihilist",           # Believer in nothing, destroyer of meaning, void as philosophy
                
                # Transformation Through Transgression
                "The Redeemed Villain",   # Darkness turned to light, transformation through suffering
                "The Noble Criminal",     # Criminal with code, illegal but ethical, law vs justice
                "The Gentleman Thief",    # Theft as art form, crime with style, rebellion with class
                "The Vigilante",          # Justice outside law, personal code above society
                "The Anti-Hero",          # Heroic ends through dark means, flawed savior
                
                # Cosmic & Mythic Darkness
                "The Void Walker",        # One who traverses nothingness, darkness as home
                "The Soul Eater",         # Consumer of essence, spiritual predator
                "The Dream Stealer",      # Thief of hopes and aspirations, destroyer of potential
                "The Memory Thief",       # Stealer of past, eraser of identity
                "The Time Corrupted",     # Twisted by temporal power, causality as plaything
                "The Reality Breaker",    # One who shatters truth, underminer of certainty
                
                # The Ultimately Fallen
                "The Damned",             # Beyond redemption, lost to all hope
                "The Cursed",             # Bound by supernatural punishment, fate as prison
                "The Possessed",          # Vessel for other will, self lost to invasion
                "The Hollowed",           # Emptied of essence, shell of former self
                "The Broken"              # Shattered beyond repair, pieces of what once was
            ],
            "analysis_focus": (
                "moral complexity, shadow integration, transgressive appeal, redemption potential, "
                "societal taboos, power dynamics, and the dark mirror of virtue."
            )
        },
        
        "divine_court_archetypes": {
            "name": "Divine Court & Celestial Hierarchy",
            "description": (
                "Archetypes from celestial realms—angels, demons, deities, and cosmic beings "
                "representing different aspects of divine nature, spiritual power, and cosmic order."
            ),
            "archetypes": [
                # Celestial Hierarchy
                "The Seraph",             # Highest angel, pure fire, closest to divine source
                "The Cherub",             # Winged guardian, protector of sacred knowledge
                "The Archangel",          # Divine warrior, messenger of god's will
                "The Guardian Angel",     # Personal protector, guide through mortal realm
                "The Recording Angel",    # Keeper of deeds, divine accountant, cosmic memory
                "The Angel of Death",     # Psychopomp, guide between worlds, ending as beginning
                "The Fallen Angel",       # Cast out from grace, divine exile, corrupted beauty
                "The Questioning Angel",  # Doubter of divine plan, celestial philosopher
                
                # Infernal Court
                "The Archdemon",          # Prince of hell, master of sin domain
                "The Tempter Demon",      # Corruptor of souls, speaker of sweet lies
                "The Rage Demon",         # Incarnation of wrath, fury given form
                "The Seduction Demon",    # Master of desire, lust made manifest
                "The Pride Demon",        # Avatar of arrogance, vanity incarnate
                "The Despair Demon",      # Bringer of hopelessness, soul-crusher
                "The Trickster Demon",    # Chaos-bringer, supernatural prankster
                "The Lost Demon",         # Seeking redemption, darkness yearning for light
                
                # Divine Roles
                "The Creator God",        # Prime mover, source of all existence
                "The Destroyer God",      # Ender of cycles, necessity of endings
                "The Trickster God",      # Divine chaos agent, necessary disruption
                "The War God",            # Conflict incarnate, battle as sacred act
                "The Love Goddess",       # Romance and passion divine, heart's ruler
                "The Wisdom God",         # Divine intellect, cosmic knowledge keeper
                "The Death God",          # Ruler of endings, master of final mysteries
                "The Forgotten God",      # Lost deity, abandoned divinity, faded power
                
                # Cosmic Forces
                "The Void Lord",          # Ruler of nothingness, master of entropy
                "The Time Lord",          # Master of causality, temporal sovereignty
                "The Fate Weaver",        # Spinner of destiny, cosmic pattern-maker
                "The Chaos Bringer",      # Agent of randomness, order's necessary opposite
                "The Balance Keeper",     # Maintainer of cosmic equilibrium
                "The World Builder",      # Creator of realities, cosmic architect
                "The Soul Judge",         # Weigher of hearts, cosmic justice incarnate
                "The Dream Maker",        # Weaver of sleeping visions, unconscious navigator
                
                # Primordial Beings
                "The First Light",        # Original illumination, dawn of consciousness
                "The Primal Darkness",    # Original void, source of mystery
                "The Earth Mother",       # Primordial fertility, life's first stirring
                "The Sky Father",         # Cosmic patriarch, order from above
                "The World Serpent",      # Cosmic cycle, eternal return, ouroboros
                "The Phoenix",            # Death and rebirth, transformation eternal
                "The Leviathan",          # Primordial chaos, untamed cosmic force
                "The Tree of Life",       # Cosmic connection, all existence unified
            ],
            "analysis_focus": (
                "divine nature, cosmic role, spiritual power, moral alignment, "
                "celestial hierarchy, and relationship to ultimate reality."
            )
        },
        
        "male_archetypes": {
            "name": "Male Heroic Archetypes",
            "description": (
                "Classic male heroic figures from mythology, legend, and literature—"
                "exploring the heroic journey through masculine archetypal patterns."
            ),
            "archetypes": [
                "Odysseus",         # The Cunning Strategist - Strengths: intelligence, resourcefulness; Weaknesses: hubris, temptation
                "Hercules",         # The Strongman - Strengths: superhuman strength, courage; Weaknesses: impulsiveness, lack of foresight
                "Perseus",          # The Slayer of Monsters - Strengths: bravery, divine assistance; Weaknesses: reliance on fate, youth
                "Theseus",          # The Founder Hero - Strengths: leadership, bravery; Weaknesses: arrogance, recklessness
                "Jason",             # The Questing Leader - Strengths: charisma, determination; Weaknesses: indecision, reliance on others
                "King Arthur",       # The Noble King - Strengths: leadership, justice; Weaknesses: tragic flaws, betrayal
                "Robin Hood",        # The Outlaw Hero - Strengths: skill, charisma; Weaknesses: lawlessness, moral ambiguity
                "Beowulf",          # The Epic Warrior - Strengths: strength, honor; Weaknesses: pride, mortality
                "Gilgamesh",        # The Demigod King - Strengths: strength, leadership; Weaknesses: arrogance, quest for immortality
                "Mulan",            # The Warrior Maiden - Strengths: bravery, loyalty; Weaknesses: societal constraints, identity struggle
                "Joan of Arc",      # The Divine Messenger - Strengths: faith, leadership; Weaknesses: youth, martyrdom
                "Robin",             # The Trickster Hero - Strengths: cleverness, adaptability; Weaknesses: deceit, lack of reliability
                "Cú Chulainn",      # The Hound of Ulster - Strengths: combat prowess, loyalty; Weaknesses: rage, tragic destiny
                "Sigurd",           # The Dragon Slayer - Strengths: bravery, skill; Weaknesses: fate, hubris
                "Lancelot",         # The Tragic Knight - Strengths: combat skill, loyalty; Weaknesses: forbidden love, betrayal
                "Tristan",          # The Romantic Knight - Strengths: bravery, passion; Weaknesses: tragic love, loyalty conflict
                "Hiawatha",         # The Peacemaker - Strengths: diplomacy, vision; Weaknesses: idealism, cultural conflict
                "Rama",             # The Virtuous Prince - Strengths: righteousness, skill; Weaknesses: exile, duty
                "Arjuna",           # The Warrior Prince - Strengths: skill, devotion; Weaknesses: doubt, moral conflict
                "Siegfried",        # The Dragon Slayer - Strengths: bravery, skill; Weaknesses: fate, hubris
                "The Unknown Hero", # The Everyman - Strengths: relatability, potential; Weaknesses: ordinariness, lack of distinction
                
                # Dark Masculine Archetypes
                "The Destroyer",    # Endings, sacrifice, clearing for growth, necessary destruction
                "The Conqueror",    # Domination, expansion, taking what is desired through force
                "The Tyrant",       # Absolute power, control through fear, order through oppression
                "The Seducer",      # Charm as weapon, manipulation through desire, conquest of hearts
                "The Wanderer",     # Eternal outsider, never settling, always moving beyond
                "The Hermit",       # Solitary wisdom, withdrawal from world, inner journey
                "The Fool",         # Sacred idiot, wisdom through innocence, disruption of order
                "The Jester",       # Truth through humor, wisdom through folly, court entertainer
                "The Rebel",        # Overthrows old order, chaos agent, necessary revolution
                "The Outlaw",       # Lives outside law, creates own rules, moral vigilante
                
                # Power & Authority
                "The King",         # Rightful ruler, sovereign power, natural leadership
                "The Emperor",      # Absolute authority, cosmic order, divine right
                "The Judge",        # Discerner of truth, weigher of souls, divine justice
                "The Executioner",  # Necessary death, final judgment, ending as service
                "The Warlord",      # Military might, conquest through strategy, warrior leader
                "The General",      # Strategic mind, battlefield genius, war as art
                "The Champion",     # Fighting for others, skill in service, noble combat
                "The Gladiator",    # Entertainment through combat, death as spectacle
                
                # Wisdom & Knowledge
                "The Wizard",       # Arcane knowledge, reality manipulation, cosmic understanding
                "The Scholar",      # Pursuit of truth, knowledge for its own sake, academic devotion
                "The Alchemist",    # Transformation seeker, turning base to gold, inner change
                "The Prophet",      # Divine messenger, future sight, warning voice
                "The Oracle",       # Cosmic knowledge, divine communication, mystical wisdom
                "The Sage",         # Accumulated wisdom, life experience, guiding elder
                "The Teacher",      # Knowledge transmitter, wisdom sharer, student developer
                "The Monk",         # Spiritual discipline, ascetic wisdom, renunciation of world
                
                # Creation & Art
                "The Artist",       # Beauty creator, aesthetic vision, creative expression
                "The Poet",         # Word weaver, emotion sculptor, linguistic artist
                "The Musician",     # Sound sculptor, emotional resonance, harmonic creation
                "The Builder",      # Physical creation, making the permanent, architectural vision
                "The Craftsman",    # Skill perfection, mastery of tools, patient creation
                "The Inventor",     # Innovation, new solutions, technological advancement
                
                # Shadow & Darkness
                "The Sinner",       # Embracer of transgression, moral boundary crosser
                "The Damned",       # Beyond redemption, lost soul, eternal punishment
                "The Fallen",       # Grace lost, heights descended from, corruption's victim
                "The Cursed",       # Bound by fate, supernatural punishment, tragic destiny
                "The Possessed",    # Vessel for other will, loss of self-control
                "The Mad",          # Sanity lost, reality fractured, chaos minded
                "The Broken",       # Shattered by life, spirit destroyed, hope abandoned
                "The Empty",        # Hollowed out, essence drained, shell remaining
            ],
            "analysis_focus": (
                "masculine energy, heroic journey, power dynamics, moral complexity, "
                "leadership patterns, shadow integration, and archetypal masculine roles."
            )
        },
        
        "modern_archetypes": {
            "name": "Modern & Contemporary Archetypes",
            "description": (
                "Archetypes born from modern life—technology, urban existence, consumer culture, "
                "and contemporary social dynamics. These represent new mythic patterns emerging in our digital age."
            ),
            "archetypes": [
                # Digital Age
                "The Hacker",           # Digital rebel, system breaker, electronic trickster
                "The Influencer",       # Social media power, attention economy, digital celebrity
                "The Streamer",         # Performance for audience, life as entertainment
                "The Gamer",            # Virtual world dweller, digital competition, escapism
                "The Blogger",          # Opinion shaper, information curator, digital voice
                "The YouTuber",         # Content creator, digital entrepreneur, fame seeker
                "The Podcaster",        # Voice in the void, intimate strangers, audio intimacy
                "The Social Media Addict", # Validation seeker, digital dopamine chaser
                "The Digital Nomad",    # Location independent, technology enabled wanderer
                "The Tech Bro",         # Silicon Valley stereotype, disruption worship
                "The AI Prompt Engineer", # Human-machine interface, digital whisperer
                "The Crypto Evangelist", # Blockchain believer, decentralized future prophet
                
                # Urban Life
                "The Hipster",          # Ironic detachment, authenticity through contrast
                "The Startup Founder",  # Entrepreneurial dreamer, risk-taking innovator
                "The Burnout",          # Exhausted achiever, success as poison
                "The Workaholic",       # Identity through labor, productivity worship
                "The Life Coach",       # Professional optimizer, self-improvement seller
                "The Wellness Guru",    # Health evangelist, body-mind harmony preacher
                "The Minimalist",       # Less is more, simplicity seeker, possession rejector
                "The Urban Shaman",     # Modern mysticism, ancient wisdom in concrete jungle
                "The Coffee Shop Regular", # Third space dweller, caffeine-fueled thinker
                "The Uber Driver",      # Gig economy survivor, temporary connections
                "The Food Blogger",     # Aesthetic experience documenter, taste curator
                "The Fitness Influencer", # Body transformation seller, motivation commodity
                
                # Consumer Culture
                "The Brand Evangelist", # Corporate loyalty incarnate, product identity
                "The Collector",        # Accumulation obsessed, possession through acquisition
                "The Shopaholic",       # Consumption as therapy, buying for emotional void
                "The Reseller",         # Arbitrage artist, profit from others' desires
                "The Reviewer",         # Opinion economy participant, taste arbiter
                "The Early Adopter",    # Technology pioneer, trend setter, innovation embracer
                "The Prepper",          # Collapse anticipator, self-reliance extremist
                "The Conspiracy Theorist", # Alternative reality believer, hidden truth seeker
                
                # Mental Health Era
                "The Therapy Client",   # Self-improvement seeker, emotional work practitioner
                "The Self-Help Addict", # Constant optimization, perpetual improvement seeker
                "The Anxiety Person",   # Modern stress incarnate, worry as lifestyle
                "The Depression Warrior", # Mental health advocate, darkness fighter
                "The Trauma Survivor",  # Pain transformer, resilience embodiment
                "The Neurodivergent",   # Different brain, alternative processing, unique perspective
                "The Empath",           # Emotional sponge, feeling absorber, psychic sensitive
                "The Introvert",        # Energy conservator, solitude seeker, inner focused
                "The People Pleaser",   # Approval addict, conflict avoider, self-sacrifice pattern
                
                # Identity Politics Era
                "The Activist",         # Change agent, social justice warrior, cause fighter
                "The Ally",             # Supportive outsider, privilege checker, solidarity practitioner
                "The Canceled",         # Social exile, digital punishment recipient
                "The Virtue Signaler",  # Moral performance artist, righteousness displayer
                "The Troll",            # Digital provocateur, chaos entertainment, anonymous aggressor
                "The Karen",            # Entitlement incarnate, manager demander, privilege wielder
                "The Incel",            # Romantic rejection, entitlement frustrated, anger isolated
                "The Simp",             # Devotion unrequited, digital age courtly love
                "The Chad",             # Alpha stereotype, confidence incarnate, success assumed
                "The Femboy",           # Gender boundary blurrer, soft masculinity, aesthetic androgyny
                
                # Pandemic Era
                "The Remote Worker",    # Home office dweller, digital commuter, isolation professional
                "The Quarantine Creator", # Lockdown productivity, constraint inspiration
                "The Doomscroller",     # News addiction, catastrophe consumer, anxiety feeder
                "The Zoom Fatigue Victim", # Digital exhaustion, screen interaction burned out
                "The Mask Compliant",   # Rule follower, safety prioritizer, collective responsibility
                "The Mask Rebel",       # Freedom fighter, individual liberty, rule resistor
                "The Vaccine Evangelist", # Science follower, public health advocate
                "The Vaccine Skeptic",  # Authority questioner, bodily autonomy defender
                "The Social Distance Hermit", # Isolation embracer, contact avoider
            ],
            "analysis_focus": (
                "contemporary adaptation, technology relationship, social media presence, "
                "consumer behavior, mental health awareness, and modern identity formation."
            )
        },
        
        "bayesian_probability": {
            "name": "Bayesian Future-Sight Lens",
            "description": "Statistical prophecy based on your archetype trajectory",
            "archetypes": [
                "Convergent Certainty (95% confidence)",
                "Divergent Possibility (high variance)",
                "Schrödinger's Self (superposition state)",
                "Markov Chain Wanderer (state-dependent)",
                "Monte Carlo Maverick (simulation-optimized)"
            ],
            "analysis_focus": "trend prediction, probability distributions, future archetype forecasting",
            "special": True
        },
    }


CHARACTER_FIELDS = {
    "personality": {
        "name": "Personality Traits",
        "fields": [
            "Resilient", "Empathetic", "Creative", "Mischievous", "Determined",
            "Analytical", "Chaotic", "Loyal", "Brooding", "Optimistic",
            "Intense", "Playful", "Mysterious", "Energetic", "Stoic",
            "Compassionate", "Rebellious", "Disciplined", "Spontaneous", "Cautious",
            "Ambitious", "Humble", "Bold", "Reserved", "Passionate",
            "Rational", "Intuitive", "Protective", "Independent", "Collaborative",
            "Philosophical", "Pragmatic", "Idealistic", "Cynical", "Hopeful",
            "Patient", "Impulsive", "Calculating", "Emotional", "Detached",
            "Generous", "Selfish", "Confident", "Insecure", "Arrogant",
            "Curious", "Content", "Restless", "Peaceful", "Turbulent"
        ]
    },
    
    "physical": {
        "name": "Physical Descriptors",
        "fields": [
            "Tall", "Short", "Average Height", "Muscular", "Lean",
            "Curvy", "Athletic", "Slender", "Stocky", "Graceful",
            "Long Hair", "Short Hair", "Bald", "Curly Hair", "Straight Hair",
            "Wavy Hair", "Braided Hair", "Wild Hair", "Elegant Hair", "Practical Hair",
            "Fair Skin", "Tan Skin", "Dark Skin", "Pale Skin", "Scarred Skin",
            "Tattooed", "Pierced", "Bearded", "Clean Shaven", "Distinctive Features",
            "Bright Eyes", "Dark Eyes", "Heterochromic Eyes", "Intense Gaze", "Soft Expression",
            "Strong Jaw", "Delicate Features", "Sharp Features", "Rounded Features", "Weathered",
            "Youthful", "Aged", "Timeless", "Intimidating Presence", "Approachable Demeanor",
            "Elegant Posture", "Casual Stance", "Warrior Build", "Dancer Physique", "Scholar Bearing"
        ]
    },
    
    "background": {
        "name": "Background & Experience",
        "fields": [
            "Noble Birth", "Common Origin", "Street Urchin", "Scholarly Upbringing", "Military Training",
            "Artistic Background", "Religious Education", "Self-Taught", "Apprenticeship", "Isolated Childhood",
            "Traumatic Past", "Peaceful History", "Adventure-Filled", "Sheltered Life", "Worldly Experience",
            "Lost Family", "Large Family", "Orphaned", "Adopted", "Royal Lineage",
            "Criminal Past", "Heroic Legacy", "Mysterious Origins", "Prophesied Birth", "Unremarkable History",
            "Master Craftsman", "Wanderer", "Former Soldier", "Ex-Noble", "Rising Star",
            "Fallen from Grace", "Seeking Redemption", "On a Quest", "Retired Adventurer", "Reluctant Hero",
            "Chosen One", "Outcast", "Beloved by Many", "Feared by Some", "Unknown Entity",
            "Time Traveler", "Dimension Walker", "Cursed Being", "Blessed Soul", "Ordinary Turned Extraordinary"
        ]
    },
    
    "values": {
        "name": "Core Values & Beliefs",
        "fields": [
            "Justice", "Freedom", "Loyalty", "Honor", "Compassion",
            "Power", "Knowledge", "Love", "Truth", "Beauty",
            "Order", "Chaos", "Balance", "Growth", "Tradition",
            "Innovation", "Family", "Community", "Self", "Duty",
            "Pleasure", "Suffering", "Transcendence", "Materialism", "Spirituality",
            "Revenge", "Forgiveness", "Ambition", "Contentment", "Excellence",
            "Survival", "Sacrifice", "Independence", "Unity", "Diversity",
            "Strength", "Wisdom", "Courage", "Faith", "Doubt",
            "Hope", "Despair", "Creation", "Destruction", "Transformation"
        ]
    },
    
    "essence": {
        "name": "Essence & Philosophy",
        "fields": [
            "Light Bearer", "Shadow Walker", "Balance Seeker", "Chaos Embracer", "Order Enforcer",
            "Life Giver", "Death Bringer", "Time Manipulator", "Space Bender", "Reality Weaver",
            "Dream Shaper", "Nightmare Haunter", "Memory Keeper", "Future Seer", "Present Focused",
            "Cosmic Wanderer", "Earth Bound", "Sky Dancer", "Ocean Deep", "Fire Spirit",
            "Ice Heart", "Thunder Soul", "Wind Rider", "Stone Steady", "Void Touched",
            "Divine Chosen", "Demonic Pact", "Fey Blessed", "Dragon Kin", "Beast Soul",
            "Machine Mind", "Nature Spirit", "Urban Dweller", "Wilderness Born", "Otherworldly",
            "Dualist", "Monist", "Nihilist", "Optimist", "Realist",
            "Existentialist", "Absurdist", "Stoic", "Epicurean", "Ascetic",
            "Hedonist", "Utilitarian", "Deontologist", "Virtue Ethicist", "Relativist"
        ]
    }
}


# ═══════════════════════════════════════════════════════════════
# MEMORY SYSTEM
# ═══════════════════════════════════════════════════════════════

class AdventurerMemory:
    """Tiered memory system for efficient context management"""
    
    def __init__(self, sigil: str):
        self.sigil = sigil
        self.entries: List[Dict] = []
        
    def add_entry(self, analysis_result: Dict, event_type: str = "archetype_analysis", 
                  narrative_tag: str = ""):
        """Add a versioned soul shard entry"""
        entry = {
            "shard_version": len(self.entries) + 1,
            "event_type": event_type,
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "analysis": analysis_result,
            "narrative_tag": narrative_tag
        }
        self.entries.append(entry)
        
    def get_context_window(self) -> List[Dict]:
        """Smart memory sampling using tiered architecture"""
        n = len(self.entries)
        
        if n == 0:
            return []
        
        context = []
        
        # Tier 1: Last 10 (immediate recall)
        recent = self.entries[-10:]
        context.extend(recent)
        
        # Tier 2: Middle cache (40-60 range)
        if n > 60:
            middle_cache = self.entries[39:60]
            context.extend(middle_cache)
        elif n > 40:
            middle_cache = self.entries[39:max(10, n-10)]
            context.extend(middle_cache)
        
        # Tier 3: Century marker (3 either side of 100th)
        if n > 103:
            century_sample = self.entries[97:104]
            context.extend(century_sample)
        
        # Tier 4: Deep history with exponential decay
        if n > 120:
            sample_points = []
            current = 120
            decay_rate = 1.24
            
            while current < n - 103:
                sample_points.append(int(current))
                current *= decay_rate
            
            for idx in sample_points[:5]:
                if idx < n - 103:
                    context.append(self.entries[idx])
        
        # Remove duplicates while preserving order
        seen = set()
        unique_context = []
        for entry in context:
            entry_id = entry.get('timestamp', id(entry))
            if entry_id not in seen:
                seen.add(entry_id)
                unique_context.append(entry)
        
        return unique_context
    
    def export_soul(self) -> Dict:
        """Export memory with integrity check"""
        data = {
            'sigil': self.sigil,
            'entries': self.entries,
            'export_date': datetime.now(timezone.utc).isoformat(),
            'version': '1.0'
        }
        
        content_hash = hashlib.sha256(
            json.dumps(data, sort_keys=True).encode()
        ).hexdigest()
        
        data['integrity_hash'] = content_hash
        return data
    
    @staticmethod
    def import_soul(data: Dict) -> 'AdventurerMemory':
        """Import memory with integrity verification"""
        claimed_hash = data.pop('integrity_hash')
        actual_hash = hashlib.sha256(
            json.dumps(data, sort_keys=True).encode()
        ).hexdigest()
        
        if claimed_hash != actual_hash:
            raise ValueError("Soul corruption detected! Integrity check failed.")
        
        memory = AdventurerMemory(data['sigil'])
        memory.entries = data['entries']
        return memory


# ═══════════════════════════════════════════════════════════════
# RECEPTIONIST MOODLET SYSTEM
# ═══════════════════════════════════════════════════════════════

class ReceptionistMood:
    """Tracks receptionist's mood based on time, events, and user behavior"""
    
    def __init__(self):
        self.base_energy = 100
        self.base_sass = 50
        self.base_enthusiasm = 90
        
    def calculate_mood(self, current_time: datetime, user_streak: int, 
                      rare_events: List[str]) -> Dict[str, Any]:
        """Calculate current mood modifiers"""
        mood = {
            'energy': self.base_energy,
            'sass_level': self.base_sass,
            'enthusiasm': self.base_enthusiasm,
            'mystical_insight': 100,
            'dialogue_flavor': 'standard'
        }
        
        hour = current_time.hour
        
        # Late night/early morning (12 AM - 5 AM)
        if 0 <= hour <= 4:
            mood['energy'] -= 20
            mood['sass_level'] += 15
            mood['dialogue_flavor'] = 'sleepy_teasing'
        
        # Peak hours (2 PM - 6 PM)
        elif 14 <= hour <= 18:
            mood['enthusiasm'] += 10
            mood['energy'] += 10
            mood['dialogue_flavor'] = 'peak_energy'
        
        # User streak bonuses
        if user_streak > 100:
            mood['devotion'] = 200
            mood['dialogue_flavor'] = 'deeply_attached'
        elif user_streak > 50:
            mood['enthusiasm'] += 20
            mood['dialogue_flavor'] = 'proud_mentor'
        elif user_streak > 10:
            mood['enthusiasm'] += 10
        
        # Rare events
        if 'full_moon' in rare_events:
            mood['mystical_insight'] = 150
            mood['dialogue_flavor'] = 'cosmic_prophetic'
        
        if 'first_visit' in rare_events:
            mood['enthusiasm'] = 150
            mood['dialogue_flavor'] = 'welcoming_excited'
        
        return mood


# ═══════════════════════════════════════════════════════════════
# OLLAMA INTEGRATION
# ═══════════════════════════════════════════════════════════════

class OllamaClient:
    """Async Ollama API client"""
    
    def __init__(self, base_url: str = "http://localhost:11434"):
        self.base_url = base_url
        
    async def chat(self, model: str, messages: List[Dict], 
                   system: str = "") -> Dict:
        """Send chat completion request"""
        url = f"{self.base_url}/api/chat"
        
        payload = {
            "model": model,
            "messages": messages,
            "stream": False
        }
        
        if system:
            payload["messages"].insert(0, {
                "role": "system",
                "content": system
            })
        
        async with aiohttp.ClientSession() as session:
            async with session.post(url, json=payload) as response:
                if response.status == 200:
                    return await response.json()
                else:
                    raise Exception(f"Ollama API error: {response.status}")
    
    async def list_models(self) -> List[Dict]:
        """List available Ollama models"""
        url = f"{self.base_url}/api/tags"
        
        async with aiohttp.ClientSession() as session:
            async with session.get(url) as response:
                if response.status == 200:
                    data = await response.json()
                    return data.get('models', [])
                else:
                    return []


# ═══════════════════════════════════════════════════════════════
# GUILD RECEPTIONIST BRAIN
# ═══════════════════════════════════════════════════════════════

class GuildReceptionist:
    """The heart of the system - analysis and character response"""
    
    def __init__(self, analyzer_model: str = "llama3", 
                 receptionist_model: str = "llama3"):
        self.analyzer_model = analyzer_model
        self.receptionist_model = receptionist_model
        self.ollama = OllamaClient()
        self.mood_system = ReceptionistMood()
        
    def analyze_persona_complexity(self, persona_data: Dict) -> Dict:
        """Analyze persona to recommend best model"""
        traits_count = sum(len(fields) for fields in persona_data.values() 
                          if isinstance(fields, list))
        
        custom_text_length = len(persona_data.get('custom_inputs', {}).get('all', ''))
        
        has_complex_philosophy = len(persona_data.get('essence', [])) > 5
        has_detailed_physical = len(persona_data.get('physical', [])) > 10
        
        complexity = 'high' if traits_count > 100 else 'medium' if traits_count > 50 else 'low'
        
        return {
            'complexity': complexity,
            'trait_count': traits_count,
            'text_heaviness': custom_text_length,
            'philosophy_depth': has_complex_philosophy,
            'detail_oriented': has_detailed_physical
        }
    
    def build_analysis_prompt(self, persona_data: Dict, lens: str, 
                             lens_weights: Dict[str, float]) -> str:
        """Construct analysis prompt for Ollama"""
        lens_info = ARCHETYPE_LENSES.get(lens, ARCHETYPE_LENSES['jungian'])
        
        # Build weighted lens instruction
        weight_text = ""
        if lens_weights:
            weight_text = "\n\nLENS WEIGHT BLEND:\n"
            for lens_name, weight in lens_weights.items():
                if weight > 0:
                    lens_data = ARCHETYPE_LENSES.get(lens_name, {})
                    weight_text += f"- {lens_data.get('name', lens_name)}: {weight*100:.0f}%\n"
        
        prompt = f"""Analyze this character through the **{lens_info['name']}** lens.

LENS DESCRIPTION: {lens_info['description']}
ANALYSIS FOCUS: {lens_info['analysis_focus']}
{weight_text}

CHARACTER DATA:
{json.dumps(persona_data, indent=2)}

Provide a structured analysis with:
1. PRIMARY ARCHETYPE (from the lens archetypes list)
2. SECONDARY ARCHETYPE (if applicable)
3. CORE ATTRIBUTES (with percentage scores)
4. MYTHIC RESONANCE (symbolic connections)
5. ELEMENTAL AFFINITY (energy type)
6. BRIEF ARCHETYPE DESCRIPTION (2-3 sentences)

Return your analysis in this JSON format:
{{
    "primary_archetype": "...",
    "secondary_archetype": "...",
    "core_attributes": {{
        "Creativity": 85,
        "Loyalty": 92,
        "Chaos Affinity": 78
    }},
    "mythic_resonance": "...",
    "elemental_affinity": "...",
    "description": "..."
}}

CRITICAL: Return ONLY valid JSON. No explanations, no markdown, no extra text. Your response must start with {{ and end with }}."""

        return prompt
    
    def attempt_json_repair(self, response_text: str) -> str:
        """Attempt to repair common JSON formatting issues"""
        # Remove common prefixes/suffixes
        response_text = response_text.strip()
        
        # Remove markdown code blocks
        if response_text.startswith('```json'):
            response_text = response_text[7:].strip()
        elif response_text.startswith('```'):
            response_text = response_text[3:].strip()
        
        if response_text.endswith('```'):
            response_text = response_text[:-3].strip()
        
        # Find JSON boundaries
        start_idx = response_text.find('{')
        end_idx = response_text.rfind('}')
        
        if start_idx != -1 and end_idx != -1 and end_idx > start_idx:
            response_text = response_text[start_idx:end_idx+1]
        
        # Fix common JSON issues
        response_text = response_text.replace('\n', ' ')  # Remove newlines
        response_text = response_text.replace('\t', ' ')  # Remove tabs
        
        # Fix trailing commas
        import re
        response_text = re.sub(r',(\s*[}\]])', r'\1', response_text)
        
        return response_text

    def validate_and_fix_analysis(self, analysis_data: Dict) -> Dict:
        """Validate and fix analysis data structure"""
        # Default structure
        default_analysis = {
            "primary_archetype": "Unknown Wanderer",
            "secondary_archetype": "Mystery Incarnate",
            "core_attributes": {"Enigma": 100},
            "mythic_resonance": "Sphinx",
            "elemental_affinity": "Void",
            "description": "The analysis was unclear..."
        }
        
        # Ensure all required fields exist
        for key, default_value in default_analysis.items():
            if key not in analysis_data:
                analysis_data[key] = default_value
        
        # Validate core_attributes is a dict with numeric values
        if not isinstance(analysis_data.get("core_attributes"), dict):
            analysis_data["core_attributes"] = {"Enigma": 100}
        else:
            # Ensure all values are numeric
            fixed_attrs = {}
            for attr, value in analysis_data["core_attributes"].items():
                try:
                    fixed_attrs[attr] = min(100, max(0, float(value)))
                except (ValueError, TypeError):
                    fixed_attrs[attr] = 50  # Default to 50%
            analysis_data["core_attributes"] = fixed_attrs
        
        return analysis_data

    async def analyze_adventurer(self, persona_data: Dict, selected_lens: str,
                                lens_weights: Dict[str, float] = None) -> Dict:
        """First call: Pure archetype analysis"""
        if lens_weights is None:
            lens_weights = {selected_lens: 1.0}
        
        analysis_prompt = self.build_analysis_prompt(persona_data, selected_lens, lens_weights)
        
        try:
            result = await self.ollama.chat(
                model=self.analyzer_model,
                messages=[{
                    'role': 'user',
                    'content': analysis_prompt
                }],
                system="You are an expert archetype analyzer. Return only valid JSON."
            )
            
            response_text = result['message']['content']
            
            # Clean and attempt to repair JSON formatting
            response_text = self.attempt_json_repair(response_text)
            
            # Debug: Print what we're trying to parse
            print(f"[Debug] Attempting to parse JSON: {response_text[:100]}...")
            
            # Validate we have actual content
            if not response_text or len(response_text.strip()) < 10:
                raise ValueError("Empty or too short response from AI model")
            
            # Try to parse JSON
            analysis = json.loads(response_text)
            
            # Validate and fix the analysis structure
            analysis = self.validate_and_fix_analysis(analysis)
            
            print(f"[Success] Parsed archetype analysis: {analysis.get('primary_archetype', 'Unknown')}")
            return analysis
            
        except json.JSONDecodeError as e:
            print(f"[JSON Error] Failed to parse response: {str(e)}")
            print(f"[JSON Error] Raw response: {response_text}")
            # Graceful fallback with specific JSON error info
            return {
                "primary_archetype": "Unknown Wanderer",
                "secondary_archetype": "Mystery Incarnate", 
                "core_attributes": {
                    "Enigma": 100
                },
                "mythic_resonance": "Sphinx",
                "elemental_affinity": "Void",
                "description": f"The crystal ball flickered... (JSON Parse Error: {str(e)})",
                "error": f"JSON parsing failed: {str(e)}",
                "raw_response": response_text[:200] + "..." if len(response_text) > 200 else response_text
            }
        except Exception as e:
            print(f"[General Error] Analysis failed: {str(e)}")
            # Graceful fallback for other errors
            return {
                "primary_archetype": "Unknown Wanderer",
                "secondary_archetype": "Mystery Incarnate",
                "core_attributes": {
                    "Enigma": 100
                },
                "mythic_resonance": "Sphinx", 
                "elemental_affinity": "Void",
                "description": f"The crystal ball flickered... (Error: {str(e)})",
                "error": str(e)
            }
    
    async def respond_in_character(self, persona_data: Dict, analysis_result: Dict,
                                   memory_context: List[Dict], mood: Dict,
                                   selected_lens: str) -> str:
        """Second call: Receptionist's animated response"""
        
        lens_info = ARCHETYPE_LENSES.get(selected_lens, {})
        
        # Build memory narrative
        memory_text = "First visit to the guild!"
        if memory_context:
            past_archetypes = [entry['analysis'].get('primary_archetype', 'Unknown') 
                             for entry in memory_context[:-1]]
            if past_archetypes:
                memory_text = f"Previous archetypes: {', '.join(past_archetypes[-3:])}"
        
        # Special handling for Bayesian lens
        bayesian_mode = selected_lens == "bayesian_probability"
        
        receptionist_prompt = f"""You are the Guild Receptionist, an energetic anime-style character who runs
the Adventurer's Guild. You just finished analyzing an adventurer through your mystical crystal ball.

YOUR PERSONALITY:
- Over-the-top enthusiastic (anime-style)
- Japanese verbal tics (ara ara~, fufu~, ne~, -san honorifics)
- Loves using sparkle emojis ✨ and dramatic gestures
- Makes specific measurements and percentages
- HIGHLY EXPRESSIVE with near-Japanese levels of explanation
- Playfully teases but always supportive

CURRENT MOOD: {mood.get('dialogue_flavor', 'standard')}
- Energy: {mood.get('energy', 100)}%
- Sass Level: {mood.get('sass_level', 50)}%
- Enthusiasm: {mood.get('enthusiasm', 90)}%

ANALYSIS RESULTS:
{json.dumps(analysis_result, indent=2)}

LENS USED: {lens_info.get('name', 'Unknown')}
MEMORY: {memory_text}

{"SPECIAL BAYESIAN MODE: Deliver this with lab-coat energy, statistical jargon, and probability percentages! Still anime enthusiastic but with MATH POWER." if bayesian_mode else ""}

Respond IN CHARACTER with:
1. Dramatic greeting or exclamation about the analysis
2. Present the archetype results with flair
3. Comment on specific attributes with percentages
4. Reference their elemental affinity dramatically
5. If this isn't their first visit, acknowledge their journey
6. End with an encouraging remark

Keep it 150-250 words. BE EXTRA SPARKLY. Use actual percentages from the analysis.
NO markdown formatting. Pure character voice."""

        try:
            result = await self.ollama.chat(
                model=self.receptionist_model,
                messages=[{
                    'role': 'user',
                    'content': receptionist_prompt
                }],
                system="You are a hyper-expressive anime guild receptionist. Never break character."
            )
            
            return result['message']['content']
            
        except Exception as e:
            return f"*The receptionist's crystal ball flickers* Oh my! Technical difficulties, gomen~ ✨ (Error: {str(e)})"


# ═══════════════════════════════════════════════════════════════
# ASYNC WORKER THREAD
# ═══════════════════════════════════════════════════════════════

class AnalysisWorker(QThread):
    """Worker thread for async Ollama calls"""
    finished = pyqtSignal(dict, str)
    error = pyqtSignal(str)
    progress = pyqtSignal(str)
    
    def __init__(self, receptionist: GuildReceptionist, persona_data: Dict,
                 lens: str, lens_weights: Dict, memory_context: List[Dict],
                 mood: Dict):
        super().__init__()
        self.receptionist = receptionist
        self.persona_data = persona_data
        self.lens = lens
        self.lens_weights = lens_weights
        self.memory_context = memory_context
        self.mood = mood
        
    def run(self):
        """Execute async analysis in thread"""
        try:
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
            
            self.progress.emit("✨ Crystal ball activating...")
            
            # First call: Analysis
            self.progress.emit("🔮 Divining your archetype...")
            analysis = loop.run_until_complete(
                self.receptionist.analyze_adventurer(
                    self.persona_data, self.lens, self.lens_weights
                )
            )
            
            # Second call: Receptionist response
            self.progress.emit("💫 Receptionist preparing response...")
            response = loop.run_until_complete(
                self.receptionist.respond_in_character(
                    self.persona_data, analysis, self.memory_context,
                    self.mood, self.lens
                )
            )
            
            loop.close()
            
            self.finished.emit(analysis, response)
            
        except Exception as e:
            self.error.emit(f"Analysis failed: {str(e)}\n{traceback.format_exc()}")


# ═══════════════════════════════════════════════════════════════
# MAIN GUI APPLICATION
# ═══════════════════════════════════════════════════════════════

class GuildReceptionistGUI(QMainWindow):
    """Main application window"""
    
    def __init__(self):
        super().__init__()
        self.setWindowTitle("🏰 Guild Receptionist - Mythic Archetype Divination Chamber 🔮")
        self.setGeometry(100, 100, 1500, 1000)  # Larger window for better readability
        
        # Initialize systems
        self.receptionist = GuildReceptionist()
        self.memory_registry = {}  # sigil -> AdventurerMemory
        self.current_sigil = ""
        self.available_models = []
        
        # Data storage
        self.data_dir = Path("guild_data")
        self.data_dir.mkdir(exist_ok=True)
        
        # Load receptionist lore
        self.load_receptionist_lore()
        
        # UI state
        self.persona_data = {category: [] for category in CHARACTER_FIELDS.keys()}
        self.persona_data['custom_inputs'] = {}
        self.lens_weights = {}
        
        # Apply fantasy theme
        self.apply_fantasy_theme()
        
        # Build UI
        self.init_ui()
        
        # Apply enhanced font styling
        QTimer.singleShot(100, self.update_font_styling)
        
        # Load models on startup
        QTimer.singleShot(500, self.load_models)
        
    def apply_fantasy_theme(self):
        """Apply fantasy aesthetic styling"""
        palette = QPalette()
        
        # Mythic Gothic Color Scheme: Deep midnight blues, silver accents, mystical purples
        palette.setColor(QPalette.ColorRole.Window, QColor(15, 15, 25))  # Deep midnight
        palette.setColor(QPalette.ColorRole.WindowText, QColor(220, 215, 255))  # Silvery white
        palette.setColor(QPalette.ColorRole.Base, QColor(20, 18, 35))  # Dark mystical base
        palette.setColor(QPalette.ColorRole.AlternateBase, QColor(25, 22, 40))  # Slightly lighter
        palette.setColor(QPalette.ColorRole.Text, QColor(230, 225, 255))  # Bright readable text
        palette.setColor(QPalette.ColorRole.Button, QColor(40, 35, 65))  # Gothic button base
        palette.setColor(QPalette.ColorRole.ButtonText, QColor(200, 180, 255))  # Mystical button text
        palette.setColor(QPalette.ColorRole.Highlight, QColor(120, 80, 200))  # Mystical purple highlight
        palette.setColor(QPalette.ColorRole.HighlightedText, QColor(255, 255, 255))  # Pure white
        
        self.setPalette(palette)
        
        # Enhanced Gothic Stylesheet with mystical elements
        self.setStyleSheet("""
            QMainWindow {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:1,
                    stop:0 #0F0F19, stop:0.3 #1A1525, stop:0.7 #151020, stop:1 #0A0A15);
                color: #E6E1FF;
            }
            
            QTabWidget::pane {
                border: 3px solid qlineargradient(x1:0, y1:0, x2:1, y2:0,
                    stop:0 #7850C8, stop:0.5 #A070E8, stop:1 #7850C8);
                border-radius: 8px;
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 #1A1628, stop:1 #12101D);
                margin-top: 10px;
            }
            
            QTabBar::tab {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 #2D2040, stop:1 #1F1530);
                color: #C8B4FF;
                padding: 12px 20px;
                margin: 2px;
                border-top-left-radius: 8px;
                border-top-right-radius: 8px;
                font-weight: bold;
                font-size: 11pt;
                border: 2px solid #7850C8;
                min-width: 120px;
            }
            
            QTabBar::tab:selected {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 #7850C8, stop:1 #5A3CA0);
                color: #FFFFFF;
                border-bottom: 3px solid #A070E8;
            }
            
            QTabBar::tab:hover:!selected {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 #4A3570, stop:1 #352850);
                color: #E6E1FF;
            }
            
            QPushButton {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 #5A3CA0, stop:0.5 #7850C8, stop:1 #4A3285);
                color: #FFFFFF;
                border: 2px solid qlineargradient(x1:0, y1:0, x2:1, y2:0,
                    stop:0 #A070E8, stop:0.5 #C890FF, stop:1 #A070E8);
                border-radius: 8px;
                padding: 10px 18px;
                font-weight: bold;
                font-size: 12pt;
            }
            
            QPushButton:hover {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 #7850C8, stop:0.5 #9B70E8, stop:1 #6A4CB0);
                border-color: #E8C8FF;
            }
            
            QPushButton:pressed {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 #4A3285, stop:1 #3A2570);
            }
            
            QPushButton:disabled {
                background: #2A2040;
                color: #666;
                border-color: #444;
            }
            
            QLineEdit, QTextEdit {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 #1A1628, stop:1 #0F0F19);
                color: #E6E1FF;
                border: 2px solid #7850C8;
                border-radius: 6px;
                padding: 8px 12px;
                font-size: 11pt;
                selection-background-color: #A070E8;
                selection-color: #FFFFFF;
            }
            
            QLineEdit:focus, QTextEdit:focus {
                border-color: #A070E8;
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 #1F1A30, stop:1 #141020);
            }
            
            QComboBox {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 #2D2040, stop:1 #1A1628);
                color: #C8B4FF;
                border: 2px solid #7850C8;
                border-radius: 6px;
                padding: 8px 12px;
                font-size: 11pt;
                min-width: 150px;
            }
            
            QComboBox:hover {
                border-color: #A070E8;
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 #3A2850, stop:1 #251D35);
            }
            
            QComboBox::drop-down {
                border: none;
                background: transparent;
                width: 20px;
            }
            
            QComboBox::down-arrow {
                image: none;
                border-left: 5px solid transparent;
                border-right: 5px solid transparent;
                border-top: 6px solid #A070E8;
                margin-right: 5px;
            }
            
            QComboBox QAbstractItemView {
                background: #1A1628;
                color: #E6E1FF;
                border: 2px solid #7850C8;
                border-radius: 4px;
                selection-background-color: #A070E8;
                selection-color: #FFFFFF;
            }
            
            QLabel {
                color: #E6E1FF;
                font-size: 11pt;
                font-weight: normal;
            }
            
            QCheckBox {
                color: #C8B4FF;
                font-size: 10pt;
                spacing: 8px;
            }
            
            QCheckBox::indicator {
                width: 18px;
                height: 18px;
                border-radius: 3px;
            }
            
            QCheckBox::indicator:unchecked {
                background: #1A1628;
                border: 2px solid #7850C8;
            }
            
            QCheckBox::indicator:unchecked:hover {
                background: #251D35;
                border-color: #A070E8;
            }
            
            QCheckBox::indicator:checked {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:1,
                    stop:0 #7850C8, stop:1 #A070E8);
                border: 2px solid #C890FF;
                image: none;
            }
            
            QCheckBox::indicator:checked:hover {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:1,
                    stop:0 #9B70E8, stop:1 #C890FF);
            }
            
            QGroupBox {
                border: 2px solid qlineargradient(x1:0, y1:0, x2:1, y2:0,
                    stop:0 #7850C8, stop:0.5 #A070E8, stop:1 #7850C8);
                border-radius: 8px;
                margin-top: 15px;
                padding-top: 15px;
                font-weight: bold;
                font-size: 12pt;
                color: #C8B4FF;
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 rgba(26, 22, 40, 0.3), stop:1 rgba(15, 15, 25, 0.3));
            }
            
            QGroupBox::title {
                subcontrol-origin: margin;
                left: 15px;
                padding: 0 8px;
                color: #E8C8FF;
                background: #1A1628;
                border-radius: 4px;
            }
            
            QScrollArea {
                border: 1px solid #7850C8;
                border-radius: 6px;
                background: transparent;
            }
            
            QScrollBar:vertical {
                background: #1A1628;
                width: 16px;
                border-radius: 8px;
                margin: 0;
            }
            
            QScrollBar::handle:vertical {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                    stop:0 #7850C8, stop:1 #A070E8);
                border-radius: 8px;
                min-height: 20px;
                margin: 2px;
            }
            
            QScrollBar::handle:vertical:hover {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                    stop:0 #9B70E8, stop:1 #C890FF);
            }
            
            QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {
                height: 0px;
            }
            
            QProgressBar {
                border: 2px solid #7850C8;
                border-radius: 8px;
                text-align: center;
                font-weight: bold;
                font-size: 11pt;
                color: #FFFFFF;
                background: #1A1628;
            }
            
            QProgressBar::chunk {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                    stop:0 #7850C8, stop:0.5 #A070E8, stop:1 #C890FF);
                border-radius: 6px;
                margin: 2px;
            }
            
            QSlider::groove:horizontal {
                border: 2px solid #7850C8;
                height: 8px;
                background: #1A1628;
                border-radius: 6px;
            }
            
            QSlider::handle:horizontal {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 #A070E8, stop:1 #7850C8);
                border: 2px solid #C890FF;
                width: 20px;
                height: 20px;
                border-radius: 12px;
                margin: -8px 0;
            }
            
            QSlider::handle:horizontal:hover {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 #C890FF, stop:1 #A070E8);
                border-color: #E8C8FF;
            }
            
            QSlider::sub-page:horizontal {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                    stop:0 #7850C8, stop:1 #A070E8);
                border-radius: 4px;
            }
            
            QTableWidget {
                background: #1A1628;
                alternate-background-color: #1F1A30;
                color: #E6E1FF;
                border: 2px solid #7850C8;
                border-radius: 6px;
                gridline-color: #4A3570;
                selection-background-color: #7850C8;
                selection-color: #FFFFFF;
            }
            
            QHeaderView::section {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 #3A2850, stop:1 #2D2040);
                color: #C8B4FF;
                border: 1px solid #7850C8;
                padding: 8px;
                font-weight: bold;
            }
            
            QHeaderView::section:hover {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 #4A3570, stop:1 #3A2850);
            }
        """)
        
        # Try to load custom fonts (fallback to system fonts if not available)
        self.load_gothic_fonts()
    
    def load_gothic_fonts(self):
        """Load gothic/fantasy fonts for enhanced visual appeal"""
        try:
            from PyQt6.QtGui import QFontDatabase
            
            # Common gothic/fantasy fonts to look for
            preferred_fonts = [
                "Cinzel",           # Elegant gothic serif
                "Immortal",         # Fantasy serif
                "MedievalSharp",    # Medieval style
                "UnifrakturMaguntia",  # Gothic blackletter
                "Griffy",           # Rough gothic
                "Creepster",        # Spooky gothic
                "Old London",       # Classic gothic
                "Blackadder ITC",   # Windows gothic
                "Chiller",          # Windows spooky
                "Papyrus",          # Mystical alternative
                "Trajan Pro",       # Classical carved look
                "Times New Roman",  # Fallback serif
                "Georgia"           # Fallback serif
            ]
            
            # Check which fonts are available
            font_families = QFontDatabase.families()
            
            selected_font = None
            for font in preferred_fonts:
                if font in font_families:
                    selected_font = font
                    print(f"[Font] Using gothic font: {font}")
                    break
            
            if not selected_font:
                # Use best available system font
                serif_fonts = [f for f in font_families if any(word in f.lower() for word in ['times', 'serif', 'roman', 'georgia'])]
                selected_font = serif_fonts[0] if serif_fonts else font_families[0] if font_families else "Arial"
                print(f"[Font] Fallback to system font: {selected_font}")
            
            # Apply font to the application
            gothic_font = QFont(selected_font, 10)
            gothic_font.setStyleHint(QFont.StyleHint.Serif)
            QApplication.instance().setFont(gothic_font)
            
            # Create special fonts for headers
            header_font = QFont(selected_font, 16, QFont.Weight.Bold)
            self.header_font = header_font
            
            title_font = QFont(selected_font, 14, QFont.Weight.Bold)
            self.title_font = title_font
            
            # Update specific UI elements with enhanced fonts
            self.update_font_styling()
            
        except Exception as e:
            print(f"[Font] Error loading gothic fonts: {e}")
            # Continue with system default fonts
            self.header_font = QFont("Arial", 16, QFont.Weight.Bold)
            self.title_font = QFont("Arial", 14, QFont.Weight.Bold)
            
    def update_font_styling(self):
        """Update specific UI elements with enhanced font styling"""
        # This will be called after UI creation to apply fonts to headers
        try:
            # Apply gothic fonts to main headers after UI is created
            if hasattr(self, 'header_font'):
                # Find and update header labels
                headers = self.findChildren(QLabel)
                for header in headers:
                    text = header.text()
                    if "✦" in text or "REGISTRATION" in text or "DIVINATION" in text:
                        header.setFont(self.header_font)
                        
            # Apply title font to group boxes
            if hasattr(self, 'title_font'):
                group_boxes = self.findChildren(QGroupBox)
                for group in group_boxes:
                    group.setFont(self.title_font)
                    
        except Exception as e:
            print(f"[Font] Error updating font styling: {e}")
    
    def init_ui(self):
        """Initialize all UI components"""
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        main_layout = QHBoxLayout(central_widget)
        
        # Create splitter for resizable panels
        splitter = QSplitter(Qt.Orientation.Horizontal)
        
        # Left panel: Input fields
        left_panel = self.create_input_panel()
        splitter.addWidget(left_panel)
        
        # Right panel: Results and controls
        right_panel = self.create_results_panel()
        splitter.addWidget(right_panel)
        
        # Set initial sizes (60% left, 40% right)
        splitter.setSizes([840, 560])
        
        main_layout.addWidget(splitter)
        
    def create_input_panel(self) -> QWidget:
        """Create left panel with character input fields"""
        panel = QWidget()
        layout = QVBoxLayout(panel)
        
        # Header
        header = QLabel("✦ ADVENTURER REGISTRATION ✦")
        header.setAlignment(Qt.AlignmentFlag.AlignCenter)
        if hasattr(self, 'header_font'):
            header.setFont(self.header_font)
        else:
            header.setFont(QFont("Arial", 16, QFont.Weight.Bold))
        header.setStyleSheet("""
            QLabel {
                color: #E8C8FF;
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                    stop:0 rgba(120, 80, 200, 0.3), stop:0.5 rgba(160, 112, 232, 0.4), stop:1 rgba(120, 80, 200, 0.3));
                border: 2px solid #A070E8;
                border-radius: 8px;
                padding: 12px;
                margin: 8px;
                text-shadow: 2px 2px 4px rgba(0,0,0,0.8);
            }
        """)
        layout.addWidget(header)
        
        # Adventurer Sigil input
        sigil_layout = QHBoxLayout()
        sigil_layout.addWidget(QLabel("Adventurer Sigil:"))
        self.sigil_input = QLineEdit()
        self.sigil_input.setPlaceholderText("Enter unique identifier (e.g., CrimsonPhoenix)")
        sigil_layout.addWidget(self.sigil_input)
        layout.addLayout(sigil_layout)
        
        # Create tabbed interface for fields
        self.field_tabs = QTabWidget()
        self.checkboxes = {}
        self.custom_inputs = {}
        
        for category, info in CHARACTER_FIELDS.items():
            tab = self.create_field_tab(category, info)
            self.field_tabs.addTab(tab, info['name'])
        
        layout.addWidget(self.field_tabs)
        
        # File operations
        file_ops = QHBoxLayout()
        
        load_btn = QPushButton("📂 Load")
        load_btn.clicked.connect(self.load_persona)
        file_ops.addWidget(load_btn)
        
        save_btn = QPushButton("💾 Save")
        save_btn.clicked.connect(self.save_persona)
        file_ops.addWidget(save_btn)
        
        refresh_btn = QPushButton("🔄 Refresh")
        refresh_btn.clicked.connect(self.refresh_fields)
        file_ops.addWidget(refresh_btn)
        
        layout.addLayout(file_ops)
        
        return panel
    
    def create_field_tab(self, category: str, info: Dict) -> QWidget:
        """Create a tab with checkboxes and custom input"""
        tab = QWidget()
        layout = QVBoxLayout(tab)
        
        # Scrollable area for checkboxes
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll_content = QWidget()
        scroll_layout = QGridLayout(scroll_content)
        
        # Create checkboxes in grid (3 columns)
        self.checkboxes[category] = []
        for idx, field in enumerate(info['fields']):
            checkbox = QCheckBox(field)
            checkbox.stateChanged.connect(lambda state, cat=category: self.update_persona_data(cat))
            self.checkboxes[category].append(checkbox)
            
            row = idx // 3
            col = idx % 3
            scroll_layout.addWidget(checkbox, row, col)
        
        scroll.setWidget(scroll_content)
        layout.addWidget(scroll)
        
        # Custom input field
        custom_label = QLabel(f"Custom {info['name']}:")
        layout.addWidget(custom_label)
        
        custom_input = QTextEdit()
        custom_input.setMaximumHeight(80)
        custom_input.setPlaceholderText("Add custom traits not in the list above...")
        custom_input.textChanged.connect(lambda cat=category: self.update_persona_data(cat))
        self.custom_inputs[category] = custom_input
        layout.addWidget(custom_input)
        
        return tab
    
    def create_results_panel(self) -> QWidget:
        """Create right panel with controls and results"""
        panel = QWidget()
        layout = QVBoxLayout(panel)
        
        # Header
        header = QLabel("✦ CRYSTAL BALL DIVINATION ✦")
        header.setAlignment(Qt.AlignmentFlag.AlignCenter)
        if hasattr(self, 'header_font'):
            header.setFont(self.header_font)
        else:
            header.setFont(QFont("Arial", 16, QFont.Weight.Bold))
        header.setStyleSheet("""
            QLabel {
                color: #E8C8FF;
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                    stop:0 rgba(120, 80, 200, 0.3), stop:0.5 rgba(160, 112, 232, 0.4), stop:1 rgba(120, 80, 200, 0.3));
                border: 2px solid #A070E8;
                border-radius: 8px;
                padding: 12px;
                margin: 8px;
                text-shadow: 2px 2px 4px rgba(0,0,0,0.8);
            }
        """)
        layout.addWidget(header)
        
        # Model selection
        model_group = QGroupBox("🔮 Scrying Orb Selection")
        model_layout = QVBoxLayout()
        
        self.model_combo = QComboBox()
        model_layout.addWidget(QLabel("Analysis Model:"))
        model_layout.addWidget(self.model_combo)
        
        self.receptionist_combo = QComboBox()
        model_layout.addWidget(QLabel("Receptionist Model:"))
        model_layout.addWidget(self.receptionist_combo)
        
        model_group.setLayout(model_layout)
        layout.addWidget(model_group)
        
        # Lens selection with archetype preview
        lens_group = QGroupBox("🔍 Archetypal Lens Selection")
        lens_layout = QVBoxLayout()
        
        # Main lens dropdown
        lens_select_layout = QHBoxLayout()
        lens_select_layout.addWidget(QLabel("Primary Lens:"))
        self.lens_combo = QComboBox()
        self.lens_combo.setMinimumWidth(300)
        
        # Add all available lenses with archetype counts
        for lens_key, lens_info in ARCHETYPE_LENSES.items():
            archetype_count = len(lens_info.get('archetypes', []))
            display_name = f"{lens_info['name']} ({archetype_count} archetypes)"
            self.lens_combo.addItem(display_name, lens_key)
        
        self.lens_combo.currentTextChanged.connect(self.on_lens_changed)
        lens_select_layout.addWidget(self.lens_combo)
        lens_layout.addLayout(lens_select_layout)
        
        # Lens description
        self.lens_description = QLabel()
        self.lens_description.setWordWrap(True)
        self.lens_description.setStyleSheet("""
            QLabel {
                background: rgba(26, 22, 40, 0.6);
                border: 1px solid #7850C8;
                border-radius: 6px;
                padding: 8px;
                color: #C8B4FF;
                font-style: italic;
            }
        """)
        lens_layout.addWidget(self.lens_description)
        
        # Archetype preview (scrollable list showing first 10 archetypes)
        preview_label = QLabel("Available Archetypes (Preview):")
        lens_layout.addWidget(preview_label)
        
        self.archetype_preview = QTextEdit()
        self.archetype_preview.setReadOnly(True)
        self.archetype_preview.setMaximumHeight(120)
        self.archetype_preview.setStyleSheet("""
            QTextEdit {
                background: rgba(15, 15, 25, 0.8);
                color: #E6E1FF;
                border: 1px solid #7850C8;
                border-radius: 4px;
                font-family: 'Courier New', monospace;
                font-size: 9pt;
                padding: 6px;
            }
        """)
        lens_layout.addWidget(self.archetype_preview)
        
        # Update preview with default lens
        self.update_lens_preview()
        
        # Lens weight sliders (now more compact)
        weight_label = QLabel("Lens Blend Weights (Advanced):")
        lens_layout.addWidget(weight_label)
        
        self.weight_sliders = {}
        # Create a scrollable area for weight sliders since we have many lenses now
        weight_scroll = QScrollArea()
        weight_scroll.setMaximumHeight(100)
        weight_scroll.setWidgetResizable(True)
        weight_widget = QWidget()
        weight_grid = QGridLayout(weight_widget)
        
        # Show weight sliders for first 6 most important lenses
        important_lenses = ['jungian', 'tarot_major', 'shadow_archetypes', 'divine_court_archetypes', 'modern_archetypes', 'mythic_pantheon']
        row, col = 0, 0
        for lens_key in important_lenses:
            if lens_key in ARCHETYPE_LENSES:
                lens_info = ARCHETYPE_LENSES[lens_key]
                
                # Compact slider layout
                slider_frame = QWidget()
                slider_layout = QVBoxLayout(slider_frame)
                slider_layout.setContentsMargins(2, 2, 2, 2)
                
                label = QLabel(lens_info['name'][:15] + "...")  # Truncate long names
                label.setStyleSheet("font-size: 8pt; color: #C8B4FF;")
                slider = QSlider(Qt.Orientation.Horizontal)
                slider.setRange(0, 100)
                slider.setValue(0)
                slider.setMaximumWidth(80)
                
                value_label = QLabel("0%")
                value_label.setStyleSheet("font-size: 8pt; color: #A070E8;")
                value_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
                slider.valueChanged.connect(lambda v, lbl=value_label: lbl.setText(f"{v}%"))
                
                slider_layout.addWidget(label)
                slider_layout.addWidget(slider)
                slider_layout.addWidget(value_label)
                
                weight_grid.addWidget(slider_frame, row, col)
                self.weight_sliders[lens_key] = slider
                
                col += 1
                if col >= 3:  # 3 columns
                    col = 0
                    row += 1
        
        weight_scroll.setWidget(weight_widget)
        lens_layout.addWidget(weight_scroll)
        
        lens_group.setLayout(lens_layout)
        layout.addWidget(lens_group)
        
        # Analyze button - Enhanced mystical styling
        self.analyze_btn = QPushButton("✨ DIVINE MY ARCHETYPE ✨")
        if hasattr(self, 'title_font'):
            self.analyze_btn.setFont(QFont(self.title_font.family(), 14, QFont.Weight.Bold))
        else:
            self.analyze_btn.setFont(QFont("Arial", 14, QFont.Weight.Bold))
        self.analyze_btn.setStyleSheet("""
            QPushButton {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 #7850C8, stop:0.3 #9B70E8, stop:0.7 #A070E8, stop:1 #7850C8);
                color: #FFFFFF;
                border: 3px solid qlineargradient(x1:0, y1:0, x2:1, y2:0,
                    stop:0 #C890FF, stop:0.5 #E8C8FF, stop:1 #C890FF);
                border-radius: 12px;
                padding: 15px 25px;
                font-weight: bold;
                font-size: 14pt;
                min-height: 25px;
            }
            QPushButton:hover {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 #9B70E8, stop:0.3 #C890FF, stop:0.7 #E8C8FF, stop:1 #9B70E8);
                border-color: #F8E8FF;
            }
            QPushButton:pressed {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 #5A3CA0, stop:1 #4A3285);
            }
        """)
        self.analyze_btn.clicked.connect(self.start_analysis)
        layout.addWidget(self.analyze_btn)
        
        # Progress bar
        self.progress_bar = QProgressBar()
        self.progress_bar.setRange(0, 0)  # Indeterminate
        self.progress_bar.hide()
        layout.addWidget(self.progress_bar)
        
        self.progress_label = QLabel("")
        self.progress_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(self.progress_label)
        
        # Results display
        results_group = QGroupBox("📜 Divination Results")
        results_layout = QVBoxLayout()
        
        # Stat window
        self.stat_display = QTextEdit()
        self.stat_display.setReadOnly(True)
        self.stat_display.setMaximumHeight(200)
        results_layout.addWidget(QLabel("Archetype Analysis:"))
        results_layout.addWidget(self.stat_display)
        
        # Receptionist response
        self.response_display = QTextEdit()
        self.response_display.setReadOnly(True)
        results_layout.addWidget(QLabel("Receptionist's Commentary:"))
        results_layout.addWidget(self.response_display)
        
        results_group.setLayout(results_layout)
        layout.addWidget(results_group)
        
        # Bottom buttons
        bottom_layout = QHBoxLayout()
        
        registry_btn = QPushButton("📖 Guild Registry")
        registry_btn.clicked.connect(self.show_guild_registry)
        bottom_layout.addWidget(registry_btn)
        
        export_btn = QPushButton("💫 Export Soul")
        export_btn.clicked.connect(self.export_soul)
        bottom_layout.addWidget(export_btn)
        
        import_btn = QPushButton("🌟 Import Soul")
        import_btn.clicked.connect(self.import_soul)
        bottom_layout.addWidget(import_btn)
        
        layout.addLayout(bottom_layout)
        
        # Graceful shutdown button
        shutdown_btn = QPushButton("🌙 Close Guild")
        shutdown_btn.clicked.connect(self.graceful_shutdown)
        layout.addWidget(shutdown_btn)
        
        return panel
    
    def on_lens_changed(self):
        """Handle lens selection change and update preview"""
        self.update_lens_preview()
    
    def update_lens_preview(self):
        """Update the archetype preview for the selected lens"""
        try:
            selected_lens = self.lens_combo.currentData()
            if not selected_lens or selected_lens not in ARCHETYPE_LENSES:
                return
            
            lens_info = ARCHETYPE_LENSES[selected_lens]
            
            # Update description
            description = lens_info.get('description', 'No description available.')
            self.lens_description.setText(description)
            
            # Update archetype preview
            archetypes = lens_info.get('archetypes', [])
            if archetypes:
                # Show first 8 archetypes, then indicate how many more
                preview_archetypes = archetypes[:8]
                preview_text = "• " + "\n• ".join(preview_archetypes)
                
                if len(archetypes) > 8:
                    remaining = len(archetypes) - 8
                    preview_text += f"\n\n... and {remaining} more archetypes"
                
                preview_text += f"\n\nTotal: {len(archetypes)} archetypes in this lens"
            else:
                preview_text = "No archetypes defined for this lens."
            
            self.archetype_preview.setText(preview_text)
            
        except Exception as e:
            print(f"Error updating lens preview: {e}")
    
    def update_persona_data(self, category: str):
        """Update persona data from UI"""
        # Collect checked boxes
        checked = []
        for checkbox in self.checkboxes[category]:
            if checkbox.isChecked():
                checked.append(checkbox.text())
        
        self.persona_data[category] = checked
        
        # Collect custom input
        custom_text = self.custom_inputs[category].toPlainText().strip()
        if custom_text:
            self.persona_data['custom_inputs'][category] = custom_text
    
    def load_models(self):
        """Load available Ollama models"""
        try:
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
            models = loop.run_until_complete(self.receptionist.ollama.list_models())
            loop.close()
            
            self.available_models = models
            
            # Populate dropdowns
            self.model_combo.clear()
            self.receptionist_combo.clear()
            
            for model in models:
                name = model.get('name', 'unknown')
                self.model_combo.addItem(f"🔮 {name}", name)
                self.receptionist_combo.addItem(f"✨ {name}", name)
            
            # Set defaults if available
            if models:
                self.receptionist.analyzer_model = models[0]['name']
                self.receptionist.receptionist_model = models[0]['name']
            
        except Exception as e:
            QMessageBox.warning(self, "Model Loading", 
                              f"Could not load Ollama models. Make sure Ollama is running.\n\nError: {str(e)}")
    
    def start_analysis(self):
        """Begin archetype analysis"""
        # Validate input
        sigil = self.sigil_input.text().strip()
        if not sigil:
            QMessageBox.warning(self, "Missing Sigil", 
                              "Please enter an Adventurer Sigil before analysis!")
            return
        
        self.current_sigil = sigil
        
        # Update persona data
        for category in CHARACTER_FIELDS.keys():
            self.update_persona_data(category)
        
        # Check if any data provided
        total_fields = sum(len(fields) for fields in self.persona_data.values() 
                          if isinstance(fields, list))
        if total_fields == 0:
            QMessageBox.warning(self, "No Data", 
                              "Please select some traits before analysis!")
            return
        
        # Get selected models
        analyzer_model = self.model_combo.currentData()
        receptionist_model = self.receptionist_combo.currentData()
        
        if analyzer_model:
            self.receptionist.analyzer_model = analyzer_model
        if receptionist_model:
            self.receptionist.receptionist_model = receptionist_model
        
        # Get selected lens
        selected_lens = self.lens_combo.currentData()
        
        # Get lens weights
        lens_weights = {}
        for lens_key, slider in self.weight_sliders.items():
            weight = slider.value() / 100.0
            if weight > 0:
                lens_weights[lens_key] = weight
        
        # Add primary lens if no weights set
        if not lens_weights:
            lens_weights = {selected_lens: 1.0}
        
        # Get or create memory
        if sigil not in self.memory_registry:
            self.memory_registry[sigil] = AdventurerMemory(sigil)
        
        memory = self.memory_registry[sigil]
        memory_context = memory.get_context_window()
        
        # Calculate mood
        current_time = datetime.now()
        user_streak = len(memory.entries)
        rare_events = []
        
        if len(memory.entries) == 0:
            rare_events.append('first_visit')
        
        mood = self.receptionist.mood_system.calculate_mood(
            current_time, user_streak, rare_events
        )
        
        # Show progress
        self.analyze_btn.setEnabled(False)
        self.progress_bar.show()
        self.progress_label.setText("Initiating divination...")
        
        # Start worker thread
        self.worker = AnalysisWorker(
            self.receptionist,
            self.persona_data,
            selected_lens,
            lens_weights,
            memory_context,
            mood
        )
        
        self.worker.finished.connect(self.on_analysis_complete)
        self.worker.error.connect(self.on_analysis_error)
        self.worker.progress.connect(self.on_analysis_progress)
        self.worker.start()
    
    def on_analysis_progress(self, message: str):
        """Update progress display"""
        self.progress_label.setText(message)
    
    def on_analysis_complete(self, analysis: Dict, response: str):
        """Handle completed analysis"""
        self.analyze_btn.setEnabled(True)
        self.progress_bar.hide()
        self.progress_label.setText("✨ Divination complete! ✨")
        
        # Display stat window
        stat_text = self.format_stat_display(analysis)
        self.stat_display.setText(stat_text)
        
        # Display receptionist response
        self.response_display.setText(response)
        
        # Save to memory
        if self.current_sigil in self.memory_registry:
            memory = self.memory_registry[self.current_sigil]
            memory.add_entry(analysis, "archetype_analysis", "Divine Reading")
            
            # Auto-save memory
            self.save_memory(self.current_sigil)
    
    def on_analysis_error(self, error_msg: str):
        """Handle analysis error"""
        self.analyze_btn.setEnabled(True)
        self.progress_bar.hide()
        self.progress_label.setText("")
        
        QMessageBox.critical(self, "Analysis Error", 
                           f"The crystal ball encountered an issue:\n\n{error_msg}")
    
    def format_stat_display(self, analysis: Dict) -> str:
        """Format analysis as stat window"""
        lines = [
            "═" * 50,
            "     ARCHETYPE ANALYSIS COMPLETE",
            "═" * 50,
            f"Primary: {analysis.get('primary_archetype', 'Unknown')}",
            f"Secondary: {analysis.get('secondary_archetype', 'None')}",
            "",
            "Core Attributes:",
        ]
        
        for attr, value in analysis.get('core_attributes', {}).items():
            bar_length = int(value / 10)
            bar = "▰" * bar_length + "▱" * (10 - bar_length)
            lines.append(f"{bar} {attr} ({value}%)")
        
        lines.extend([
            "",
            f"Mythic Resonance: {analysis.get('mythic_resonance', 'Unknown')}",
            f"Elemental Affinity: {analysis.get('elemental_affinity', 'Unknown')}",
            "",
            "Description:",
            analysis.get('description', 'No description available'),
            "═" * 50
        ])
        
        return "\n".join(lines)
    
    def save_persona(self):
        """Save current persona to file"""
        filename, _ = QFileDialog.getSaveFileName(
            self, "Save Persona", "", 
            "YAML Files (*.yaml);;JSON Files (*.json);;All Files (*)"
        )
        
        if not filename:
            return
        
        # Update data from UI
        for category in CHARACTER_FIELDS.keys():
            self.update_persona_data(category)
        
        data = {
            'sigil': self.sigil_input.text(),
            'persona': self.persona_data,
            'saved_at': datetime.now(timezone.utc).isoformat()
        }
        
        try:
            if filename.endswith('.yaml'):
                with open(filename, 'w') as f:
                    yaml.dump(data, f, default_flow_style=False)
            else:
                with open(filename, 'w') as f:
                    json.dump(data, f, indent=2)
            
            QMessageBox.information(self, "Saved", 
                                  f"Persona saved to {filename}")
        except Exception as e:
            QMessageBox.critical(self, "Save Error", 
                               f"Failed to save: {str(e)}")
    
    def load_persona(self):
        """Load persona from file"""
        filename, _ = QFileDialog.getOpenFileName(
            self, "Load Persona", "",
            "All Supported (*.yaml *.json *.txt);;YAML Files (*.yaml);;JSON Files (*.json);;Text Files (*.txt);;All Files (*)"
        )
        
        if not filename:
            return
        
        try:
            with open(filename, 'r') as f:
                if filename.endswith('.yaml'):
                    data = yaml.safe_load(f)
                elif filename.endswith('.json'):
                    data = json.load(f)
                else:
                    # Try to parse as JSON first, then YAML
                    content = f.read()
                    try:
                        data = json.loads(content)
                    except:
                        data = yaml.safe_load(content)
            
            # Load sigil
            if 'sigil' in data:
                self.sigil_input.setText(data['sigil'])
            
            # Load persona data
            persona = data.get('persona', data)  # Flexible format
            
            # Update checkboxes
            for category, fields in persona.items():
                if category in self.checkboxes and isinstance(fields, list):
                    for checkbox in self.checkboxes[category]:
                        checkbox.setChecked(checkbox.text() in fields)
            
            # Update custom inputs
            custom_inputs = persona.get('custom_inputs', {})
            for category, text in custom_inputs.items():
                if category in self.custom_inputs:
                    self.custom_inputs[category].setText(text)
            
            QMessageBox.information(self, "Loaded", 
                                  f"Persona loaded from {filename}")
            
        except Exception as e:
            QMessageBox.critical(self, "Load Error", 
                               f"Failed to load: {str(e)}")
    
    def refresh_fields(self):
        """Clear all fields"""
        reply = QMessageBox.question(
            self, "Refresh Fields",
            "Clear all current selections?",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
        )
        
        if reply == QMessageBox.StandardButton.Yes:
            self.sigil_input.clear()
            
            for category in self.checkboxes:
                for checkbox in self.checkboxes[category]:
                    checkbox.setChecked(False)
            
            for category in self.custom_inputs:
                self.custom_inputs[category].clear()
            
            self.persona_data = {category: [] for category in CHARACTER_FIELDS.keys()}
            self.persona_data['custom_inputs'] = {}
    
    def show_guild_registry(self):
        """Show registry of all adventurers"""
        dialog = QDialog(self)
        dialog.setWindowTitle("Guild Registry")
        dialog.setGeometry(200, 200, 800, 600)
        
        layout = QVBoxLayout(dialog)
        
        # Table
        table = QTableWidget()
        table.setColumnCount(5)
        table.setHorizontalHeaderLabels([
            "Sigil", "Last Visit", "Total Visits", "Last Archetype", "Actions"
        ])
        table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        
        # Populate table
        table.setRowCount(len(self.memory_registry))
        for row, (sigil, memory) in enumerate(self.memory_registry.items()):
            table.setItem(row, 0, QTableWidgetItem(sigil))
            
            if memory.entries:
                last_entry = memory.entries[-1]
                last_visit = datetime.fromisoformat(last_entry['timestamp'])
                last_archetype = last_entry['analysis'].get('primary_archetype', 'Unknown')
                
                table.setItem(row, 1, QTableWidgetItem(
                    last_visit.strftime("%Y-%m-%d %H:%M")
                ))
                table.setItem(row, 2, QTableWidgetItem(str(len(memory.entries))))
                table.setItem(row, 3, QTableWidgetItem(last_archetype))
            else:
                table.setItem(row, 1, QTableWidgetItem("Never"))
                table.setItem(row, 2, QTableWidgetItem("0"))
                table.setItem(row, 3, QTableWidgetItem("Unknown"))
            
            # Action button
            view_btn = QPushButton("View")
            view_btn.clicked.connect(lambda checked, s=sigil: self.load_adventurer(s))
            table.setCellWidget(row, 4, view_btn)
        
        layout.addWidget(table)
        
        close_btn = QPushButton("Close")
        close_btn.clicked.connect(dialog.close)
        layout.addWidget(close_btn)
        
        dialog.exec()
    
    def load_adventurer(self, sigil: str):
        """Load an adventurer's data"""
        # This would load their full persona from saved files
        # For now, just set the sigil
        self.sigil_input.setText(sigil)
        QMessageBox.information(self, "Adventurer Loaded", 
                              f"Loaded: {sigil}\n\nNote: Full persona loading from registry coming soon!")
    
    def export_soul(self):
        """Export adventurer memory"""
        sigil = self.sigil_input.text().strip()
        if not sigil or sigil not in self.memory_registry:
            QMessageBox.warning(self, "Export Soul", 
                              "No adventurer memory to export!")
            return
        
        filename, _ = QFileDialog.getSaveFileName(
            self, "Export Soul", f"{sigil}_soul.json",
            "JSON Files (*.json);;All Files (*)"
        )
        
        if not filename:
            return
        
        try:
            memory = self.memory_registry[sigil]
            soul_data = memory.export_soul()
            
            with open(filename, 'w') as f:
                json.dump(soul_data, f, indent=2)
            
            QMessageBox.information(self, "Soul Exported", 
                f"✨ Soul transfer complete! Your essence has been preserved.\n\nFile: {filename}")
            
        except Exception as e:
            QMessageBox.critical(self, "Export Error", 
                               f"Soul export failed: {str(e)}")
    
    def import_soul(self):
        """Import adventurer memory"""
        filename, _ = QFileDialog.getOpenFileName(
            self, "Import Soul", "",
            "JSON Files (*.json);;All Files (*)"
        )
        
        if not filename:
            return
        
        try:
            with open(filename, 'r') as f:
                data = json.load(f)
            
            memory = AdventurerMemory.import_soul(data)
            
            self.memory_registry[memory.sigil] = memory
            self.sigil_input.setText(memory.sigil)
            
            # Auto-save
            self.save_memory(memory.sigil)
            
            QMessageBox.information(self, "Soul Imported", 
                f"✨ Soul transfer complete! Welcome home, {memory.sigil}!\n\n"
                f"Restored {len(memory.entries)} memory shards.")
            
        except ValueError as e:
            QMessageBox.critical(self, "Import Error", 
                f"Soul corruption detected!\n\n{str(e)}")
        except Exception as e:
            QMessageBox.critical(self, "Import Error", 
                f"Soul import failed: {str(e)}")
    
    def save_memory(self, sigil: str):
        """Auto-save memory to disk"""
        if sigil not in self.memory_registry:
            return
        
        memory_file = self.data_dir / f"{sigil}_memory.jsonl"
        
        try:
            with open(memory_file, 'w') as f:
                for entry in self.memory_registry[sigil].entries:
                    f.write(json.dumps(entry) + '\n')
        except Exception as e:
            print(f"Failed to save memory: {e}")
    
    def load_receptionist_lore(self):
        """Load receptionist personality configuration"""
        lore_file = self.data_dir / "receptionist_lore.yaml"
        
        if lore_file.exists():
            try:
                with open(lore_file, 'r') as f:
                    self.receptionist_lore = yaml.safe_load(f)
            except:
                self.receptionist_lore = {}
        else:
            # Create default lore
            self.receptionist_lore = {
                'personality': {
                    'base_enthusiasm': 90,
                    'sass_level': 65,
                    'empathy': 85
                },
                'dialogue_unlocks': {
                    'streak_10': ["Oh! You've been coming by regularly! I'm starting to remember your face~"],
                    'streak_50': ["Fifty visits! You're basically family now. Want to hear a guild secret?"]
                }
            }
            
            with open(lore_file, 'w') as f:
                yaml.dump(self.receptionist_lore, f)
    
    def graceful_shutdown(self):
        """Graceful application closure"""
        # Save all memories
        for sigil in self.memory_registry:
            self.save_memory(sigil)
        
        # Farewell dialog
        farewell = QMessageBox(self)
        farewell.setWindowTitle("Guild Closing for the Evening")
        farewell.setText(
            "「Safe travels, brave soul~ ✨」\n\n"
            "The Guild Receptionist waves as the crystal ball dims.\n"
            "All adventurer records have been safely stored in the archives.\n\n"
            "May the stars guide your path until we meet again!"
        )
        farewell.setIcon(QMessageBox.Icon.Information)
        farewell.exec()
        
        # Close application
        QApplication.quit()
    
    def closeEvent(self, event):
        """Handle window close event"""
        self.graceful_shutdown()
        event.accept()


# ═══════════════════════════════════════════════════════════════
# APPLICATION ENTRY POINT
# ═══════════════════════════════════════════════════════════════

def main():
    """Launch the Guild Receptionist application"""
    app = QApplication(sys.argv)
    
    # Set application metadata
    app.setApplicationName("Guild Receptionist")
    app.setApplicationVersion("1.0.0")
    app.setOrganizationName("Mythic Forge Studios")
    
    # Create and show main window
    window = GuildReceptionistGUI()
    window.show()
    
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
