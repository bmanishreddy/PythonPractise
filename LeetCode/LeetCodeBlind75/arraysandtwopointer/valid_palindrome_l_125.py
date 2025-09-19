class Solution:
    def isPalindrome(self, s: str) -> bool:
        l, r = 0, len(s) - 1

        while l < r:
            if not self.alphaNum(s[l]):
                l = l+1
            if not self.alphaNum(s[r]):
                r = r-1
            elif s[l].lower() != s[r].lower():
                return False
            else:
                l = l+1
                r = r-1
        return True

    def alphaNum(self, c):
        return ord('A') <= ord(c) <= ord('Z') or \
               ord('a') <= ord(c) <= ord('z') or \
               ord('0') <= ord(c) <= ord('9')

# Test cases
solution = Solution()

# Test case 1: "A man, a plan, a canal: Panama"
print(solution.isPalindrome("A man, a plan, a canal: Panama"))  # Output: True

# Test case 2: "race a car"
print(solution.isPalindrome("race a car"))  # Output: False

# Test case 3: " "
print(solution.isPalindrome(" "))  # Output: True