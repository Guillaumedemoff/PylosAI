import copy


class Tree:
    def __init__(self, value, action =None, children=[]):
        self.__value = value
        self.__children = copy.deepcopy(children)
        self.action = copy.deepcopy(action)
        self.__tree = {'parent': self.__value, 'children':[c.json for c in self.__children]}


    def __getitem__(self, index):
        return self.__children[index]

    def __str__(self):
        def _str(tree, level):
            result = '[{}] A{}\n'.format(tree.__value, tree.action)
            for child in tree.children:
                result += '{}|--{}'.format('    '*level, _str(child, level + 1))
            return result
        return _str(self, 0)

    def __lt__(self, other):
        return self.value < other.value

    def ___le__(self, other):
        return self.value <= other.value

    def __eq__(self, other):
        return self.value == other.value

    def __ne__(self, other):
        return self.value != other.value

    def __gt__(self, other):
        return self.value > other.value

    def __ge__(self, other):
        return self.value >= other.value

    @property
    def value(self):
        return self.__value

    @property
    def children(self):
        return copy.deepcopy(self.__children)

    @property
    def childrenVal(self):
        childr = []
        for child in self.__children:
            childr.append(child.value)
        return childr

    @property
    def size(self):
        result = 1
        for child in self.__children:
            result += child.size
        return result
    @property
    def json(self):
        return self.__tree

    def addChild(self, tree):
        self.__children.append(tree)




c1 = Tree(25, [Tree(-9)])
c2 = Tree(12)
c3 = Tree(14)




def treeMaker(n):
    return Tree(1, [treeMaker(n-1) for i in range(n)])

#oxoTree = treeMaker(3)
#print(oxoTree)
