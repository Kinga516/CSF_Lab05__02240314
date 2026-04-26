class Stack:
    def __init__(self):
        self.stack = []

    # Push operation
    def push(self, item):
        self.stack.append(item)

    # Pop operation
    def pop(self):
        if self.is_empty():
            return "Stack is empty"
        return self.stack.pop()

    # Peek operation
    def peek(self):
        if self.is_empty():
            return "Stack is empty"
        return self.stack[-1]

    # Check if stack is empty
    def is_empty(self):
        return len(self.stack) == 0

    # Display stack
    def display(self):
        return self.stack


# Example usage
s = Stack()

# Push elements
s.push(10)
s.push(20)
s.push(30)

print("Stack after pushing elements:")
print(s.display())

# Peek top element
print("\nTop element:", s.peek())

# Pop element
print("\nPopped element:", s.pop())

# Display after popping
print("\nStack after popping:")
print(s.display())

