class Node:
    def __init__(self, value=None):
        self.value = value
        self.nextn = None


class List:
    def __init__(self):
        self.head = None

    def append(self, node):
        if not self.head:
            self.head = Node(node)
            return

        last_node = self.head
        while last_node.nextn:
            last_node = last_node.nextn
        last_node.nextn = Node(node)
        
    def __str__(self):
        numbers = ""
        last_node = self.head
        numbers = f'{last_node.value}'
        while last_node.nextn:
            last_node = last_node.nextn
            numbers = f'{numbers + ", " + last_node.value}'
        return str(numbers)


mylist = List()
while True:
    number = input("Extend the list: ")
    mylist.append(number)
    print(mylist)

