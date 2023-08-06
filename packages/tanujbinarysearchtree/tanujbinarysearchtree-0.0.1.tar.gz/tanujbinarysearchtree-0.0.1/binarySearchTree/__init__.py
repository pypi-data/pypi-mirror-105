def class Node:
    def __init__(self, data):
        self.data = data
        self.left = None
        self.right = None


class BST:
    def __init__(self):
        self.root = None

    def insert(self, value):
        node = Node(value)
        if self.root is None:
            self.root = node
        else:
            temp = self.root
            cur = temp
            while temp is not None:
                cur = temp
                if value > temp.data:
                    temp = temp.right
                else:
                    temp = temp.left
            if value > cur.data:
                cur.right = node
            else:
                cur.left = node

    def preorder(self, temp):
        if temp is None:
            return
        print(temp.data, end=' ')
        self.preorder(temp.left)
        self.preorder(temp.right)

    def postorder(self, temp):
        if temp is None:
            return
        self.postorder(temp.left)
        self.postorder(temp.right)
        print(temp.data, end=' ')

    def inorder(self, temp):
        if temp is None:
            return
        self.inorder(temp.left)
        print(temp.data, end=' ')
        self.inorder(temp.right)



