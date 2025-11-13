# BIT502 Assessment 1 - The Aurora Archive
## Bookstore Membership System

**Student:** Jessica Balsley  
**Student Number:** [INSERT STUDENT NUMBER]  
**Course:** BIT502 Fundamentals of Programming  
**Assessment:** Assignment 1 - Set A ver. 3.1  

---

## 📋 Assignment Submission

### Required Files
The core assignment submission file that fulfills all assessment requirements:

- **`BIT502_AS1_Jessica_Balsley.py`** - Main console application (SUBMIT THIS)

This file contains a fully functional console-based bookstore membership management system with:
- ✅ Task 1: Main menu with navigation
- ✅ Task 2: Membership plans sub-menu with cost calculations
- ✅ Task 3: Optional extras selection and totaling
- ✅ Task 4: Kids' reading challenge with rankings
- ✅ Task 5: Aurora-Picks rental calculator
- ✅ Full error handling and input validation
- ✅ Good programming practices throughout

### How to Run the Assignment
```bash
python BIT502_AS1_Jessica_Balsley.py
```

No additional dependencies required - uses only Python standard library.

---

## 🚀 Extended Implementation (Optional)

In addition to the required console application, this submission includes an **extended implementation** demonstrating advanced programming concepts and real-world application architecture.

### Extended Features Overview
The extended implementation showcases:
- GUI application development (PyQt6)
- Multi-stage authentication systems
- Database-like member management
- Image processing and steganography
- API integration patterns
- Modular architecture design
- Secure configuration management

### Extended Files Structure
```
aurora_pyqt6_main.py          # Main GUI application launcher
archive_sanctum.py            # Member dashboard (PyQt6 GUI)
member_registration_app.py    # Member registration interface
member_manager.py             # Member data management
card_generation.py            # Member card generation system
card_scanner.py              # Card authentication scanner
obelisk_customs.py           # Authentication gateway
steganography_module.py      # Data embedding in images
mutable_steganography.py     # Advanced steganography
api_config_manager.py        # API configuration management
launcher.bat / launcher.sh   # Automated setup and launch scripts
```

### Running the Extended Implementation

**Windows:**
```bash
launcher.bat
```

**Linux/Mac:**
```bash
chmod +x launcher.sh
./launcher.sh
```

The launcher will:
1. Check for Python 3.10+ installation
2. Create/activate virtual environment
3. Install required dependencies (PyQt6, Pillow, cryptography)
4. Optionally download Stable Diffusion WebUI (if selected)
5. Launch all GUI applications in sequence

### Extended Implementation Features

#### 1. **Archive Sanctum** (Member Dashboard)
- Visual constellation dashboard showing account status
- Tier-based membership visualization
- Achievement system with unlockable badges
- Book rental tracking with due dates
- Subscription upgrade portal
- Animated UI with real-time updates

#### 2. **Card Generation System**
- AI-powered member card generation
- Steganographic data embedding
- Unique visual identity for each member
- Supports multiple AI backends (Stable Diffusion, DALL-E, Grok)

#### 3. **Authentication System**
- Multi-stage verification (Obelisk gateway)
- Steganography-based card scanning
- Secure session management
- Visual MP4 avatars with audio

#### 4. **Member Management**
- Complete CRUD operations
- Tier-based permissions
- Generation tracking and limits
- Book rental records
- Subscription management

---

## 📦 Dependencies

### Core Assignment (No dependencies)
- Python 3.8+
- Standard library only

### Extended Implementation
- Python 3.10+
- PyQt6 >= 6.4.0
- Pillow >= 10.0.0
- cryptography >= 41.0.0
- requests >= 2.31.0
- (Optional) Stable Diffusion WebUI for AI card generation

---

## 🎯 Assessment Requirements Mapping

### Task 1: Main Menu (15 marks)
**Location:** Lines 537-561 in `BIT502_AS1_Jessica_Balsley.py`
- Full menu navigation with error handling
- Options 1-5 working correctly
- Clear screen functionality
- Graceful exit with message

### Task 2: Membership Plans (25 marks)
**Location:** Lines 122-184
- Sub-menu with all options (Standard, Premium, Kids)
- Monthly and annual cost calculations
- One month free discount applied correctly
- Return to main menu and exit functionality
- Proper error handling

### Task 3: Optional Extras (20 marks)
**Location:** Lines 191-258
- All four extras displayed with prices
- Yes/no prompts for each extra
- Case-insensitive input handling (yes/y, no/n)
- Summary display with selected items
- Total cost calculation
- Clear formatting

