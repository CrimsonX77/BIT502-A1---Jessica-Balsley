from datetime import datetime

def check_due_dates(member_data):
    overdue_items = []
    upcoming_due = []
    for rental in member_data.get('rentals', []):
        due_date = datetime.fromisoformat(rental['due_date'])
        days_until_due = (due_date - datetime.now()).days
        if days_until_due < 0:
            overdue_items.append({
                **rental,
                "late_fee": calculate_late_fee(abs(days_until_due))
            })
        elif days_until_due <= 2:
            upcoming_due.append(rental)
    return overdue_items, upcoming_due

# ... (Add late_fee calc, integrate with Aurora-Picks logic from assessment)    

def calculate_late_fee(days_late):
    base_fee = 5.00
    daily_fee = 1.00
    return base_fee + (daily_fee * days_late)