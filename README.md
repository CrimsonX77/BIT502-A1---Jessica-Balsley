# BIT502 Assessment 1 - The Aurora Archive
**Student:** Jessica Balsley  
**Course:** BIT502 Fundamentals of Programming  
**Assessment:** Assignment 1 - Console Application Development

---

## 📋 Assignment Submission

### Required File
**`BIT502_AS1_Jessica_Balsley.py`** - The main assignment submission

This is the **official assessment submission** that fulfills all requirements as specified in the assignment brief:

- ✅ Task 1: Main menu with 5 options and navigation
- ✅ Task 2: Membership plans sub-menu with cost calculations
- ✅ Task 3: Optional extras selection with total calculation
- ✅ Task 4: Kids' Reading Challenge with ranking system
- ✅ Task 5: Aurora-Picks Rental Calculator with tiered pricing

### How to Run
```bash
python BIT502_AS1_Jessica_Balsley.py
```

Or on Windows:
```bash
python3 BIT502_AS1_Jessica_Balsley.py
```

**Requirements:**
- Python 3.6 or higher
- No external dependencies required
- Works on Windows, Linux, and macOS

---

## 🎨 Extended Implementation (Bonus)

In addition to the required console application, this submission includes an **extended implementation** demonstrating advanced programming concepts and real-world application architecture.

### Extended Files

#### Core System Files
- **`archive_sanctum.py`** - PyQt6 GUI member portal with advanced features
- **`aurora_pyqt6_main.py`** - Card generation interface
- **`member_manager.py`** - Member data management system
- **`member_registration_app.py`** - Registration workflow

#### Authentication & Security
- **`obelisk_customs.py`** - Multi-stage authentication system
- **`api_config_manager.py`** - Secure API configuration with encryption

#### Card Generation System
- **`card_generation.py`** - AI-powered card generation
- **`card_scanner.py`** - Card authentication and validation
- **`steganography_module.py`** - Data embedding in images
- **`mutable_steganography.py`** - Advanced steganographic techniques

### Extended Features Demonstrated

#### Advanced Programming Concepts
- **Object-Oriented Design**: Classes, inheritance, encapsulation
- **GUI Development**: PyQt6 with custom widgets and animations
- **Cryptography**: Fernet encryption, PBKDF2 key derivation
- **Steganography**: LSB encoding for data embedding
- **API Integration**: Support for multiple AI backends (Grok, Stable Diffusion, OpenAI)
- **File I/O**: JSON configuration, image processing
- **Error Handling**: Comprehensive try-except blocks with graceful fallbacks
- **Resource Management**: Proper cleanup of timers, dialogs, and resources

#### Architecture Patterns
- **Separation of Concerns**: Modular design with distinct responsibilities
- **Configuration Management**: Centralized constants and encrypted storage
- **Event-Driven Programming**: Signal/slot architecture in PyQt6
- **State Management**: Session handling and authentication flows

#### Real-World Features
- **Multi-tier Subscription System**: Bronze, Silver, Gold, Platinum tiers
- **Rental Tracking**: Book checkout with due dates
- **Achievement System**: Gamification elements
- **Visual Dashboards**: Constellation-style data visualization
- **Secure Authentication**: Two-stage verification with cryptographic signing

---

## 🚀 Quick Start Launcher

For evaluators who wish to see the extended implementation:

### Windows
```bash
launch_aurora.bat
```

### Linux/Mac
```bash
./launch_aurora.sh
```

The launcher will:
1. Check Python installation and version
2. Verify/create virtual environment
3. Install required dependencies
4. Check for optional AI backends (Stable Diffusion)
5. Launch all GUI applications in sequence
6. Provide fallback options if components are unavailable

**Note:** The extended implementation requires additional dependencies (PyQt6, cryptography, Pillow, requests). These are automatically installed by the launcher.

---

## 📦 Project Structure

```
BIT502_A1_Jessica_Balsley/
├── BIT502_AS1_Jessica_Balsley.py    # ⭐ MAIN ASSESSMENT FILE
├── README.md                         # This file
├── launch_aurora.bat                 # Windows launcher
├── launch_aurora.sh                  # Linux/Mac launcher
├── requirements.txt                  # Python dependencies
│
├── archive_sanctum.py               # Extended: Member portal GUI
├── aurora_pyqt6_main.py             # Extended: Card generator GUI
├── obelisk_customs.py               # Extended: Authentication system
├── api_config_manager.py            # Extended: API configuration
├── member_manager.py                # Extended: Member management
├── member_registration_app.py       # Extended: Registration GUI
├── card_generation.py               # Extended: Card generation logic
├── card_scanner.py                  # Extended: Card validation
├── steganography_module.py          # Extended: Data embedding
└── mutable_steganography.py         # Extended: Advanced steganography
```

---

## 💡 Design Decisions

