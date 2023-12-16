from datetime import datetime, timedelta
from dateutil import parser

def find_format(classes: list[str]) -> str:
    """Default the NEO Student format to Online."""
    for c in classes:
        if c.startswith("Miftaah Associate Program:"):
            return "Associates"
        elif c.startswith("Miftaah Online:"):
            return "Online"
        return "Online"
    

def find_grade(joined_at: str) -> str:
    """
    Input: date str when student joined
    Output: Year based on years passed since then
    """
    try:
        join_date = parser.parse(joined_at)
    except ValueError:
        return "Invalid datetime format"

    current_date = datetime.now()
    years_passed = current_date.year - join_date.year

    return f"Year {years_passed + 1}"

def month_year_format(date_str: str) -> str:
    """
    Input: Raw Date string
    Output: January 2023
    """
    try:
        date = parser.parse(date_str)
    except ValueError:
        return "Invalid datetime format"

    return date.strftime("%B %Y")


def expected_grad(joined_at: str) -> str:
    """
    Input: date str when student joined
    Output: expected graduation in month/year format (4 years after start date)
    """
    try:
        join_date = parser.parse(joined_at)
    except ValueError:
        return "Invalid datetime format"

    end_date = join_date + timedelta(days=365 * 4)
    formatted_result = end_date.strftime('%B %Y')

    return formatted_result

if __name__ == "__main__":
    
    date_str = "2023-05-16T09:51:55.000Z"

    # testing month_year_format
    # myf = month_year_format("2023-05-16T09:51:55.000Z")
    # print(myf)

    # expected_grad
    eg = expected_grad(date_str)
    print(eg)
