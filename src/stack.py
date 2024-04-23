class StackOverflowError(Exception):
    """Exception raised when attempting to push an item onto a full stack."""
    pass

class StackUnderflowError(Exception):
    """Exception raised when attempting to pop an item from an empty stack."""
    pass

class Stack:
    def __init__(self, size):
        self.size = size
        self.items = []
        self.top = 0

    def is_empty(self):
        """Check if the stack is empty."""
        return self.top == 0

    def push(self, element):
        """Push an element onto the stack."""
        if self.top == self.size:
            raise StackOverflowError("Stack overflow")
        self.items.append(element)
        self.top += 1

    def pop(self):
        """Pop an element from the stack."""
        if self.is_empty():
            raise StackUnderflowError("Stack underflow")
        self.top -= 1
        return self.items.pop()

# Example usage:
try:
    stack = Stack(3)
    stack.push(1)
    stack.push(2)
    stack.push(3)

    print("Stack is empty:", stack.is_empty())
    print("Popped item:", stack.pop())
    print("Popped item:", stack.pop())
    print("Popped item:", stack.pop())
    print("Stack is empty:", stack.is_empty())

    # This will raise an error because the stack is empty
    print("Popped item:", stack.pop())

except StackOverflowError as e:
    print(e)
except StackUnderflowError as e:
    print(e)