### Assignment Compliance
The main submission file (`BIT502_AS1_Jessica_Balsley.py`) strictly adheres to the assessment requirements:

- **Console-based**: Text-only interface as specified
- **Menu-driven**: Clear numbered options with input validation
- **Beginner-friendly**: Uses only fundamental Python concepts
- **Well-documented**: Comments explain logic and calculations
- **Easy to modify**: Constants defined at the top for future changes
- **Error handling**: Validates all user inputs with helpful messages
- **Good practices**: Meaningful variable names, function decomposition, no hard-coding

### Extended Implementation Philosophy
The extended implementation demonstrates:

- **Scalability**: Architecture supports growth and feature additions
- **Security**: Encryption for sensitive data, secure authentication flows
- **User Experience**: Polished GUI with animations and visual feedback
- **Maintainability**: Modular design with clear separation of concerns
- **Real-world applicability**: Features you'd find in production systems

---

## 🧪 Testing

### Basic Submission Testing
The main assessment file has been tested with:
- ✅ Valid inputs for all menu options
- ✅ Invalid inputs (letters, out-of-range numbers, empty inputs)
- ✅ Edge cases (minimum/maximum rental days, record-breaking reading challenge)
- ✅ Navigation flow (returning to menus, exiting cleanly)
- ✅ Calculation accuracy (membership costs, rental tiers, reading rankings)

### Extended Implementation Testing
The extended system has been tested with:
- ✅ GUI responsiveness and animations
- ✅ File I/O operations (reading/writing cards and configs)
- ✅ Encryption/decryption cycles
- ✅ Steganographic encoding/decoding
- ✅ API connection handling (with and without valid credentials)
- ✅ Resource cleanup (timers, dialogs, file handles)

---

## 📚 Dependencies

### Core Assignment (Required)
- Python 3.6+
- Standard library only (`os`, `sys`)

### Extended Implementation (Optional)
```
PyQt6>=6.4.0
cryptography>=41.0.0
Pillow>=10.0.0
requests>=2.31.0
numpy>=1.24.0
```

Install via:
```bash
pip install -r requirements.txt
```

---

## 🎓 Learning Outcomes Demonstrated

### LO1: Create simple applications using fundamental programming logic
- ✅ Variables, constants, and data types
- ✅ Conditional statements (if/elif/else)
- ✅ Loops (while, for)
- ✅ Functions with parameters and return values
- ✅ Input validation and error handling
- ✅ Mathematical operations and calculations
- ✅ String formatting and output

### Additional Skills (Extended)
- Advanced data structures (dictionaries, lists, nested structures)
- Object-oriented programming (classes, methods, inheritance)
- GUI development with event-driven architecture
- File handling and persistence
- Cryptography and security concepts
- API integration and network requests
- Image processing and steganography
- Resource management and cleanup

---

## 📝 Code Quality

### Assessment Submission
- **Lines of code**: ~450
- **Functions**: 15 well-defined functions
- **Comments**: Strategic comments explaining complex logic
- **Style**: PEP 8 compliant
- **Maintainability**: High - easy to understand and modify

### Extended Implementation
- **Total lines**: ~4,000+
- **Modules**: 10 specialized modules
- **Classes**: 20+ custom classes
- **Documentation**: Comprehensive docstrings and inline comments
- **Architecture**: Production-ready modular design

---

## 🔧 Troubleshooting

### Main Assessment File
If you encounter issues running the main submission:

1. **ImportError**: Ensure Python 3.6+ is installed
2. **Clear screen not working**: Normal in some terminals, doesn't affect functionality
3. **Input validation loops**: Intentional - keeps prompting until valid input received

### Extended Implementation
If the launcher fails:

1. **No Python**: Install Python 3.10+ from python.org
2. **Virtual environment issues**: Run launcher again - it will recreate
3. **Dependency errors**: Check internet connection - pip needs to download packages
4. **GUI doesn't appear**: Ensure you're running in a desktop environment (not SSH/headless)
5. **Missing Stable Diffusion**: Optional - system will run without it

---

## 👤 About

**Developer Notes:**

This submission demonstrates both:
1. **Compliance with assessment requirements** - A clean, functional console application
2. **Initiative and advanced understanding** - An extended implementation showing real-world capabilities

The main assessment file can be evaluated independently without any external dependencies. The extended implementation is provided as supplementary evidence of programming proficiency and system design skills.

**Contact:**
- Student: Jessica Balsley
- Course: BIT502 - Open Polytechnic of New Zealand

---

## 📄 License

This project is submitted as part of academic coursework for BIT502. All code is original work created for this assessment.

---

## 🙏 Acknowledgments

- Open Polytechnic of New Zealand for the assessment framework
- Python community for excellent documentation
- PyQt6 for the GUI framework

---

**Assessment Completed:** November 2024  
**Python Version:** 3.10+  
**Tested On:** Windows 11, Ubuntu 22.04, macOS Sonoma
