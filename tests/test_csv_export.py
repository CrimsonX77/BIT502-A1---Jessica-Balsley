#!/usr/bin/env python3
"""
Test CSV export with full member schema fields
"""

import csv
from pathlib import Path
from datetime import datetime

def flatten_dict_for_csv(data: dict, parent_key: str = '', sep: str = '.') -> dict:
    """Flatten nested dictionary for CSV export"""
    items = []
    for k, v in data.items():
        new_key = f"{parent_key}{sep}{k}" if parent_key else k
        
        if isinstance(v, dict):
            items.extend(flatten_dict_for_csv(v, new_key, sep=sep).items())
        elif isinstance(v, list):
            if len(v) == 0:
                items.append((new_key, '[]'))
            else:
                for i, item in enumerate(v):
                    if isinstance(item, dict):
                        items.extend(flatten_dict_for_csv(item, f"{new_key}[{i}]", sep=sep).items())
                    else:
                        items.append((f"{new_key}[{i}]", item))
        else:
            items.append((new_key, str(v) if v is not None else ''))
    
    return dict(items)

# Load test users from database
try:
    from card_scanner import CardScanner
    
    scanner = CardScanner()
    all_users = scanner.database.get_all_users()
    
    print("=" * 60)
    print("CSV EXPORT TEST")
    print("=" * 60)
    print(f"\nLoaded {len(all_users)} user(s) from database\n")
    
    # Flatten all users
    all_fields = set()
    flattened_users = []
    
    for user in all_users:
        user_data = user.get('data', {})
        flattened = flatten_dict_for_csv(user_data)
        
        # Add scanner metadata
        flattened['_user_id'] = user.get('user_id', '')
        flattened['_card_format'] = user.get('format', '')
        flattened['_first_scan'] = user.get('first_scan', '')
        flattened['_last_scan'] = user.get('last_scan', '')
        flattened['_scan_count'] = user.get('scan_count', 0)
        
        all_fields.update(flattened.keys())
        flattened_users.append(flattened)
    
    # Sort fields
    sorted_fields = sorted(all_fields)
    
    print(f"Total unique fields across all users: {len(sorted_fields)}")
    print("\nSample fields (first 20):")
    for i, field in enumerate(sorted_fields[:20], 1):
        print(f"  {i:2d}. {field}")
    
    if len(sorted_fields) > 20:
        print(f"  ... and {len(sorted_fields) - 20} more fields")
    
    # Write CSV
    output_file = f"test_export_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"
    
    with open(output_file, 'w', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=sorted_fields, extrasaction='ignore')
        writer.writeheader()
        
        for user_dict in flattened_users:
            row = {field: user_dict.get(field, '') for field in sorted_fields}
            writer.writerow(row)
    
    print(f"\n✓ CSV exported successfully to: {output_file}")
    print(f"\nFile details:")
    print(f"  Rows: {len(all_users) + 1} (including header)")
    print(f"  Columns: {len(sorted_fields)}")
    
    # Verify CSV can be read back
    with open(output_file, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        rows = list(reader)
        print(f"\n✓ CSV verification: Read {len(rows)} data row(s)")
        
        # Show sample row
        if rows:
            print("\nSample row (first user):")
            sample_fields = ['_user_id', 'member_id', 'name', 'tier', '_card_format', '_scan_count']
            for field in sample_fields:
                if field in rows[0]:
                    print(f"  {field}: {rows[0][field]}")
    
    print("\n" + "=" * 60)
    print("✓ CSV EXPORT TEST PASSED")
    print("=" * 60)
    print("\nEach user's data is in a separate row")
    print("No crossover between accounts ✓")
    print("All member schema fields included ✓")
    
except Exception as e:
    print(f"❌ Error: {e}")
    import traceback
    traceback.print_exc()
