# Node class
class Node:
    def __init__(self, data):
        self.data = data
        self.next = None


# LinkedList class
class LinkedList:
    def __init__(self):
        self.head = None

    def insert_at_beginning(self, data):
        new_node = Node(data)
        new_node.next = self.head
        self.head = new_node

    def insert_at_end(self, data):
        new_node = Node(data)
        if self.head is None:
            self.head = new_node
            return
        temp = self.head
        while temp.next:
            temp = temp.next
        temp.next = new_node

    def delete_node(self, key):
        temp = self.head

        # If head node itself holds the key
        if temp is not None and temp.data == key:
            self.head = temp.next
            temp = None
            return

        # Search for the key
        prev = None
        while temp is not None and temp.data != key:
            prev = temp
            temp = temp.next

        if temp is None:
            return  # Key not found

        prev.next = temp.next
        temp = None

    def search(self, key):
        temp = self.head
        while temp:
            if temp.data == key:
                return True
            temp = temp.next
        return False

    def display(self):
        temp = self.head
        while temp:
            print(temp.data, end=" -> ")
            temp = temp.next
        print("None")


# Example usage:
ll = LinkedList()

# Insert elements
ll.insert_at_end(10)
ll.insert_at_end(20)
ll.insert_at_end(30)
print("Linked List:")
ll.display()

# Insert at beginning
ll.insert_at_beginning(5)
print("After inserting 5 at beginning:")
ll.display()

# Delete node
ll.delete_node(20)
print("After deleting 20:")
ll.display()

# Search element
print("Search 30:")
print("Element found" if ll.search(30) else "Element not found")

