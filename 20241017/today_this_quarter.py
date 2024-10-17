import calendar
import datetime
from colorama import Fore, Back, Style, init

# Initialize colorama
init(autoreset=True)

def print_month_with_highlight(year, month, today_day=None):
    """Print the month with today highlighted if it's in the current month."""
    cal = calendar.monthcalendar(year, month)

    # Print the month and year header
    print(f"{calendar.month_name[month]} {year}".center(20))
    print("Su Mo Tu We Th Fr Sa")

    # Print each week, highlighting today's date if it matches
    for week in cal:
        week_str = ""
        for day in week:
            if day == 0:  # Empty days (padding in calendar)
                week_str += "   "
            elif day == today_day:
                # Highlight today with a green background and ensure two-digit width
                week_str += Back.GREEN + f"{day:2}" + Style.RESET_ALL + " "
            else:
                # Print other days with two-digit width
                week_str += f"{day:2} "
        print(week_str.strip())

def print_current_quarter():
    """Prints the three months of the current quarter with today highlighted."""
    now = datetime.datetime.now()
    current_month = now.month
    current_day = now.day
    current_year = now.year
    
    # Determine the current quarter based on the current month
    if 1 <= current_month <= 3:
        quarter_months = [1, 2, 3]
    elif 4 <= current_month <= 6:
        quarter_months = [4, 5, 6]
    elif 7 <= current_month <= 9:
        quarter_months = [7, 8, 9]
    else:
        quarter_months = [10, 11, 12]
    
    # Print each month in the quarter, highlighting today's date in the current month
    for month in quarter_months:
        if month == current_month:
            print_month_with_highlight(current_year, month, current_day)
        else:
            print_month_with_highlight(current_year, month)
        print()  # Add space between months

if __name__ == "__main__":
    print_current_quarter()
