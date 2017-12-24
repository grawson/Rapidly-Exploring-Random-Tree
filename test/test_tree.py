from src.TreeMap import TreeMap

tm = TreeMap()

data1 = (10, 20)
assert tm.add_node(data1)
node1 = tm.find(data1)
assert node1.data == data1
assert tm.find((20, 10)) is None
assert tm.path(node1) == [data1]
assert tm.data_list == [data1]

data2 = (100, 200)
assert tm.add_node(data2, node1)
node2 = tm.find(data2)
assert node2.data == data2
assert tm.path(node2) == [data1, data2]
assert tm.data_list == [data1, data2]

data3 = (200, 200)
assert tm.add_node(data3)
node3 = tm.find(data3)
assert node3.data == data3
assert tm.path(node3) == [data3]
assert tm.data_list == [data1, data2, data3]

assert not tm.point_in_range((600, 600), 5)
assert tm.point_in_range((202, 201), 5)

