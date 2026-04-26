class Queue:
    def __init__(self):
        self.items = []

    def enqueue(self, item):
        self.items.append(item)

    def dequeue(self):
        if not self.is_empty():
            return self.items.pop(0)
        else:
            return "Queue is empty"

    def front(self):
        if not self.is_empty():
            return self.items[0]
        else:
            return "Queue is empty"

    def is_empty(self):
        return len(self.items) == 0

    def display(self):
        return self.items


# Example usage:
q = Queue()

# Enqueue elements
q.enqueue(100)
q.enqueue(200)
q.enqueue(300)
print("Queue after enqueue:")
print(q.display())

# Front element
print("Front element:", q.front())

# Dequeue element
print("Dequeued element:", q.dequeue())

# Queue after dequeue
print("Queue after dequeue:")
print(q.display())
