def is_palindrome(s):
    # Normalize the string by removing spaces and converting to lowercase
    s = s.replace(" ", "").lower()
    
    # Check if the string is equal to its reverse
    return s == s[::-1]

# Example usage:
print(is_palindrome("A man a plan a canal Panama"))  # Output: True
print(is_palindrome("Hello, World!"))               # Output: False

# Original code that prints 2+2
print(2 + 2)