# BIT502 Assessment 1
# Jessica Balsley
# Student Number: [INSERT STUDENT NUMBER]
# The Aurora Archive - Bookstore Membership System

import os
import sys

# ============================================================================
# CONSTANTS - Easy to modify for future price changes
# ============================================================================

# Membership base prices (monthly)
STANDARD_PRICE = 10
PREMIUM_PRICE = 15
KIDS_PRICE = 5

# Optional extras prices (monthly)
BOOK_RENTAL_PRICE = 5
PRIVATE_AREA_PRICE = 15
MONTHLY_BOOKLET_PRICE = 2
ONLINE_EBOOK_PRICE = 5

# Aurora-Picks rental prices
BASE_RENTAL_PRICE = 1.00  # First 3 days
MID_RENTAL_PRICE = 0.80   # Days 4-8
LATE_RENTAL_PRICE = 0.50  # Days 9-21
MAX_RENTAL_DAYS = 21
MIN_RENTAL_DAYS = 3
FIXED_21_DAY_PRICE = 12.00

# Reading challenge ranks
BRONZE_THRESHOLD = 25
SILVER_THRESHOLD = 50
GOLD_THRESHOLD = 100
RECORD_PAGES = 150


# ============================================================================
# UTILITY FUNCTIONS
# ============================================================================

def clear_screen():
    """Clear the console screen"""
    os.system('cls' if os.name == 'nt' else 'clear')


def get_valid_integer(prompt, min_val=None, max_val=None):
    """
    Get valid integer input from user with optional range validation
    
    Args:
        prompt: Message to display to user
        min_val: Minimum acceptable value (optional)
        max_val: Maximum acceptable value (optional)
    
    Returns:
        Valid integer within specified range
    """
    while True:
        try:
            value = int(input(prompt))
            
            if min_val is not None and value < min_val:
                print(f"Please enter a value of at least {min_val}.")
                continue
            
            if max_val is not None and value > max_val:
                print(f"Please enter a value no greater than {max_val}.")
                continue
            
            return value
            
        except ValueError:
            print("Invalid input. Please enter a valid number.")


def get_valid_number(prompt):
    """
    Get valid numeric input (int or float) from user
    
    Args:
        prompt: Message to display to user
    
    Returns:
        Valid number (float)
    """
    while True:
        try:
            user_input = input(prompt).strip()
            
            if not user_input:
                print("Invalid input. Please enter a valid number.")
                continue
            
            value = float(user_input)
            
            if value < 0:
                print("Please enter a positive number.")
                continue
            
            return value
            
        except ValueError:
            print("Invalid input. Please enter a valid number.")


def get_yes_no(prompt):
    """
    Get yes/no input from user
    
    Args:
        prompt: Message to display to user
    
    Returns:
        True for yes, False for no
    """
    while True:
        response = input(prompt).strip().lower()
        
        if response in ['yes', 'y']:
            return True
        elif response in ['no', 'n']:
            return False
        else:
            print("Invalid choice. Please enter 'yes' or 'no'.")


def pause():
    """Pause and wait for user to press Enter"""
    input("\nPress Enter to continue...")


# ============================================================================
# TASK 2: MEMBERSHIP PLANS
# ============================================================================

def display_membership_cost(plan_type):
    """
    Display membership cost and description for selected plan
    
    Args:
        plan_type: Type of membership (standard, premium, kids)
    """
    clear_screen()
    print("=" * 60)
    print("MEMBERSHIP PLAN DETAILS")
    print("=" * 60)
    
    if plan_type == 'standard':
        monthly = STANDARD_PRICE
        description = "Basic membership providing access to our reading area and\nparticipation in community events."
        plan_name = "Standard Plan"
        
    elif plan_type == 'premium':
        monthly = PREMIUM_PRICE
        description = "Premium membership with exclusive book discounts, priority\naccess to new releases, and invitations to special sales events."
        plan_name = "Premium Plan"
        
    elif plan_type == 'kids':
        monthly = KIDS_PRICE
        description = "Kids membership (ages 12 and under) providing the same benefits\nas Standard, with access to our kid-friendly reading environment."
        plan_name = "Kids Plan"
    
    # Calculate annual cost (11 months - one month free)
    annual = monthly * 11
    
    print(f"\n{plan_name}")
    print("-" * 60)
    print(f"\n{description}")
    print(f"\nMonthly Cost: ${monthly:.2f}")
    print(f"Annual Cost: ${annual:.2f} (Save one month - pay for 11 months only!)")
    print("\n" + "=" * 60)
    
    pause()


def membership_plans_menu():
    """Display membership plans sub-menu and handle selection"""
    while True:
        clear_screen()
        print("=" * 60)
        print("MEMBERSHIP PLANS")
        print("=" * 60)
        print("\n1. Standard")
        print("2. Premium")
        print("3. Kids")
        print("4. Return to main menu")
        print("5. Exit")
        print("\n" + "=" * 60)
        
        choice = get_valid_integer("\nEnter your selection (1-5): ", 1, 5)
        
        if choice == 1:
            display_membership_cost('standard')
        elif choice == 2:
            display_membership_cost('premium')
        elif choice == 3:
            display_membership_cost('kids')
        elif choice == 4:
            return  # Return to main menu
        elif choice == 5:
            exit_program()


