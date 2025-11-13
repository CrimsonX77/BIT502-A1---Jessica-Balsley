#!/usr/bin/env python3
"""
Test Card Scanner Module
Quick test to verify card scanning functionality
"""

from card_scanner import CardScanner, CardFormat
from pathlib import Path

def test_scanner():
    """Test the card scanner with existing embedded cards"""
    
    print("="*60)
    print("Card Scanner Test")
    print("="*60)
    print()
    
    # Test card path - use relative path or search in common locations
    test_card = "test_card_embedded22.png"
    
    # Try to find the test card in common locations
    possible_paths = [
        Path(test_card),  # Current directory
        Path("tests") / test_card,  # tests directory
        Path("cards") / test_card,  # cards directory
        Path("output") / test_card,  # output directory
    ]
    
    card_path = None
    for path in possible_paths:
        if path.exists():
            card_path = str(path)
            break
    
    if not card_path:
        print(f"❌ Test card not found: {test_card}")
        print(f"   Searched in: {', '.join([str(p) for p in possible_paths])}")
        print("   Please ensure you have an embedded card image.")
        return
    
    # Create scanner
    scanner = CardScanner()
    
    try:
        print(f"📷 Scanning card: {Path(card_path).name}")
        print()
        
        # Scan the card
        data, card_format = scanner.scan_card(card_path, register_user=True)
        
        print(f"✓ Card format detected: {card_format}")
        print()
        print("─"*60)
        print("ACCOUNT DETAILS:")
        print("─"*60)
        print(scanner.display_account_details())
        
        print()
        print("="*60)
        print("DATABASE TEST:")
        print("="*60)
        print(scanner.list_all_users())
        
        print()
        print("✓ Scanner test completed successfully!")
        
    except FileNotFoundError as e:
        print(f"❌ File error: {e}")
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    test_scanner()
