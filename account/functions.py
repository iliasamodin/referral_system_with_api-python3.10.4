from string import digits, ascii_uppercase


# Function for converting numbers to an arbitrary number system, 
#   up to the thirty-six number system
def convert_to_another_system(
        number, 
        number_system, 
        digits=digits+ascii_uppercase
    ):

    if number_system > len(digits): 
        return None

    resulting_string = ""
    while number > 0:
        resulting_string = digits[number % number_system] + resulting_string
        number //= number_system

    return resulting_string