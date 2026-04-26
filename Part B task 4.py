class CustomerServiceQueue:
    def __init__(self):
        self.queue = []

    def add_customer(self, name):
        self.queue.append(name)

    def serve_customer(self):
        if not self.is_empty():
            served = self.queue.pop(0)
            print("Serving customer:", served)
            return served
        else:
            print("No customers in queue")
            return None

    def is_empty(self):
        return len(self.queue) == 0

    def display(self):
        print("Customers waiting:")
        print(self.queue)


# Example usage:
csq = CustomerServiceQueue()

# Add customers
csq.add_customer("Sonam")
csq.add_customer("Pema")
csq.add_customer("Karma")

# Display queue
csq.display()

# Serve first customer
csq.serve_customer()

# Display remaining queue
print("Remaining queue:")
print(csq.queue)