# ============================================================================
# TASK 3: OPTIONAL EXTRAS
# ============================================================================

def optional_extras():
    """Handle optional extras selection and calculation"""
    clear_screen()
    print("=" * 60)
    print("OPTIONAL EXTRAS")
    print("=" * 60)
    print("\nEnhance your membership with these additional services:")
    print("-" * 60)
    print(f"\n1. Book Rental - ${BOOK_RENTAL_PRICE:.2f}/month")
    print("   Borrow one book at a time from our select range.")
    print("   Return and borrow up to twice per month.")
    
    print(f"\n2. Private Area Access - ${PRIVATE_AREA_PRICE:.2f}/month")
    print("   Access to our second floor quiet reading area")
    print("   with comfortable seating.")
    
    print(f"\n3. Monthly Booklet - ${MONTHLY_BOOKLET_PRICE:.2f}/month")
    print("   Receive our monthly newsletter with book reviews,")
    print("   upcoming events, and new release information.")
    
    print(f"\n4. Online Ebook Rental - ${ONLINE_EBOOK_PRICE:.2f}/month")
    print("   Access our e-reader library. Borrow one book at a time")
    print("   with automatic 7-day return.")
    
    print("\n" + "=" * 60)
    
    pause()
    
    # Get user selections
    clear_screen()
    print("=" * 60)
    print("SELECT YOUR OPTIONAL EXTRAS")
    print("=" * 60 + "\n")
    
    selections = []
    total_cost = 0
    
    # Book rental
    if get_yes_no(f"Would you like Book Rental for ${BOOK_RENTAL_PRICE:.2f}? (yes/no): "):
        selections.append(f"Book Rental - ${BOOK_RENTAL_PRICE:.2f}")
        total_cost += BOOK_RENTAL_PRICE
    
    # Private area
    if get_yes_no(f"Would you like Private Area Access for ${PRIVATE_AREA_PRICE:.2f}? (yes/no): "):
        selections.append(f"Private Area Access - ${PRIVATE_AREA_PRICE:.2f}")
        total_cost += PRIVATE_AREA_PRICE
    
    # Monthly booklet
    if get_yes_no(f"Would you like the Monthly Booklet for ${MONTHLY_BOOKLET_PRICE:.2f}? (yes/no): "):
        selections.append(f"Monthly Booklet - ${MONTHLY_BOOKLET_PRICE:.2f}")
        total_cost += MONTHLY_BOOKLET_PRICE
    
    # Online ebook
    if get_yes_no(f"Would you like Online Ebook Rental for ${ONLINE_EBOOK_PRICE:.2f}? (yes/no): "):
        selections.append(f"Online Ebook Rental - ${ONLINE_EBOOK_PRICE:.2f}")
        total_cost += ONLINE_EBOOK_PRICE
    
    # Display summary
    clear_screen()
    print("=" * 60)
    print("SELECTED EXTRAS SUMMARY")
    print("=" * 60)
    
    if selections:
        print("\nYou have selected:")
        for item in selections:
            print(f"  • {item}")
        print("\n" + "-" * 60)
        print(f"Total Monthly Cost: ${total_cost:.2f}")
    else:
        print("\nNo extras selected.")
        print(f"Total Monthly Cost: $0.00")
    
    print("=" * 60)
    pause()


# ============================================================================
# TASK 4: KIDS' READING CHALLENGE
# ============================================================================

def kids_reading_challenge():
    """Handle kids' reading challenge input and ranking"""
    clear_screen()
    print("=" * 60)
    print("KIDS' READING CHALLENGE")
    print("=" * 60)
    print("\nWelcome to the Reading Challenge!")
    print("Please enter the number of pages you read each weekday.")
    print("\n" + "=" * 60)
    
    pause()
    
    days = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday']
    pages = []
    
    # Collect pages for each day
    clear_screen()
    print("=" * 60)
    print("ENTER YOUR READING PROGRESS")
    print("=" * 60 + "\n")
    
    for day in days:
        page_count = get_valid_number(f"{day}: ")
        pages.append(page_count)
    
    # Calculate results
    total_pages = sum(pages)
    average_pages = total_pages / len(pages)
    max_pages = max(pages)
    
    # Find day(s) with most pages
    best_days = [days[i] for i, p in enumerate(pages) if p == max_pages]
    
    # Determine rank
    if total_pages <= BRONZE_THRESHOLD:
        rank = "Bronze"
        pages_to_next = BRONZE_THRESHOLD + 1 - total_pages
        next_rank = "Silver"
    elif total_pages <= SILVER_THRESHOLD:
        rank = "Silver"
        pages_to_next = SILVER_THRESHOLD + 1 - total_pages
        next_rank = "Gold"
    elif total_pages <= GOLD_THRESHOLD:
        rank = "Gold"
        pages_to_next = GOLD_THRESHOLD + 1 - total_pages
        next_rank = "Platinum"
    else:
        rank = "Platinum"
        pages_to_next = 0
        next_rank = None
    
    # Check for record break
    broke_record = total_pages > RECORD_PAGES
    
    # Display results
    clear_screen()
    print("=" * 60)
    print("READING CHALLENGE RESULTS")
    print("=" * 60)
    print(f"\nTotal pages read: {total_pages:.1f}")
    print(f"Average pages per day: {average_pages:.1f}")
    
    # Display best day(s)
    if len(best_days) == 1:
        print(f"{best_days[0]} was your biggest reading day!")
    else:
        print(f"{', '.join(best_days)} were your biggest reading days!")
    
    print(f"\nYou ranked {rank}!")
    
    # Next rank info
    if next_rank:
        print(f"To reach {next_rank} rank you need to read {pages_to_next:.1f} more pages.")
    else:
        print("Congratulations! You've achieved the highest rank!")
    
    # Record check
    if broke_record:
        print("\n" + "=" * 60)
        print("🌟 AMAZING! YOU BROKE THE RECORD! 🌟")
        print(f"The previous record was {RECORD_PAGES} pages!")
        print("You are a true reading champion!")
        print("=" * 60)
    
    print("\nGood luck with your reading journey!")
    print("=" * 60)
    
    pause()


