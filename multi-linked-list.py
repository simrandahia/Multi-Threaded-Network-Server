class Node:
    def __init__(self, data):
        self.data = data
        self.next = None  # Link to the next element in the shared list
        self.book_next = None  # Link to the next item in the same book
        self.next_frequent_search = None  # Link to the next item with frequent search terms


class Book:
    def __init__(self, name):
        self.name = name
        self.content_head = None  # Head of the linked list for the book's content
        self.content_tail = None  # Tail of the linked list for efficient appending

    def add_line(self, line):
        new_node = Node(line)
        if self.content_head is None:
            self.content_head = new_node
            self.content_tail = new_node
        else:
            self.content_tail.next = new_node
            self.content_tail = new_node

    def display_content(self):
        current = self.content_head
        while current:
            print(current.data)
            current = current.next


class MultiLinkedList:
    def __init__(self):
        self.shared_head = None  # Head of the shared list pointing to the order of books received

    def add_book(self, book):
        new_node = Node(book)
        if self.shared_head is None:
            self.shared_head = new_node
        else:
            current = self.shared_head
            while current.next:
                current = current.next
            current.next = new_node

    def display_books_order(self):
        current = self.shared_head
        while current:
            print(f"Received Book: {current.data.name}")
            current = current.next


# Example usage:
multi_list = MultiLinkedList()

book1 = Book("Book A")
book1.add_line("Line 1")
book1.add_line("Line 2")
book1.add_line("Line 3")

book2 = Book("Book B")
book2.add_line("Chapter 1")
book2.add_line("Chapter 2")
book2.add_line("Chapter 3")

multi_list.add_book(book1)
multi_list.add_book(book2)

# Display the order in which books were received
multi_list.display_books_order()
