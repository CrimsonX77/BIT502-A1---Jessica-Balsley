# Bookstore Members Club Database

A bookstore members club management system with an interactive GUI built using PyQt6 and SQLAlchemy.

## Features

- Member database management
- Interactive PyQt6 GUI
- SQLAlchemy ORM for database operations
- Data export capabilities with pandas and openpyxl

## Requirements

- Python 3.10
- See `requirements.txt` for all dependencies

## Installation

1. Clone the repository:
```bash
git clone <your-repo-url>
cd Authunder
```

2. Create a virtual environment:
```bash
python3.10 -m venv venv
```

3. Activate the virtual environment:
```bash
source venv/bin/activate  # On Linux/Mac
# or
venv\Scripts\activate  # On Windows
```

4. Install dependencies:
```bash
pip install -r requirements.txt
```

## Usage

```bash
python Bookward.py
```

## Project Structure

```
Authunder/
├── Bookward.py          # Main application file
├── requirements.txt     # Python dependencies
├── .gitignore          # Git ignore rules
└── README.md           # This file
```

## Technologies Used

- **PyQt6**: GUI framework
- **SQLAlchemy**: Database ORM
- **Pandas**: Data manipulation and analysis
- **openpyxl**: Excel file support
- **python-dotenv**: Environment variable management

# Aurora Archive - Advanced Library Management System

## Overview
A next-generation library membership system combining physical trading cards with digital identity management, subscription services, and AI-generated personalized content.

## Core Features
- Steganographic identity cards
- Tier-based subscription model
- Dynamic card generation (Stable Diffusion / Grok API)
- Motion card animations
- Payment processing (simulation)
- Vector database indexing

## File Structure
/aurora_archive/
├── src/
│   ├── account_mod.py
│   ├── card_motion.py
│   ├── image_pipe.py
│   └── ...
├── config/
│   ├── tier_config.json
│   └── pricing_config.json
├── data/
│   └── members.jsonl
├── docs/
│   ├── ethics.md
│   └── API.md
└── README.md

## License

[Add your license here]

## Author

[Add your name here]
