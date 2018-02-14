class Stack:
     def __init__(self):
         self.items = []

     def isEmpty(self):
         return self.items == []

     def push(self, item):
         self.items.append(item)

     def pop(self):
         return self.items.pop()

     def top(self):
         return self.items[len(self.items)-1]

     def size(self):
         return len(self.items)
     
     def printStack(self):
        print 'Stack: '
        for i in self.items:
            print str(i),
        if(not self.items):
            print 'EMPTY'

def main():
    map = {}
    map["key"] = '212'
    map["key2"] = '345'
    print map
    print map["key"]
    print map["key2"]

if __name__ == "__main__":
    main()


