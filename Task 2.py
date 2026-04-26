def is_balanced(expression):
    stack = []
    # Mapping of closing to opening brackets
    bracket_map = {')': '(', '}': '{', ']': '['}

    for char in expression:
        if char in "({[":
            stack.append(char)
        elif char in ")}]":
            if not stack or stack[-1] != bracket_map[char]:
                return "Not Balanced"
            stack.pop()

    return "Balanced" if not stack else "Not Balanced"


# Example usage:
print(is_balanced("(a+b)*(c+d)"))   # Balanced
print(is_balanced("(a+b)*(c+d"))    # Not Balanced
print(is_balanced("{[a+b]*(c+d)}")) # Balanced
print(is_balanced("{[a+b]*(c+d)"))  # Not Balanced