### Task 4: Reading Challenge (20 marks)
**Location:** Lines 265-347
- Input for 5 weekdays (Monday-Friday)
- Accepts integer and decimal values
- Calculates total and average pages
- Determines correct rank (Bronze/Silver/Gold/Platinum)
- Shows day(s) with most pages
- Displays pages needed for next rank
- Special message for breaking record (>150 pages)
- Proper error handling for invalid inputs

### Task 5: Aurora-Picks Rental (20 marks)
**Location:** Lines 354-426
- Sub-menu with rental period and return options
- Tiered pricing structure:
  - Days 1-3: $1.00/day
  - Days 4-8: $0.80/day
  - Days 9-21: $0.50/day
  - Day 21: Fixed $12.00
- Minimum 3 days, maximum 21 days validation
- Integer input validation
- Cost calculation with proper accumulation
- Clear error messages

---

## 💻 Code Quality Features

### Good Programming Practices Implemented
- **Constants:** All prices defined at top for easy modification
- **Functions:** Modular code with single-responsibility functions
- **Validation:** Comprehensive input validation with error handling
- **User Experience:** Clear prompts, formatted output, screen clearing
- **Error Handling:** Graceful handling of invalid inputs
- **Comments:** Explanatory comments for complex logic
- **Naming:** Meaningful variable and function names
- **No Hard-Coding:** All values stored in constants
- **DRY Principle:** Reusable validation functions

### Validation Functions
- `get_valid_integer()` - Integer input with range checking
- `get_valid_number()` - Numeric input (int/float) with validation
- `get_yes_no()` - Yes/no input with case-insensitive handling
- `clear_screen()` - Cross-platform screen clearing
- `pause()` - Consistent user pacing

---

## 🧪 Testing

### Test Scenarios Covered
1. **Menu Navigation:** All menu options 1-5 tested
2. **Invalid Input:** Non-numeric, out-of-range, empty inputs handled
3. **Edge Cases:** 
   - Reading challenge: 0 pages, record-breaking amounts
   - Rental: 3 days (minimum), 21 days (maximum, fixed price)
   - Optional extras: All combinations tested
4. **Calculations:** All pricing formulas verified
5. **Navigation:** Return to menu and exit from all sub-menus

### Known Limitations (By Design)
- No persistent data storage (as per assignment requirements)
- Console-based interface only (for core submission)
- No database integration (not required)

---

## 📚 Learning Outcomes Demonstrated

### LO1: Create simple applications using fundamental programming logic
✅ **Demonstrated through:**
- Control structures (if/elif/else, while loops)
- Functions with parameters and return values
- Input/output operations
- Error handling and validation
- Mathematical operations (calculations, comparisons)
- Boolean logic (yes/no validation)
- Data structures (lists for pages, dictionaries for extras)

---

## 🎨 Design Philosophy

### Core Assignment
- **Simplicity:** Clean, readable code following Python conventions
- **Robustness:** Comprehensive error handling prevents crashes
- **Usability:** Clear prompts and formatted output
- **Maintainability:** Modular design with constants for easy updates

### Extended Implementation
- **Scalability:** Modular architecture supports future expansion
- **Security:** Encrypted configuration, steganographic authentication
- **User Experience:** Polished GUI with animations and visual feedback
- **Real-World Patterns:** Demonstrates industry-standard practices

---

## 🔮 Future Enhancements (Conceptual)

Potential improvements for a production system:
1. Database integration (SQLite/PostgreSQL)
2. User authentication and sessions
3. Payment processing integration
4. Inventory management system
5. Email notifications for due dates
6. Web interface (Flask/Django)
7. Mobile application
8. Analytics dashboard
9. Export/reporting functionality
10. Multi-language support

---

## 🙏 Acknowledgments

This project demonstrates progression from fundamental programming concepts (console application) to advanced real-world application development (GUI with authentication and data management).

The core submission fulfills all assignment requirements while the extended implementation showcases potential career-ready development skills.

---

## 📞 Support

For any questions about this submission:
- Check code comments in `BIT502_AS1_Jessica_Balsley.py`
- Review this README for feature documentation
- Test using the provided launcher scripts

---

## ⚖️ Academic Integrity Statement

This work is my own original submission. All code has been written specifically for this assessment and demonstrates my understanding of fundamental programming concepts taught in BIT502.

**Submitted:** [INSERT DATE]  
**Word Count:** N/A (Programming Assessment)  

---

**Note:** The core assignment file (`BIT502_AS1_Jessica_Balsley.py`) is fully self-contained and meets all assessment criteria. The extended implementation is provided as supplementary material to demonstrate additional technical capabilities.