# ============================================================================
# TASK 5: AURORA-PICKS RENTAL CALCULATOR
# ============================================================================

def calculate_rental_cost(days):
    """
    Calculate rental cost based on number of days
    
    Args:
        days: Number of rental days
    
    Returns:
        Total rental cost
    """
    # Special case: 21 days fixed price
    if days == MAX_RENTAL_DAYS:
        return FIXED_21_DAY_PRICE
    
    total = 0
    
    # First 3 days at base rate
    if days <= 3:
        total = days * BASE_RENTAL_PRICE
    else:
        total = 3 * BASE_RENTAL_PRICE
        remaining_days = days - 3
        
        # Days 4-8 at mid rate
        if remaining_days <= 5:
            total += remaining_days * MID_RENTAL_PRICE
        else:
            total += 5 * MID_RENTAL_PRICE
            remaining_days -= 5
            
            # Days 9+ at late rate
            total += remaining_days * LATE_RENTAL_PRICE
    
    return total


def aurora_picks_rental():
    """Handle Aurora-Picks rental calculation sub-menu"""
    while True:
        clear_screen()
        print("=" * 60)
        print("AURORA-PICKS RENTAL CALCULATOR")
        print("=" * 60)
        print("\nSpecially selected books available for rental!")
        print("\nRental Pricing:")
        print(f"  • First 3 days: ${BASE_RENTAL_PRICE:.2f} per day")
        print(f"  • Days 4-8: ${MID_RENTAL_PRICE:.2f} per day")
        print(f"  • Days 9-21: ${LATE_RENTAL_PRICE:.2f} per day")
        print(f"  • 21-day rental: Fixed price of ${FIXED_21_DAY_PRICE:.2f}")
        print(f"\nMinimum rental: {MIN_RENTAL_DAYS} days")
        print(f"Maximum rental: {MAX_RENTAL_DAYS} days")
        print("\n" + "=" * 60)
        print("\n1. Enter rental period")
        print("2. Return to main menu")
        print("\n" + "=" * 60)
        
        choice = get_valid_integer("\nEnter your selection (1-2): ", 1, 2)
        
        if choice == 1:
            # Get rental days
            print("\n" + "-" * 60)
            days = get_valid_integer(
                f"Enter number of days ({MIN_RENTAL_DAYS}-{MAX_RENTAL_DAYS}): ",
                MIN_RENTAL_DAYS,
                MAX_RENTAL_DAYS
            )
            
            # Calculate cost
            cost = calculate_rental_cost(days)
            
            # Display result
            print("\n" + "=" * 60)
            print(f"Rental period: {days} days")
            print(f"Total cost: ${cost:.2f}")
            print("=" * 60)
            
            pause()
            
        elif choice == 2:
            return  # Return to main menu


# ============================================================================
# MAIN MENU
# ============================================================================

def display_main_menu():
    """Display the main menu"""
    clear_screen()
    print("=" * 60)
    print("THE AURORA ARCHIVE")
    print("Bookstore Membership System")
    print("=" * 60)
    print("\n1. Membership Plans")
    print("2. Optional Extras")
    print("3. Reading Challenge")
    print("4. Aurora-Picks Rental Calculator")
    print("5. Exit the program")
    print("\n" + "=" * 60)


def exit_program():
    """Exit the program with a message"""
    clear_screen()
    print("\n" + "=" * 60)
    print("Thank you for using The Aurora Archive system!")
    print("We look forward to seeing you again.")
    print("=" * 60 + "\n")
    sys.exit(0)


def main():
    """Main program loop"""
    while True:
        display_main_menu()
        
        choice = get_valid_integer("\nEnter your selection (1-5): ", 1, 5)
        
        if choice == 1:
            membership_plans_menu()
        elif choice == 2:
            optional_extras()
        elif choice == 3:
            kids_reading_challenge()
        elif choice == 4:
            aurora_picks_rental()
        elif choice == 5:
            exit_program()


if __name__ == '__main__':
    main()
