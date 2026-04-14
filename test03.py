class Basic:
    def __init__(self, owner):
        self.owner = owner


class A(Basic):
    def __init__(self, owner,  rect):
        super().__init__(owner)
        self.rect = rect

a = A(None, 'rect')
print(a.rect)

