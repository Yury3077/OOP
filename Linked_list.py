from weakref import ref
from Driver import IStructureDriver


class _Node:
    def __init__(self, data, prev_node=None, next_node=None):
        self.next_node = next_node
        self.prev_node = prev_node
        self.data = data

    @property
    def prev_node(self):
        return self._prev_node() if self._prev_node is not None else None

    @prev_node.setter
    def prev_node(self, value):
        self._prev_node = ref(value) if value is not None else None

    def __str__(self):
        return f' {self.prev_node} - {self.data} - {self.next_node}'

    def __repr__(self):
        return f' {self.prev_node} - {self.data} - {self.next_node}'


class LinkedList:  # индексация списка от 0
    def __init__(self, driver: IStructureDriver = None):
        self.driver = driver
        self._size = 0
        self.head = None
        self.tail = None

    def __len__(self):
        return self._size

    def __iter__(self):
        for node in self._node_iter():
            yield node.data

    def _node_iter(self):
        current = self.head
        while current:
            yield current
            current = current.next_node

    def insert(self, data, index):
        '''
        Insert Node to any place of LinkedList
        node - Node
        index - position of node
        '''
        if not isinstance(index, int):
            raise TypeError

        new_node = _Node(data)
        if self.head is None:
            self.head = new_node
            self.tail = new_node
        else:
            if index == 0:
                self.head.prev_node = new_node
                new_node.next_node = self.head
                self.head = new_node
                self._size += 1
            elif index < len(self):
                for i, node in enumerate(self._node_iter()):
                    if i == index - 1:
                        new_node.next_node = node.next_node
                        node.next_node.prev_node = new_node
                        node.next_node = new_node
                        new_node.prev_node = node
                        self._size += 1
            elif index >= len(self):
                self.append(data)

    def append(self, data):
        '''
        Append Node to tail of LinkedList
        node - Node
        '''
        new_node = _Node(data)
        if self.head is None:
            self.head = new_node
            self.tail = new_node
        else:
            self.tail.next_node = new_node
            new_node.set_prev = self.tail
            self.tail = new_node
        self._size += 1

    def clear(self):
        '''
        Clear LinkedList
        '''
        self.head = None
        self.tail = None
        self._size = 0

    def find(self, node):
        for count_index, i in enumerate(self._node_iter()):
            if node == i.data:
                return count_index
                break
        else:
            raise ValueError("Такого объекта не найдено")

    def remove(self, node):
        index = self.find(node)
        self.delete(index)

    def delete(self, index):
        if index == 0:
            curr = self.head
            self.head = curr.next_node
            self._size -= 1
        elif index < len(self) - 1:
            for i, node in enumerate(self._node_iter()):
                if i == index:
                    n_pr = node.prev_node
                    n_nx = node.next_node
                    n_pr.next_node = node.next_node
                    n_nx.prev_node = node.prev_node
                    self._size -= 1
        elif index == len(self) - 1:
            cur2 = self.tail
            cur2.prev_node.next_node = None
            self.tail = cur2.prev_node
            self._size -= 1
        else:
            print("Неверный индекс")

    def save(self):
        lincked_list = {}
        for node in self._node_iter():
            lincked_list[id(node)] = {
                "data": node.data,
                "next_node": id(node.next_node) if node.next_node else None,
            }
        lincked_list["head"] = id(self.head)
        return self.driver.write(lincked_list)

    def load(self):
        self.clear()
        dict_values = self.driver.read()
        head = dict_values.pop("head")
        current_value = str(head)
        for _ in dict_values:
            node = dict_values[current_value]
            self.append(node['data'])
            current_value = str(node['next_node'])


if __name__ == '__main__':
    some_data = LinkedList()
    some_data.append("se0")
    some_data.append("se1")
    some_data.append("se2")
    some_data.append("se3")
    some_data.append("se4")

    # some_dict = some_data.save()
    # print(some_dict)
    # new_data = LinkedList()
    # new_data.load(some_dict)

    # first = _Node(5)
    # second = _Node(10)
    # first.next_node = second
    # second.prev_node = first
    # print(sys.getrefcount(first))
    # print(sys.getrefcount(second))

    # new_data.insert(51, 3)
    # some_data.clear()
    # print(new_data.find("se4"))
    # new_data.delete(4)
    # some_data.remove("se1")
    for i in some_data:
        print(i)
    # for i2 in new_data:
    #     print(i2)
