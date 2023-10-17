class Stack:
    class Obj:
        def __init__(self, data):
            self.data = data
            self.next = None
            self.prev = None

        def __repr__(self):
            return self.data.__repr__()

    def __init__(self, *args):
        self.head = self.tail = None

        if args:
            for elem in args:
                self.append(elem)

    def append(self, data):
        if self.head is None:
            self.head = self.tail = self.Obj(data)
        else:
            obj = self.Obj(data)
            obj.prev = self.tail
            self.tail.next = self.tail = obj

    def appendleft(self, data):
        if self.head is None:
            self.head = self.tail = self.Obj(data)
        else:
            obj = self.Obj(data)
            obj.next = self.head
            self.head.prev = self.head = obj

    def __iter__(self):
        start = self.head
        while start:
            yield start
            start = start.next


stack = Stack()
stack.append(10)
stack.append(20)
stack.append(30)
stack.append(40)
stack.append(50)

stack.appendleft(10)
stack.appendleft(20)
stack.appendleft(30)
stack.appendleft(40)
stack.appendleft(50)

for elem in stack:
    print(elem)
