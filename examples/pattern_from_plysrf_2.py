list1 = [0, 1, 2]
list2 = [4, 5, 6]
ziplist = zip(list1, list2)
dict1 = {j: i for i, j in ziplist}
print(dict1)